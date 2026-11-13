import re

import requests
from utils import publish_or_update, publish_logo, create_job, show_jobs

url = "https://r.jina.ai/https://www.fgaromania.ro/categorie/cariera/"

company = "fga"

response = requests.get(url, timeout=30)
response.raise_for_status()
content = response.text

pattern = re.compile(
    r"##### \[(.+?)\]\((https://www\.fgaromania\.ro/anunt-[^)]+)\)"
)

jobs = []
seen_links = set()
for title, link in pattern.findall(content):
    if link in seen_links:
        continue
    seen_links.add(link)
    job_title = title.strip()
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
