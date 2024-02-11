from scraper.Scraper import Scraper
from utils import publish, publish_logo, create_job, show_jobs, translate_city
from getCounty import get_county, remove_diacritics


def get_aditional_city(url):
    scraper = Scraper()
    scraper.get_from_url(url)

    locations = (
        scraper.find_all("div", {"class": "item-list"})[0]
        .find("div", {"class": "field-items"})
        .text.replace("-", ",")
        .replace(".", "")
        .split(",")
    )

    cities = []
    counties = []

    for location in locations:
        city = remove_diacritics(translate_city(location.strip()))
        county = get_county(city)

        if not county:
            city = translate_city(remove_diacritics(location.strip().replace(" ", "-")))
            county = get_county(city)

        cities.append(city)
        counties.append(county)

    return cities, counties


company = "Cat"
url = "https://www.bm-cat.com/ro-ro/articole/resurse-umane"

scraper = Scraper()
scraper.get_from_url(url)

jobs = []

jobs_elements = scraper.find("div", class_="three").find_all("li")

for job in jobs_elements:
    job_link = job.find("a")["href"]
    cities, counties = get_aditional_city(job_link)

    jobs.append(
        create_job(
            job_title=job.find("a").text,
            job_link=job_link,
            city=cities,
            county=counties,
            country="Romania",
            company=company,
        )
    )


publish(4, company, jobs, "APIKEY")

publish_logo(
    company, "https://www.bm-cat.com/ro-ro/sites/all/themes/custom/theme_brg/logo.png"
)
show_jobs(jobs)
