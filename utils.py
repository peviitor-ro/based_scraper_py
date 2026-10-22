import requests
import os
import json
import inspect
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

domain = os.environ.get("DOMAIN")
REPO_ROOT = Path(__file__).resolve().parent
MAX_LOG_LENGTH = 4000
REPAIR_TIMEOUT_SECONDS = int(os.getenv("OPENCODE_REPAIR_TIMEOUT", "900"))
EMPTY_REPAIR_ATTEMPT_ENV = "OPENCODE_EMPTY_JOBS_REPAIR_ATTEMPTED"
EMPTY_REPAIR_DISABLED_ENV = "OPENCODE_EMPTY_JOBS_REPAIR_DISABLED"
EMPTY_REPAIR_COOLDOWN_DAYS = int(os.getenv("OPENCODE_EMPTY_JOBS_REPAIR_COOLDOWN_DAYS", "7"))
EMPTY_REPAIR_STATE_PATH = REPO_ROOT / ".cache" / "empty_jobs_repair_state.json"


def get_token():
    """
    Returnează token-ul necesar pentru a face request-uri către API.
    :return: token-ul necesar pentru a face request-uri către API
    """
    endpoint = os.environ.get("TOKEN_ROUTE")
    email = os.environ.get("EMAIL")
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"{domain}{endpoint}"
    response = requests.post(url, json={"email": email}, headers=headers)
    return response.json()["access"]


def create_job(**kwargs):
    job = {}
    job.update(kwargs)
    return job


def truncate_output(content, limit=MAX_LOG_LENGTH):
    if not content:
        return "No output captured."

    content = content.strip()
    if len(content) <= limit:
        return content

    return content[:limit] + "\n...[truncated]"


def utc_now():
    return datetime.now(timezone.utc)


def format_timestamp(value):
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_timestamp(value):
    if not value:
        return None

    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def get_empty_jobs_state_key(script_path):
    try:
        return str(script_path.relative_to(REPO_ROOT))
    except ValueError:
        return str(script_path)


def load_empty_jobs_repair_state():
    if not EMPTY_REPAIR_STATE_PATH.exists():
        return {}

    try:
        with EMPTY_REPAIR_STATE_PATH.open("r", encoding="utf-8") as state_file:
            data = json.load(state_file)
            return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_empty_jobs_repair_state(state):
    EMPTY_REPAIR_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with EMPTY_REPAIR_STATE_PATH.open("w", encoding="utf-8") as state_file:
        json.dump(state, state_file, indent=2, sort_keys=True)


def update_empty_jobs_repair_state(script_path, company, **fields):
    state = load_empty_jobs_repair_state()
    key = get_empty_jobs_state_key(script_path)
    entry = state.get(key, {})
    entry["company"] = company

    for field_name, value in fields.items():
        if value is not None:
            entry[field_name] = value

    state[key] = entry
    save_empty_jobs_repair_state(state)


def clear_empty_jobs_repair_state(script_path):
    state = load_empty_jobs_repair_state()
    key = get_empty_jobs_state_key(script_path)

    if key not in state:
        return

    state.pop(key, None)
    if state:
        save_empty_jobs_repair_state(state)
    else:
        EMPTY_REPAIR_STATE_PATH.unlink(missing_ok=True)


def get_empty_jobs_repair_cooldown_until(script_path):
    state = load_empty_jobs_repair_state()
    entry = state.get(get_empty_jobs_state_key(script_path))
    if not isinstance(entry, dict):
        return None

    confirmed_empty_at = parse_timestamp(entry.get("last_confirmed_empty_at"))
    if confirmed_empty_at is None:
        return None

    return confirmed_empty_at + timedelta(days=EMPTY_REPAIR_COOLDOWN_DAYS)


def snapshot_sibling_files(script_path):
    return {
        path.name
        for path in script_path.parent.iterdir()
        if path.is_file() or path.is_symlink()
    }


def cleanup_created_sibling_files(script_path, existing_files):
    current_files = snapshot_sibling_files(script_path)
    created_files = sorted(current_files - existing_files)

    for file_name in created_files:
        created_file = script_path.parent / file_name
        if created_file == script_path:
            continue

        created_file.unlink(missing_ok=True)
        print(f"Deleted extra file {created_file.name}")


def infer_company_name(module_globals, script_path):
    for key in ("COMPANY", "company", "company_name"):
        value = module_globals.get(key)
        if isinstance(value, dict):
            value = value.get("company")
        if isinstance(value, str) and value.strip():
            return value.strip()

    return script_path.stem


def get_calling_scraper_context():
    current_file = Path(__file__).resolve()
    main_module = sys.modules.get("__main__")
    main_file = getattr(main_module, "__file__", None)
    shared_helper_names = {"ats_common"}

    if main_file:
        main_path = Path(main_file).resolve()
        if (
            main_path != current_file
            and main_path.suffix == ".py"
            and main_path.stem not in shared_helper_names
        ):
            return main_path, infer_company_name(main_module.__dict__, main_path)

    frame = inspect.currentframe()
    if frame is None:
        return None, None

    selected_context = None

    try:
        caller = frame.f_back if frame else None
        while caller:
            caller_path = Path(caller.f_code.co_filename).resolve()
            if caller_path != current_file and caller_path.suffix == ".py":
                if caller_path.stem in shared_helper_names:
                    caller = caller.f_back
                    continue

                company = infer_company_name(caller.f_globals, caller_path)
                if caller.f_globals.get("__name__") == "__main__":
                    return caller_path, company

                if selected_context is None:
                    selected_context = (caller_path, company)
            caller = caller.f_back
    finally:
        del frame

    if selected_context is not None:
        return selected_context

    return None, None


def repair_scraper_with_opencode(script_path, company):
    if shutil.which("opencode") is None:
        print(f"OpenCode is not installed. Cannot auto-repair {script_path.name}.")
        return False

    prompt = (
        f"Fix the scraper `{script_path.relative_to(REPO_ROOT)}`. "
        f"It exits successfully but returns an empty jobs list for company `{company}`. "
        "Check the company's source website, repair the scraper if jobs still exist there, "
        "and rerun the scraper until it no longer returns an empty list unless the company "
        "truly has no jobs left on the source website."
    )
    repair_context = f"""
Scraper: {script_path.relative_to(REPO_ROOT)}
Run command: {sys.executable} {script_path.relative_to(REPO_ROOT)}

Requirements:
- Fix only what is needed for this scraper to return the real jobs.
- Preserve the existing scraper behavior and output schema.
- Keep changes focused; avoid unrelated edits.
- Re-run the scraper after your fix and stop only when it exits successfully.
- Do not leave any extra files next to the scraper.

Observed behavior:
- The scraper returned an empty jobs list.
- Company detected from scraper: {company}
- You must verify the source website directly, not peviitor search results.
""".strip()
    context_file_path = None

    try:
        print(f"Starting OpenCode empty-jobs repair for {script_path.name}...")

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix="_opencode_empty_jobs_context.md",
            delete=False,
            encoding="utf-8",
        ) as context_file:
            context_file.write(repair_context)
            context_file_path = context_file.name

        action = subprocess.run(
            [
                "opencode",
                "run",
                "--dir",
                str(REPO_ROOT),
                "-f",
                str(script_path),
                "-f",
                context_file_path,
                "--",
                prompt,
            ],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=REPAIR_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        print(f"OpenCode empty-jobs repair timed out for {script_path.name}.")
        return False
    finally:
        if context_file_path and os.path.exists(context_file_path):
            os.unlink(context_file_path)

    if action.returncode != 0:
        print(f"OpenCode could not repair {script_path.name}.")
        print(truncate_output(action.stderr or action.stdout))
        return False

    print(f"OpenCode empty-jobs repair finished for {script_path.name}.")
    return True


def rerun_repaired_scraper(script_path):
    env = os.environ.copy()
    env[EMPTY_REPAIR_ATTEMPT_ENV] = "1"

    print(f"Re-running repaired scraper {script_path.name}...")
    action = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
    )

    if action.stdout:
        print(action.stdout, end="" if action.stdout.endswith("\n") else "\n")
    if action.stderr:
        print(action.stderr, end="" if action.stderr.endswith("\n") else "\n")

    if action.returncode != 0:
        raise Exception(
            "Auto-repair rerun failed:\n" + truncate_output(action.stderr or action.stdout)
        )

    return "No jobs Available" in action.stdout or "No jobs Available" in action.stderr


def maybe_repair_empty_jobs_output():
    if os.getenv(EMPTY_REPAIR_DISABLED_ENV) == "1":
        return False

    if os.getenv(EMPTY_REPAIR_ATTEMPT_ENV) == "1":
        print("Empty-jobs auto-repair already attempted for this run.", flush=True)
        return False

    script_path, company = get_calling_scraper_context()
    if not script_path or not company:
        print("Could not detect scraper context for empty-jobs verification.", flush=True)
        return False

    cooldown_until = get_empty_jobs_repair_cooldown_until(script_path)
    if cooldown_until and utc_now() < cooldown_until:
        update_empty_jobs_repair_state(
            script_path,
            company,
            last_empty_at=format_timestamp(utc_now()),
        )
        print(
            f"No jobs returned for {company}. Empty-jobs auto-repair is on cooldown for "
            f"{script_path.name} until {format_timestamp(cooldown_until)}.",
            flush=True,
        )
        return False

    print(
        f"No jobs returned for {company}. Starting direct source verification and repair for "
        f"{script_path.name}...",
        flush=True,
    )

    attempted_at = format_timestamp(utc_now())
    update_empty_jobs_repair_state(
        script_path,
        company,
        last_empty_at=attempted_at,
        last_repair_attempt_at=attempted_at,
    )

    existing_files = snapshot_sibling_files(script_path)
    repaired = repair_scraper_with_opencode(script_path, company)
    cleanup_created_sibling_files(script_path, existing_files)

    if not repaired:
        raise Exception(f"Auto-repair failed for empty jobs result in {script_path.name}.")

    existing_files = snapshot_sibling_files(script_path)
    try:
        rerun_was_empty = rerun_repaired_scraper(script_path)
    finally:
        cleanup_created_sibling_files(script_path, existing_files)

    if rerun_was_empty:
        now = format_timestamp(utc_now())
        update_empty_jobs_repair_state(
            script_path,
            company,
            last_empty_at=now,
            last_confirmed_empty_at=now,
            last_repair_attempt_at=attempted_at,
        )
    else:
        clear_empty_jobs_repair_state(script_path)

    raise SystemExit(0)


def publish_or_update(data):

    if not data:
        maybe_repair_empty_jobs_output()
        print("No jobs Available", flush=True)
        return

    script_path, _ = get_calling_scraper_context()
    if script_path:
        clear_empty_jobs_repair_state(script_path)
    
    route = os.environ.get("ADD_JOBS_ROUTE")
    url = f"{domain}{route}"
    token = os.environ.get("TOKEN") if os.environ.get("TOKEN") else get_token()

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}", "User-Agent": "Mozilla/5.0"}

    res = requests.post(url, headers=headers, json=data)

    status_code = res.status_code

    if status_code == 200:
        company = data[0].get("company")
        total_jobs = len(data)

        print(f"Successfully added {total_jobs} jobs for {company} company.", flush=True)
    else:
        raise Exception(f"Failed to add jobs. Status code: {status_code}")


def publish_logo(company, logo_url):
    content_type = "application/json"
    try:
        requests.post(
            "https://api.peviitor.ro/v3/logo/add/",
            headers={"Content-Type": content_type},
            json=[{"id": company, "logo": logo_url}],
            timeout=10,
        )
    except Exception as e:
        print(f"Failed to publish logo for {company}. Error: {e}")


def show_jobs(data):
    print(json.dumps(data, indent=4))


def translate_city(city):
    city = city.replace(" ", "_")
    cities = {
        # This is general for all scrapers
        "bucharest": "Bucuresti",
        "cluj": "Cluj-Napoca",
        # This is for Arabesque Scraper
        "targul-mures": "Targu-Mures",
        "militari": "Bucuresti",
        ############################
        # This is for Vodafone Scraper
        "cluj_napoca": "Cluj-Napoca",
        "targu_mures": "Targu-Mures",
        "pipera": "Bucuresti",
        ############################
        # This is for ppt
        "campulung_muscel": "Campulung",
        # This is for Strabag
        "petrobrazi": "Ploiesti",
        # This is for CARTOFISSERIE
        "Satu-Mare": "Satu Mare",
        "Piatra_Neamt": "Piatra Neamt",
    }

    if cities.get(city.lower()):
        return cities.get(city.lower())
    else:
        return city.replace("_", " ")


def acurate_city_and_county(**kwargs):
    """
    Returns a dictionary containing accurate city and county information.

    Keyword Arguments:
    **kwargs -- key-value pairs representing city and county information

    Returns:
    A dictionary containing accurate city and county information.
    """
    city_and_county = {}
    if kwargs:
        city_and_county.update(kwargs)
    else:
        city_and_county = {
            "Satu_Mare": {"city": "Satu Mare", "county": "Satu Mare"},
            "Iasi": {"city": "Iasi", "county": "Iasi"},
            "Piatra_Neamt": {"city": "Piatra-Neamt", "county": "Neamt"},
            "Ramnicu_Valcea": {"city": "Ramnicu Valcea", "county": "Valcea"},
        }

    return city_and_county


def get_jobtype(sentence, **kwargs):
    """
    Get the job types mentioned in a sentence.

    Args:
        sentence (str): The sentence to analyze.
        **kwargs: Additional keyword arguments.
            jobs_typse (list): Additional job types to consider.

    Returns:
        list: A list of job types mentioned in the sentence.
    """

    jobs_typse = ["on-site", "remote", "hybrid"]
    jobs_typse.extend(kwargs.get("jobs_typse", []))

    sentence = sentence.lower().replace("_", "-").replace("onsite", "on-site")

    types = [jobtype for jobtype in jobs_typse if jobtype in sentence.lower()]

    return list(set(types))
