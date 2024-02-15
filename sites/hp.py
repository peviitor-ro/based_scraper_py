from scraper_peviitor import Scraper
from utils import publish, publish_logo, show_jobs, translate_city
from getCounty import get_county
import json
import re


regex = re.compile(r"jobsCallback\((.*)\)")

apiUrl = "https://jobsapi-internal.m-cloud.io/api/job?callback=jobsCallback&facet%5B%5D=business_unit%3ARomania&sortfield=title&sortorder=ascending&Limit=100&Organization=2292&offset=1&useBooleanKeywordSearch=true"
scraper = Scraper(apiUrl)

jobs = json.loads(regex.search(scraper.soup.text).group(1)).get("queryResult")

company = {"company": "HP"}
finalJobs = list()

for job in jobs:
    job_title = job.get("title")
    job_link = job.get("url")
    city = translate_city(job.get("primary_city"))
    county = get_county(city)

    if "https://jobs.hp.com/" not in job_link:
        job_link = "https://jobs.hp.com/jobdetails/" + str(job.get("id"))

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

publish(4, company.get("company"), finalJobs, "APIKEY")

logourl = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/HP_logo_2012.svg/100px-HP_logo_2012.svg.png"
publish_logo(company.get("company"), logourl)

show_jobs(finalJobs)
