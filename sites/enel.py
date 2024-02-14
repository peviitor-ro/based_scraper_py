from scraper.Scraper import Scraper
from utils import publish, publish_logo, show_jobs, translate_city
from getCounty import get_county

def get_aditional_city(url):
    scraper = Scraper()
    scraper.get_from_url(url, "JSON")
    html = scraper.markup.get("data").get("job").get("jobDescription")
    scraper.__init__(html, "html.parser")
    paragraphs = scraper.find_all("p")
    location = [
        paragraph.text if "📍" in paragraph.text else None for paragraph in paragraphs
    ]
    city = [loc.replace("📍:", "").strip() for loc in location if loc is not None][0]
    return city

scraper = Scraper()
url = "https://mingle.ro/api/boards/mingle/jobs?q=companyUid~eq~%22enel%22&page=0&pageSize=30&sort=modifiedDate~DESC"

scraper.get_from_url(url, "JSON")

company = {"company": "Enel"}
finaljobs = list()

jobs = scraper.markup.get("data").get("results")

for job in jobs:
    job_title = job.get("jobTitle")
    job_link = f"https://enel.mingle.ro/en/apply/{job.get('publicUid')}"
    locations = job.get("locations")

    city = []

    if not locations:
        city = city + translate_city(
            get_aditional_city(
                f"https://mingle.ro/api/open-positions/{job.get('publicUid')}/apply"
            )
        ).split(",")
    else:
        for location in locations:
            city.append(translate_city(location.get("name")))

    county = [get_county(city) for city in city]

    finaljobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county,
        }
    )

publish(4, company.get("company"), finaljobs, "APIKEY")

logoUrl = "https://www.enel.com/etc.clientlibs/enel-common/clientlibs/clientlib-bundle/resources/img/logo/logo.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)
