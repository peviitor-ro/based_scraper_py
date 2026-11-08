from scraper.Scraper import Scraper
from getCounty import GetCounty
from utils import (
    translate_city,
    acurate_city_and_county,
    publish_or_update,
    publish_logo,
    show_jobs,
)

url = "https://electrogrup.applytojob.com/apply/jobs/?department=Electrogrup"
company = "Electrogrup"

_counties = GetCounty()

scraper = Scraper()
scraper.get_from_url(url, verify=False)

job_rows = scraper.find_all(
    "tr",
    {"class": ["resumator_even_row", "resumator_odd_row"]},
)

final_jobs = []

acurate_city = acurate_city_and_county(
    Bucuresti={"city": "Bucuresti", "county": "Bucuresti"},
    Iasi={"city": "Iasi", "county": "Iasi"},
    Piatra_Neamt={"city": "Piatra-Neamt", "county": "Neamt"},
    Constanta={"city": "Constanta", "county": "Constanta"},
    Sibiu={"city": "Sibiu", "county": "Sibiu"},
)

for row in job_rows:
    link = row.find("a", {"class": "job_title_link"})
    if not link:
        continue

    job_title = link.get_text(strip=True)
    job_link = "https://electrogrup.applytojob.com" + link.get("href")
    location_text = row.find_all("td")[1].get_text(strip=True)

    city = location_text.split(",")[0].strip()
    city = translate_city(city.lower().title())

    if acurate_city.get(city):
        county = acurate_city.get(city).get("county")
    else:
        county = _counties.get_county(city)

    if isinstance(county, list):
        county = county[0] if county else None

    if not county:
        city = "Bucuresti"
        county = "Bucuresti"

    final_jobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": "Romania",
            "city": city,
            "county": county,
        }
    )

publish_or_update(final_jobs)

publish_logo(
    company,
    "https://electrogrup.ro/wp-content/uploads/2018/07/LGOELECTRO.jpg",
)

show_jobs(final_jobs)