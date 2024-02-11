from scraper_peviitor import Scraper, Rules
from utils import translate_city, publish, publish_logo, show_jobs
from getCounty import get_county, counties

# Cream o instanta a clasei Scraper
scraper = Scraper(
    "https://erstegroup-careers.com/bcr/search/?createNewAlert=false&q=&locations"
)
rules = Rules(scraper)

# Cautam elementele care contin joburile
elements = rules.getTags("tr", {"class": "data-row"})

company = {"company": "BCR"}
finalJobs = list()

# Iteram prin elementele gasite si extragem informatiile necesare
for element in elements:
    job_title = element.find("a", {"class": "jobTitle-link"}).text
    job_link = (
        "https://erstegroup-careers.com"
        + element.find("a", {"class": "jobTitle-link"})["href"]
    )
    city = translate_city(element.find("span", {"class": "jobShifttype"}).text)
    county = get_county(city)

    if not county:
        find_city = [c for c in counties if c.get(city)][0].get(city)[0]
        county = city
        city = find_city

    finalJobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county,
        }
    )

publish(4, company.get("company"), finalJobs, "APIKEY")

logoUrl = "https://rmkcdn.successfactors.com/d1204926/7da4385b-5dfa-431c-9772-9.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
