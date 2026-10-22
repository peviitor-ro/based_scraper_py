import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from utils import (
    EMPTY_REPAIR_COOLDOWN_DAYS,
    EMPTY_REPAIR_STATE_PATH,
    get_empty_jobs_repair_cooldown_until,
    load_empty_jobs_repair_state,
    parse_timestamp,
    utc_now,
)

EXCLUDE = {
    "__init__.py",
    "main.py",
    "ats_common.py",
}
SITES_DIR = Path(__file__).resolve().parent
REPO_ROOT = SITES_DIR.parent
REPAIR_TIMEOUT_SECONDS = int(os.getenv("OPENCODE_REPAIR_TIMEOUT", "900"))
MAX_LOG_LENGTH = 4000


def log(message):
    print(message, flush=True)


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
        log(f"Deleted extra file {created_file.name}")


def truncate_output(content, limit=MAX_LOG_LENGTH):
    if not content:
        return "No output captured."

    content = content.strip()
    if len(content) <= limit:
        return content

    return content[:limit] + "\n...[truncated]"


NO_JOBS_MARKER = "No jobs Available"


def format_remaining(delta):
    total_seconds = int(delta.total_seconds())
    if total_seconds <= 0:
        return "expired"

    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes = remainder // 60

    if days:
        return f"{days}d {hours}h left"
    if hours:
        return f"{hours}h {minutes}m left"
    return f"{minutes}m left"


def log_empty_jobs_cache():
    state = load_empty_jobs_repair_state()
    cache_path = EMPTY_REPAIR_STATE_PATH

    try:
        cache_display = cache_path.relative_to(REPO_ROOT)
    except ValueError:
        cache_display = cache_path

    if not state:
        log(f"Empty-jobs cache: no entries ({cache_display} missing or empty).")
        log("  Auto-repair will run for every scraper returning 0 jobs, with no cooldown.")
        return

    now = utc_now()
    on_cooldown = []
    cooldown_expired = []

    for state_key, entry in sorted(state.items()):
        if not isinstance(entry, dict):
            continue

        company = entry.get("company") or state_key
        cooldown_until = get_empty_jobs_repair_cooldown_until(REPO_ROOT / state_key)

        if cooldown_until and now < cooldown_until:
            on_cooldown.append((state_key, company, cooldown_until))
        else:
            cooldown_expired.append(
                (state_key, company, parse_timestamp(entry.get("last_confirmed_empty_at")))
            )

    log(f"Empty-jobs cache: {len(state)} scraper(s) known to return 0 jobs ({cache_display}).")
    log(f"  Cooldown lasts {EMPTY_REPAIR_COOLDOWN_DAYS} days after a confirmed empty result.")

    for state_key, company, cooldown_until in on_cooldown:
        log(f"  [on cooldown] {state_key} | {company} | {format_remaining(cooldown_until - now)}")

    for state_key, company, confirmed_at in cooldown_expired:
        confirmed = confirmed_at.strftime("%Y-%m-%d %H:%M UTC") if confirmed_at else "unknown"
        log(f"  [cooldown over] {state_key} | {company} | confirmed empty {confirmed}")

    if not on_cooldown:
        log("  No scraper is currently on cooldown.")


def log_scraper_empty_result(script_path, action):
    stdout = action.stdout or ""
    stderr = action.stderr or ""

    if NO_JOBS_MARKER not in stdout and NO_JOBS_MARKER not in stderr:
        return

    cooldown_until = get_empty_jobs_repair_cooldown_until(script_path)

    if cooldown_until and utc_now() < cooldown_until:
        log(
            f"Empty result for {script_path.name} | on cooldown | "
            f"{format_remaining(cooldown_until - utc_now())} (OpenCode skipped)"
        )
    else:
        log(f"Empty result for {script_path.name} | OpenCode verification will run")


def run_scraper(script_path):
    return subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def get_script_path(scraper_name):
    script_name = scraper_name if scraper_name.endswith(".py") else scraper_name + ".py"
    script_path = SITES_DIR / script_name

    if script_name in EXCLUDE:
        raise ValueError(f"{script_name} cannot be tested manually.")

    if not script_path.exists() or not script_path.is_file():
        raise FileNotFoundError(f"Scraper not found: {script_name}")

    return script_path


def repair_scraper_with_opencode(script_path, failed_action):
    if shutil.which("opencode") is None:
        log(f"OpenCode is not installed. Skipping auto-repair for {script_path.name}.")
        return False

    stderr_output = truncate_output(failed_action.stderr)
    stdout_output = truncate_output(failed_action.stdout)
    prompt = (
        f"Fix the failing scraper `{script_path.relative_to(REPO_ROOT)}`. "
        "Use the attached context file for the traceback and rerun the scraper until it exits successfully."
    )
    context_file_path = None

    repair_context = f"""
Scraper: {script_path.relative_to(REPO_ROOT)}
Run command: {sys.executable} {script_path.relative_to(REPO_ROOT)}

Requirements:
- Fix only what is needed for this scraper to run correctly.
- Preserve the existing scraper behavior and output schema.
- Keep changes focused; avoid unrelated edits.
- Re-run the scraper after your fix and stop only when it exits successfully.

Captured stderr:
```
{stderr_output}
```

Captured stdout:
```
{stdout_output}
```
""".strip()

    try:
        log(f"Starting OpenCode repair for {script_path.name}...")

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix="_opencode_repair_context.md",
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
        log(f"OpenCode repair timed out for {script_path.name}.")
        return False
    finally:
        if context_file_path and os.path.exists(context_file_path):
            os.unlink(context_file_path)

    if action.returncode != 0:
        opencode_error = truncate_output(action.stderr or action.stdout)
        log(f"OpenCode could not repair {script_path.name}.")
        log(opencode_error)
        return False

    log(f"OpenCode repair finished for {script_path.name}.")
    return True


def test_scraper_repair(scraper_name):
    try:
        script_path = get_script_path(scraper_name)
    except (FileNotFoundError, ValueError) as error:
        log(error)
        return False

    existing_files = snapshot_sibling_files(script_path)
    log(f"Starting scraper {script_path.name}...")
    action = run_scraper(script_path)
    cleanup_created_sibling_files(script_path, existing_files)

    if action.returncode == 0:
        log(f"Scraper {script_path.name} already works.")
        return True

    log(f"Error scraping {script_path.name}")
    log(truncate_output(action.stderr))

    if not repair_scraper_with_opencode(script_path, action):
        return False

    existing_files = snapshot_sibling_files(script_path)
    log(f"Re-running scraper after auto-repair {script_path.name}...")
    repaired_action = run_scraper(script_path)
    cleanup_created_sibling_files(script_path, existing_files)

    if repaired_action.returncode == 0:
        log(f"Success scraping after auto-repair {script_path.name}")
        return True

    log(f"Auto-repair did not fix {script_path.name}")
    log(truncate_output(repaired_action.stderr))
    return False


def main():
    log_empty_jobs_cache()
    log("")

    for site in sorted(os.listdir(SITES_DIR)):
        if not site.endswith(".py") or site in EXCLUDE:
            continue
        
        script_path = SITES_DIR / site
        existing_files = snapshot_sibling_files(script_path)
        log(f"Starting scraper {site}...")
        action = run_scraper(script_path)
        cleanup_created_sibling_files(script_path, existing_files)

        if action.returncode == 0:
            log("Success scraping " + site)
            log_scraper_empty_result(script_path, action)
            continue

        log("Error scraping " + site)
        log(truncate_output(action.stderr))

        if not repair_scraper_with_opencode(script_path, action):
            continue

        existing_files = snapshot_sibling_files(script_path)
        log(f"Re-running scraper after auto-repair {site}...")
        repaired_action = run_scraper(script_path)
        cleanup_created_sibling_files(script_path, existing_files)

        if repaired_action.returncode == 0:
            log("Success scraping after auto-repair " + site)
        else:
            log("Auto-repair did not fix " + site)
            log(truncate_output(repaired_action.stderr))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_scraper_repair(sys.argv[1])
    else:
        main()
