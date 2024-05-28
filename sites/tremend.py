from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, get_jobtype

url = "https://tremend.com/careers/"
company = "tremend"

scraper = Scraper()
scraper.get_from_url(url, "HTML")

final_jobs = []
job_elements = scraper.find("div", id="jobs").find_all("div", class_="career-wrapper")

for job in job_elements:
    job_title = job.find("h3").text.strip()
    job_link = "https://tremend.com/careers/" + job.find("a")["href"].strip("/")
    remote = get_jobtype(job.find("p", id="location-word").text.strip())

    if (
        "Bucharest" in job.find("p", id="location-word").text
        or "Romania" in job.find("p", id="location-word").text
    ):

        final_jobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "country": "Romania",
                "company": company,
                "remote": remote,
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
