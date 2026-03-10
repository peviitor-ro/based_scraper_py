from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty, remove_diacritics
import json

_counties = GetCounty()
data = {"locations": ["cou:ro"], "workAreas": [],
        "contractType": [], "fulltext": "", "order_by": "", "page": 1}

url = "https://career.hm.com/wp-json/hm/v1/sr/jobs/search?_locale=user"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://career.hm.com",
    "Referer": "https://career.hm.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin"
}

scraper = Scraper()
scraper.set_headers(headers)
jobs = scraper.post(url, data=json.dumps(data)).json()

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
    jobs = scraper.post(url, data=json.dumps(data)).json()

publish_or_update(finalJobs)

logourl = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/H%26M-Logo.svg/709px-H%26M-Logo.svg.png?20130107164928"
publish_logo(company.get("company"), logourl)

show_jobs(finalJobs)
