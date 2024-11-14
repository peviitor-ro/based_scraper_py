from utils import publish_or_update, publish_logo, show_jobs, translate_city, acurate_city_and_county
from getCounty import GetCounty, remove_diacritics
from scraper.Scraper import Scraper

_counties = GetCounty()
acurete_city = acurate_city_and_county(
    Ilfov={
        "city": "Otopeni",
    }
)

url = "https://www.ejobs.ro/company/skilld-by-ejobs/317733"
company = "SKILLD"

scraper = Scraper()
scraper.get_from_url(url)

job_elements = scraper.find("main", class_="CDInner__Main").find_all(
    "div", class_="JobCard"
)

final_jobs = []

for job in job_elements:
    job_title = job.find("h2", class_="JCContentMiddle__Title").text.strip()
    job_url = job.find("h2", class_="JCContentMiddle__Title").find("a")["href"]
    job_url = "https://www.ejobs.ro" + job_url


    final_jobs.append(
        {
            "job_title": job_title,
            "job_link": job_url,
            "country": "Romania",
            "company": company,
        }
    )

publish_or_update(final_jobs)

publish_logo(company, "https://content.ejobs.ro/img/logos/3/317733.png")
show_jobs(final_jobs)
