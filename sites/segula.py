from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty, remove_diacritics
import requests
import urllib3

_counties = GetCounty()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
company = "Segula"
jobs = []

url = "https://careers.segulatechnologies.com/wp/wp-admin/admin-ajax.php"

payload = {
    "action": "sgl_jobs_ajax",
    "limit": 100,
    "location": "Romania",
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}

response = requests.post(url, data=payload, headers=headers, timeout=10, verify=False)

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
