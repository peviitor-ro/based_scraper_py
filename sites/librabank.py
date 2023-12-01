from scraper_peviitor import Scraper, Rules, loadingData
import json
from utils import translate_city, acurate_city_and_county
from getCounty import get_county


def remove_words(text, words):
    for word in words:
        text = text.replace(word, "")
    return text


acurate_city = acurate_city_and_county(
    Iasi={
        "city": "Iasi",
        "county": "Iasi"
    }
)

url = "https://www.librabank.ro/Cariere"

scraper = Scraper(url)
rules = Rules(scraper)

jobContainer = rules.getTags("div", {"class": "jobListing"})
jobs = list(jobContainer)[0].find_all("div", {"class": "card-body"})

company = {"company": "LibraBank"}
finalJobs = list()

for job in jobs:
    job_title = job.find("a").text.strip()
    job_link = "https://www.librabank.ro" + job.find("a").get("href")

    location = remove_words(
        job_title.split(" - ")[-1].strip(), ["Sucursala", "Sucursale"]
    ).strip()

    if acurate_city.get(location):
        city = acurate_city.get(location).get("city")
        county = acurate_city.get(location).get("county")
    else:
        city = translate_city(location)
        county = get_county(city)

        if not county:
            city = "Bucuresti"
            county = "Bucuresti"

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
