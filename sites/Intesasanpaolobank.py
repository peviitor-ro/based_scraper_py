from scraper_peviitor import Scraper, Rules, loadingData
import json
from getCounty import get_county, remove_diacritics

url = "https://www.intesasanpaolobank.ro/en/persoane-fizice/Our-World/cariere.html"

company = {"company": "IntesaSanpaoloBank"}
finalJobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTags("article", {"class": "careersItem"})

for job in jobs:
    job_title = job.find("h2").text.strip()
    job_link = "https://www.intesasanpaolobank.ro" + job.find("a").get("href")
    locations = job.find("p").text.split("/")

    remote = ["Remote" for location in locations if "remote" in location.lower()]

    cities = [remove_diacritics(location.strip())
              for location in locations if get_county(location.strip())]
    counties = [get_county(cities) for cities in cities]

    finalJobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": cities,
        "county": counties,
        "remote": remote
    })

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))

logoUrl = "https://www.epromsystem.com/wp-content/uploads/2021/09/Clienti-INTESASP-epromsystem.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post("https://api.peviitor.ro/v1/logo/add/", json.dumps([
    {
        "id": company.get("company"),
        "logo": logoUrl
    }
]))
