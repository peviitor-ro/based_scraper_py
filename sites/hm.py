from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty, remove_diacritics

_counties = GetCounty()

url = "https://api.smartrecruiters.com/v1/companies/HMGroup/postings"
params = {"country": "ro", "limit": 100, "offset": 0}

scraper = Scraper()
scraper.get_from_url(url + "?country=ro&limit=100&offset=0", type="JSON")

company = {"company": "HM"}
finalJobs = list()

jobs = scraper.markup
while jobs.get("content"):
    for job in jobs.get("content"):
        job_title = job.get("name")
        job_link = f"https://jobs.smartrecruiters.com/HMGroup/{job.get('id')}"
        city = remove_diacritics(job.get("location", {}).get("city", ""))
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

    params["offset"] += params["limit"]
    if params["offset"] >= jobs.get("totalFound", 0):
        break
    scraper.get_from_url(
        f"{url}?country=ro&limit={params['limit']}&offset={params['offset']}",
        type="JSON",
    )
    jobs = scraper.markup

publish_or_update(finalJobs)

logourl = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/H%26M-Logo.svg/709px-H%26M-Logo.svg.png?20130107164928"
publish_logo(company.get("company"), logourl)

show_jobs(finalJobs)
