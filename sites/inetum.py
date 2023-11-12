from scraper_peviitor import Scraper, Rules, loadingData
import json
from getCounty import get_county
from utils import translate_city, acurate_city_and_county

url = "https://www.inetum.com/en/jobs?f%5B0%5D=region%3A1068"

company = {"company": "Inetum"}
finalJobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

totalJobs = int(rules.getTag("li", {"id": "1068"}).find("span", {"class":"facet-item__count"}).text.replace("(", "").replace(")", "").strip())

paginations = [*range(1, totalJobs, 9)]

for page in range(len(paginations)):
    scraper.url = "https://www.inetum.com/en/jobs?f%5B0%5D=region%3A1068&page=" + str(page)
    rules = Rules(scraper)

    jobs = rules.getTags("div", {"class": "node node-job node-teaser"})

    for job in jobs:
        job_title = job.find("h3", {"class":"card-title"}).text.strip()
        job_link = "https://www.inetum.com" + job.find("a").get("href")
        city = translate_city(job.find("p", {"class": "card-text"}).text.split("-")[-1].split("/")[0].strip())
        county = get_county(city)
        remote = []

        jobs_types = ["Remote", "Hybrid"]


        for types in jobs_types:
            if types in job.find("p", {"class": "card-text"}).text.split("-")[-1].strip():
                remote.append(types) 

        finalJobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county,
            "remote": remote,
        })

print(json.dumps(finalJobs, indent=4))

# loadingData(finalJobs, company.get("company"))

# logoUrl = "https://vtlogo.com/wp-content/uploads/2021/05/inetum-vector-logo-small.png"

# scraper.session.headers.update({
#     "Content-Type": "application/json",
# })
# scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
#     {
#         "id":company.get("company"),
#         "logo":logoUrl
#     }
# ]))