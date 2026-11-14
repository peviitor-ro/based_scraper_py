from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city, get_jobtype
from getCounty import GetCounty

url = "https://www.ionos-group.com/jobs-career/job-search.html?locationName=Bucharest"
company = {"company": "ionosgroup"}

scraper = Scraper()
scraper.get_from_url(url)
jobs_elements = scraper.find_all("a", class_="joboffer-list-job")


finalJobs = [
    {
        "job_title": job.find("h4").text.strip(),
        "job_link": "https://www.ionos-group.com" + job["href"],
        "city": "Bucuresti",
        "county": ["Bucuresti"],
        "remote": get_jobtype(job.find("h4").text.strip()),
        "company": company.get("company"),
        "country": "Romania",
    }
    for job in jobs_elements
]

try:
    publish_or_update(finalJobs)
except Exception as e:
    print(f"Failed to publish jobs: {e}")

logoUrl = "https://www.ionos-group.com/_assets/debf05b51933fca5f1c347f2aabc0cf0/Media/ionos-group.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
