from scraper.Scraper import Scraper
from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty

_counties = GetCounty()
url = "https://erstegroup-careers.com/bcr/search/?createNewAlert=false&q=&locations"
scraper = Scraper()
scraper.get_from_url(url)

elements = scraper.find_all("tr", {"class": "data-row"})

company = {"company": "BCR"}
finalJobs = list()

for element in elements:
    job_title = element.find("a", {"class": "jobTitle-link"}).text
    job_link = (
        "https://erstegroup-careers.com"
        + element.find("a", {"class": "jobTitle-link"})["href"]
    )
    city = translate_city(element.find("span", {"class": "jobShifttype"}).text)
    county = _counties.get_county(city)

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

publish_or_update(finalJobs)

logoUrl = "https://rmkcdn.successfactors.com/d1204926/7da4385b-5dfa-431c-9772-9.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
