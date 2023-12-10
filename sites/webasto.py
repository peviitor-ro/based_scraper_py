from scraper_peviitor import Scraper, Rules, loadingData
import json
from utils import translate_city
from getCounty import get_county

url = "https://jobs.webasto.com/search/?createNewAlert=false&q=&optionsFacetsDD_country=RO&optionsFacetsDD_location=&optionsFacetsDD_dept=&optionsFacetsDD_shifttype="

company = {"company": "Webasto"}
finaljobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTag("table", {"id": "searchresults"}).find(
    "tbody").find_all("tr")

for job in jobs:
    job_title = job.find("a").text.strip()
    job_link = "https://jobs.webasto.com" + job.find("a").get("href")
    city = translate_city(
        job.find("span", {"class": "jobLocation"}).text.split(",")[0].strip()
    )
    county = get_county(city)
    
    finaljobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city,
        "county": county,
    })

print(json.dumps(finaljobs, indent=4))

loadingData(finaljobs, company.get("company"))

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/8/81/Webasto_20xx_logo.svg"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post("https://api.peviitor.ro/v1/logo/add/", json.dumps([
    {
        "id": company.get("company"),
        "logo": logoUrl
    }
]))
