from scraper_peviitor import Scraper, Rules, loadingData
import json
from utils import (translate_city, acurate_city_and_county,)
from getCounty import (get_county, remove_diacritics)

# Folosim ScraperSelenium deoarece numarul de joburi este incarcat prin AJAX
scraper = Scraper(
    "https://careers.eon.com/romania/go/Toate-joburile-din-Romania/3727401?utm_source=pagina-cariere-ro")
rules = Rules(scraper)

# Luam numarul total de joburi
jobs = rules.getTag("span", {"class": "paginationLabel"}).find_all("b")[1]
step = 25

# Calculam numarul de pagini
totalJobs = [*range(0, int(jobs.text), step)]

company = {"company": "Eon"}
finalJobs = list()

acurate_city = acurate_city_and_county(
    Iasi={"city": "Iasi", "county": "Iasi"},
    Targu_Mures={"city": "Targu-Mures", "county": "Mures"}
)

# Pentru fiecare pagina, luam joburile si le adaugam in lista finalJobs
for page in totalJobs:
    pageurl = f"https://careers.eon.com/romania/go/Toate-joburile-din-Romania/3727401/{page}/?q=&sortColumn=referencedate&sortDirection=desc"
    pageScaper = Scraper(pageurl)
    rules = Rules(pageScaper)

    jobs = rules.getTags("tr", {"class": "data-row"})

    for job in jobs:
        job_title = job.find("a").text
        job_link = "https://careers.eon.com" + job.find("a")["href"]
        city = translate_city(
            remove_diacritics(
                job.find("span", {"class": "jobLocation"}
                         ).text.split(",")[0].strip()
            )
        )

        job = {
            "job_title": job_title,
            "job_link": job_link,
            "country": "Romania",
            "company": company.get("company"),
        }

        if acurate_city.get(city.replace(" ", "_")):
            county = acurate_city.get(city.replace(" ", "_")).get("county")
            city = acurate_city.get(city.replace(" ", "_")).get("city")

            job["city"] = city
            job["county"] = county

        elif "Remote" in city:
            job["remote"] = ["Remote"]
            job["city"] = ""
            job["county"] = ""

        else:
            county = get_county(city)
            if not county:
                county = get_county(city.replace(" ", "-"))
            job["city"] = city
            job["county"] = county

        finalJobs.append(job)

# Afisam numarul de joburi extrase
print(json.dumps(finalJobs, indent=4))

# Incarcam joburile in baza de date
loadingData(finalJobs, company.get("company"))
