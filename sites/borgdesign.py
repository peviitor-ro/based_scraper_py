from scraper.Scraper import Scraper
from utils import (
    translate_city,
    acurate_city_and_county,
    publish_or_update,
    publish_logo,
    show_jobs,
)

url = "https://jobs.borgdesign.ro"
company = "Borg Design"

scraper = Scraper()
scraper.get_from_url(url, verify=False)

job_cards = scraper.find_all("li", {"class": "pos-card"})

final_jobs = []

acurate_city = acurate_city_and_county(
    Bucuresti={"city": "Bucuresti", "county": "Bucuresti"},
)

for job in job_cards:
    title_div = job.find("div", {"class": "title"})
    if not title_div:
        continue

    job_title = title_div.get_text(separator=" ", strip=True).replace("  ", " ")
    dept = job.find("div", {"class": "dept"})
    department = dept.get_text(strip=True) if dept else ""

    city = translate_city("bucharest")

    if acurate_city.get(city):
        county = acurate_city.get(city).get("county")
    else:
        county = "Bucuresti"

    final_jobs.append(
        {
            "job_title": job_title,
            "job_link": url,
            "company": company,
            "country": "Romania",
            "city": city,
            "county": county,
            "department": department,
        }
    )

publish_or_update(final_jobs)

publish_logo(
    company,
    "https://www.borgdesign.ro/img/logo/borg.png",
)

show_jobs(final_jobs)