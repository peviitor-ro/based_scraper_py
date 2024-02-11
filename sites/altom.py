from scraper.Scraper import Scraper
from utils import show_jobs, translate_city, publish, publish_logo
from getCounty import get_county

company = "altom"

url = "https://www.altom.com/jobs/"

scraper = Scraper()
scraper.get_from_url(url)
jobs = scraper.find_all("article", class_="job")

final_jobs = [
    {
        "job_title": job.find("h2", class_="job-title").text.strip(),
        "job_link": job.find("h2", class_="job-title").find("a").get("href"),
        "city": translate_city(job.find("p", class_="job-feed-meta").text.strip()),
        "county": get_county(
            translate_city(job.find("p", class_="job-feed-meta").text.strip())
        ),
        "country": "Romania",
        "company": company,
    }
    for job in jobs
]

publish(4, "altom", final_jobs, "APIKEY")

publish_logo(
    "altom",
    "https://altom.com/app/themes/altom-sage-theme/dist/images/logo-altom_60516779.png",
)
show_jobs(final_jobs)
