from scraper_peviitor import Scraper, Rules, loadingData
from getCounty import get_county, remove_diacritics
import json

url = "https://www.autonom.ro/cariere"

scraper = Scraper(url)
rules = Rules(scraper)

# Obtinem toate joburile
jobs = rules.getTags('a', {'class': 'box-listing-job'})

company = {"company": "Autonom"}
finalJobs = list()

acurate_city = {
    "Iasi": {
        "city": "Iasi",
        "county": "Iasi"
    }
}

# Pentru fiecare job, extragem datele si le adaugam in lista finalJobs
for job in jobs:
    job_title = job.find('p', {"class": "nume-listing-job"}).text
    job_link = job['href']

    locations = job.find_all('span', {"class": "locatie-job"})
    cities = [remove_diacritics(city.text) for city in locations]
    counties = [
        city for city in cities if acurate_city.get(city) or get_county(city)
    ]

    finalJobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": cities,
        "county": counties,
    })

# Afisam numarul de joburi
print(json.dumps(finalJobs, indent=4))

# Incarcam datele in baza de date
loadingData(finalJobs, company.get("company"))
