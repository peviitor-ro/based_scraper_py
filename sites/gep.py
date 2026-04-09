import re
from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs

company = "GEP"
url = "https://jobseurope-gep.icims.com/jobs/search?ss=1&in_iframe=1"

scraper = Scraper()
scraper.render_page(url)

content = str(scraper)
job_pattern = r'href="(https://jobseurope-gep\.icims\.com/jobs/\d+/[^"]+)"[^>]*>([^<]+)'
matches = re.findall(job_pattern, content)

jobs = [
    create_job(
        job_title=re.sub(r'\s+', ' ', title).strip(),
        job_link=href,
        city="Cluj-Napoca",
        county="Cluj",
        country="Romania",
        company=company,
    )
    for href, title in matches
]

publish_or_update(jobs)
publish_logo(
    company,
    "https://gep.icims.com/icims2/servlet/icims2?module=AppInert&action=download&id=96578&hashed=855987836",
)
show_jobs(jobs)
