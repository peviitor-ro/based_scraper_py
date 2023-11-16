from scraper_peviitor import Scraper, Rules, loadingData
import json
from utils import (translate_city)
from getCounty import get_county

url = "https://www.wtb.ro/wp-admin/admin-ajax.php"

company = {"company": "WTB"}
finalJobs = set()

data = {
    "action": "post_mypagination",
    "postoffset": 0,
    "dataType": "html",
}

scraper = Scraper()
rules = Rules(scraper)

while True:
    html = scraper.session.post(url, data=data)
    scraper.soup = html.text

    jobs = rules.getTags("div", {"class": "row mycontet"})

    if len(jobs) > 0:
        for job in jobs:
            job_title = job.find("h3").text.strip()
            job_link = job.find("a").get("href")
            city = translate_city(job.findAll("span", {"class": "mysort"})[
                                  0].text.split(",")[0])
            county = get_county(city)

            finalJobs.add((
                job_title,
                job_link,
                company["company"],
                "Romania",
                city,
                county
            ))
        data["postoffset"] += 1
    else:
        break

jobs = list()
for job in finalJobs:
    job_title = job[0]
    job_link = job[1]
    city = job[4]
    county = job[5]

    jobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city,
        "county": county,
    })

print(json.dumps(jobs, indent=4))

loadingData(jobs, company.get("company"))

logoUrl = "https://www.wtb.ro/wp-content/uploads/2018/04/logoblack.svg"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post("https://api.peviitor.ro/v1/logo/add/", json.dumps([
    {
        "id": company.get("company"),
        "logo": logoUrl
    }
]))
