from scraper_peviitor import Scraper, Rules
from utils import translate_city, acurate_city_and_county, publish, publish_logo, show_jobs
from getCounty import get_county, remove_diacritics

url = "https://veoneerro.teamtailor.com/jobs"

company = {"company": "Veoneer"}
finalJobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTag("div", {"class": "mx-auto text-lg block-max-w--lg"}).find_all(
    "li", {"class": "w-full"}
)

for job in jobs:
    job_title = job.find("span", {"class": "company-link-style"}).text.strip()
    job_link = job.find("a").get("href")
    acurate_city = acurate_city_and_county(Iasi={"city": "Iasi", "county": "Iasi"})
    cities = [
        remove_diacritics(city.strip())
        for city in job.find("div", {"class": "mt-1 text-md"})
        .find_all("span")[2]
        .text.split(",")
    ]
    counties = [
        (
            acurate_city.get(city.strip()).get("county")
            if acurate_city.get(city.strip())
            else get_county(translate_city(city.strip()))
        )
        for city in cities
    ]

    finalJobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "country": "Romania",
            "city": cities,
            "county": counties,
            "company": company.get("company"),
        }
    )

publish(4, company.get("company"), finalJobs, "APIKEY")

logoUrl = "https://seekvectorlogo.com/wp-content/uploads/2020/02/veoneer-inc-vector-logo-small.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
