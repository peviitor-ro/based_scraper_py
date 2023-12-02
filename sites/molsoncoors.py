from scraper_peviitor import Scraper, loadingData, Rules
import json
from utils import translate_city, acurate_city_and_county
from getCounty import get_county

url = "https://jobs.molsoncoors.com/MolsonCoors_GBSRomania/search/?q=Romania&startrow=1"

company = {"company": "MolsonCoors"}
finalJobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

totalJobs = int(rules.getTag(
    "span", {"class": "paginationLabel"}).find_all("b")[-1].text.strip())

paginate = [*range(0, totalJobs, 25)]

acurate_city = acurate_city_and_county(
    Alba={
        "city": "Alba Iulia",
        "county": "Alba"
    }
)

for page in paginate:
    url = f"https://jobs.molsoncoors.com/MolsonCoors_GBSRomania/search/?q=Romania&startrow={page}"
    scraper.url = url

    jobs = rules.getTag("table", {"id": "searchresults"}).find(
        "tbody").find_all("tr")

    for job in jobs:
        job_title = job.find("a").text.strip()
        job_link = "https://jobs.molsoncoors.com" + job.find("a").get("href")
        cities = []
        counties = []

        for city in job.find("span", {"class": "jobLocation"}).text.split(","):
            city = translate_city(city.strip())
            if acurate_city.get(city):
                cities.append(acurate_city.get(city).get("city"))
                counties.append(acurate_city.get(city).get("county"))
            elif get_county(city):
                cities.append(city)
                counties.append(get_county(city))
        if cities and counties:
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

logoUrl = "https://rmkcdn.successfactors.com/e2403c2e/b8073680-5e29-45a9-8c61-4.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))
