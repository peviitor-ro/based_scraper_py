from scraper_peviitor import Scraper, loadingData, Rules
import json
from utils import (translate_city, acurate_city_and_county)
from getCounty import (get_county, remove_diacritics)

url = "https://veoneerro.teamtailor.com/jobs"

company = {"company": "Veoneer"}
finalJobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTag("div", {
                    "class": "mx-auto text-lg block-max-w--lg"}).find_all("li", {"class": "w-full"})

for job in jobs:
    job_title = job.find("span", {"class": "company-link-style"}).text.strip()
    job_link = job.find("a").get("href")
    acurate_city = acurate_city_and_county(
        Iasi={"city": "Iasi", "county": "Iasi"})
    cities = [remove_diacritics(city.strip()) for city in job.find(
        "div", {"class": "mt-1 text-md"}).find_all("span")[2].text.split(",")]
    counties = [acurate_city.get(city.strip()).get("county") if acurate_city.get(city.strip())else
                get_county(translate_city(city.strip())) for city in cities]

    finalJobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "country": "Romania",
        "city": cities,
        "county": counties,
        "company": company.get("company")
    })

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))

logoUrl = "https://seekvectorlogo.com/wp-content/uploads/2020/02/veoneer-inc-vector-logo-small.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))
