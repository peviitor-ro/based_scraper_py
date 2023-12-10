# TODO: De verificat cand sunt joburi noi

from scraper_peviitor import Scraper, Rules, loadingData
import json
from utils import translate_city, acurate_city_and_county
from getCounty import get_county

# Cream o instanta de tip Scraper
scraper = Scraper(
    "https://cariere.romstal.ro/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_location=&optionsFacetsDD_department=")
rules = Rules(scraper)

# Luam toate joburile
jobs = rules.getTags('li', {'class': 'job-tile'})

company = {"company": "Romstal"}
finalJobs = list()

acurate_city = acurate_city_and_county(
    Iasi={
        "city": "Iasi",
        "county": "Iasi"
    }
)

# Pentru fiecare job luam titlul, linkul, compania, tara si orasul
for job in jobs:
    job_title = job.find('a', {"class": "jobTitle-link"}).text.strip()
    job_link = "https://cariere.romstal.ro" + \
        job.find('a', {"class": "jobTitle-link"})['href']
    city = job.find('div', {"class": "location"}).find(
        'div').text.split(',')[0].strip()

    if "SECTOR" in city:
        city = "Bucuresti"

    city = translate_city(city.title().replace(" - ", "-"))

    if acurate_city.get(city):
        county = acurate_city.get(city).get("county")
    else:
        county = get_county(city)

    finalJobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city,
        "county": county
    })

# Afisam numarul de joburi
print(json.dumps(finalJobs, indent=4))

# Incarcam datele in baza de date
loadingData(finalJobs, company.get("company"))
