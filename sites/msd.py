from scraper_peviitor import Scraper, loadingData
import json
import re
from utils import (translate_city)
from getCounty import get_county

url = " https://jobs.msd.com/gb/en/search-results?qcountry=Romania"  # &from=10

company = {"company": "MSD"}
finalJobs = list()

scraper = Scraper()
response = scraper.session.get(url)

pattern = re.compile(r"phApp.ddo = {(.*?)};", re.DOTALL)

data = re.search(pattern, response.text).group(1)
totalJobs = json.loads(
    "{" + data + "}").get("eagerLoadRefineSearch").get("totalHits")

querys = [*range(0, totalJobs, 10)]

for query in querys:
    url = "https://jobs.msd.com/gb/en/search-results?qcountry=Romania&from=" + \
        str(query)
    response = scraper.session.get(url)
    data = re.search(pattern, response.text).group(1)
    jobs = json.loads(
        "{" + data + "}").get("eagerLoadRefineSearch").get("data").get("jobs")

    for job in jobs:
        job_title = job.get("title")
        job_link = "https://jobs.msd.com/gb/en/job/" + job.get("jobId")
        city = translate_city(job.get("city"))
        county = get_county(city)
        remote = []

        if not county:
            finalJobs.append({
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "remote": "Remote",
            })
        else:
            finalJobs.append({
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
                "county": county,
            })

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))

logoUrl = "https://www.msdmanuals.com/Content/Images/msd_foot_logo.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))
