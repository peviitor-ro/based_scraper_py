from scraper_peviitor import Scraper, Rules
from utils import (
    translate_city,
    acurate_city_and_county,
    publish,
    publish_logo,
    show_jobs,
)
from getCounty import get_county, remove_diacritics

scraper = Scraper()
rules = Rules(scraper)

jobsFound = True
startRow = 0

company = {"company": "Heineken"}
finalJobs = list()

acurate_city = acurate_city_and_county(
    Mures={"city": "Satu Mare", "county": "Satu Mare"},
    Ciuc={"city": "Miercurea Ciuc", "county": "Harghita"},
)

while jobsFound:
    scraper.url = f"https://careers.theheinekencompany.com/search/?createNewAlert=false&q=&locationsearch=Romania&startrow={startRow}"
    jobs = rules.getTags("tr", {"class": "data-row"})
    for job in jobs:
        if (
            job.find("span", {"class": "jobLocation"}).text.split(",")[1].strip()
            != "RO"
        ):
            jobsFound = False
            break

        job_title = job.find("span", {"class": "jobTitle"}).text.strip()
        job_link = "https://careers.theheinekencompany.com" + job.find(
            "a", {"class": "jobTitle-link"}
        ).get("href")
        city = translate_city(
            remove_diacritics(
                job.find("span", {"class": "jobLocation"}).text.split(",")[0].strip()
            )
        )

        job = {
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
        }

        if acurate_city.get(city):
            job["city"] = acurate_city.get(city).get("city")
            job["county"] = acurate_city.get(city).get("county")
        else:
            job["city"] = city
            job["county"] = get_county(city)

        finalJobs.append(job)

    startRow += 25

publish(4, company.get("company"), finalJobs, "APIKEY")

logoUrl = "https://agegate.theheinekencompany.com/assets/img/logo-corporate.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
