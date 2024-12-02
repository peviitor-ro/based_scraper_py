from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()
url = " https://careers-ro.jdepeets.com/job-search/"

company = {"company": "Jacobsdouweegberts"}
finaljobs = list()

scraper = Scraper()
scraper.set_headers({"Accept-Language": "en-GB,en;q=0.9",})
scraper.get_from_url(url)

jobs = scraper.find_all("li", {"class": "app-smartRecruiterSearchResult-list__item"})

for job in jobs:
    job_title = job.find("span", {"class": "job-name"}).text.strip()
    job_link = "https://careers-ro.jacobsdouweegberts.com" + job.find("a").get("href")
    city = translate_city(job.find("span", {"class": "job-city"}).text.strip())
    county = _counties.get_county(city)

    finaljobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "country": "Romania",
            "city": city,
            "county": county,
            "company": company.get("company"),
        }
    )

publish_or_update(finaljobs)

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/JDE_Peet%27s_box_logo.svg/1024px-JDE_Peet%27s_box_logo.svg.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)
