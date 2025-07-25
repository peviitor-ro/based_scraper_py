from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs

url = "https://tremend.com/careers/"
company = "tremend"

scraper = Scraper()
scraper.get_from_url(url, "HTML")

final_jobs = []
job_elements = scraper.find_all(
    "article", class_="career__job-card")

print(f"Found {len(job_elements)} jobs on {company} careers page.")

for job in job_elements:
    job_title = job.find("h3").text.strip()
    job_link =  job.find("a")["href"]

    final_jobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "country": "Romania",
            "company": company,
            "city": "Bucuresti",
            "county": "Bucuresti",
        }
    )

publish_or_update(final_jobs)

publish_logo(
    company,
    "https://www.drupal.org/files/styles/grid-4-2x/public/logo%20Tremend%20480%20x480.png",
)

show_jobs(final_jobs)
