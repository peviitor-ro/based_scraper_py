from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty, remove_diacritics

_counties = GetCounty()
company = "Segula"
jobs = []

url = "https://careers.segulatechnologies.com/wp/wp-admin/admin-ajax.php"

payload = {
    "action": "sgl_jobs_ajax",
    "" "limit": 100,
    "location": "Romania",
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}

scraper = Scraper()
scraper.set_headers(headers)
response = scraper.post(url, data=payload)

for job in response.json()["data"]["jobs"]:
    city = translate_city(remove_diacritics(job["city"]))
    county = _counties.get_county(city)
    jobs.append(
        create_job(
            company=company,
            job_title=job["title"],
            job_link=job["link"],
            city=city,
            county=county,
            country="Romania",
        )
    )

publish_or_update(jobs)
publish_logo(
    company,
    "https://careers.segulatechnologies.com/app/themes/segula/library/medias/images/logo-blue.png",
)
show_jobs(jobs)
