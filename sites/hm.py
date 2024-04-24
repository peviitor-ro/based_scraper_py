from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty, remove_diacritics

_counties = GetCounty() 
data = {
    "locations": [],
    "workAreas": [],
    "contractType": [],
    "fulltext": "Romania",
    "order_by": "relevance",
    "page": 1,
}
url = "https://career.hm.com/wp-json/hm/v1/sr/jobs/search?_locale=user"

scraper = Scraper()
jobs = scraper.post(url, data).json()

company = {"company": "HM"}
finalJobs = list()

while jobs.get("jobs"):
    for job in jobs.get("jobs"):
        job_title = job.get("title")
        job_link = job.get("permalink")
        city = remove_diacritics(job.get("city"))
        county = _counties.get_county(city)

        finalJobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
                "county": county,
            }
        )

    data["page"] += 1
    jobs = scraper.post(url, data).json()

publish_or_update(finalJobs)

logourl = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/H%26M-Logo.svg/709px-H%26M-Logo.svg.png?20130107164928"
publish_logo(company.get("company"), logourl)

show_jobs(finalJobs)
