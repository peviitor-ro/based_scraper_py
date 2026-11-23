import html
import re
import shutil
import subprocess
import tempfile
import time

from utils import publish_or_update, publish_logo, create_job, show_jobs

url = "https://www.fgaromania.ro/categorie/cariera/"

company = "fga"

browser = next(
    (
        path
        for name in ("google-chrome", "chromium", "chromium-browser")
        if (path := shutil.which(name))
    ),
    None,
)
if browser is None:
    raise RuntimeError("A Chrome/Chromium browser is required to load the FGA careers page")

content = ""
for attempt in range(10):
    with tempfile.TemporaryDirectory() as profile_dir:
        result = subprocess.run(
            [
                browser,
                "--headless=new",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "--virtual-time-budget=20000",
                f"--user-data-dir={profile_dir}",
                "--dump-dom",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=90,
        )
    if result.returncode == 0:
        content = result.stdout
        if "Just a moment" not in content:
            break
    time.sleep(1)
else:
    raise RuntimeError("Failed to load the FGA careers page")

pattern = re.compile(
    r'<h5\b[^>]*>\s*<a\b[^>]*href="(https://www\.fgaromania\.ro/anunt-[^"]+)"[^>]*>'
    r"(.*?)</a>\s*</h5>",
    re.S | re.I,
)

jobs = []
seen_links = set()
for link, title in pattern.findall(content):
    if link in seen_links:
        continue
    seen_links.add(link)
    job_title = html.unescape(re.sub(r"<[^>]+>", "", title)).strip()
    if not job_title or job_title == "Nu sunt poziții deschise în acest moment":
        continue
    jobs.append(
        create_job(
            job_title=job_title,
            job_link=link,
            company=company,
            country="Romania",
            city="Bucuresti",
            county="Bucuresti",
        )
    )

publish_or_update(jobs)

publish_logo(
    company, "https://www.fgaromania.ro/wp-content/uploads/2020/06/logo-FGA.png"
)
show_jobs(jobs)
