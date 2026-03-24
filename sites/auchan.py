from utils import create_job, publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty, remove_diacritics
import requests


_counties = GetCounty()

company = "Auchan"
url = "https://cariere.auchan.ro/joburi"

ALGOLIA_URL = "https://UM59DWRPA1-dsn.algolia.net/1/indexes/*/queries"
ALGOLIA_HEADERS = {
    "x-algolia-application-id": "UM59DWRPA1",
    "x-algolia-api-key": "33719eb8d9f28725f375583b7e78dbab",
    "Content-Type": "application/json",
}
ALGOLIA_PAYLOAD = {
    "requests": [
        {
            "indexName": "production_Auchan_jobs",
            "params": "hitsPerPage=1000&page=0",
        }
    ]
}

CITY_OVERRIDES = {
    "Iasi": {"city": "Iasi", "county": ["Iasi"]},
    "Galati": {"city": "Galati", "county": ["Galati"]},
    "Ilfov": {"city": "Stefanestii de Jos", "county": ["Ilfov"]},
    "Satu Mare": {"city": "Satu Mare", "county": ["Satu Mare"]},
    "Stefanestii_de_Jos": {"city": "Stefanestii de Jos", "county": ["Ilfov"]},
    "Stefanestii de Jos": {"city": "Stefanestii de Jos", "county": ["Ilfov"]},
    "Cluj": {"city": "Cluj-Napoca", "county": ["Cluj"]},
    "Targu_Mures": {"city": "Targu-Mures", "county": ["Mures"]},
}


def normalize_city(city):
    city = remove_diacritics((city or "").strip())
    city = translate_city(city) or ""
    city = " ".join(city.split())

    if city in CITY_OVERRIDES:
        return CITY_OVERRIDES[city]["city"], CITY_OVERRIDES[city]["county"]

    county = _counties.get_county(city)
    return city, county


response = requests.post(
    ALGOLIA_URL,
    headers=ALGOLIA_HEADERS,
    json=ALGOLIA_PAYLOAD,
    timeout=20,
).json()

jobs_elements = response.get("results", [{}])[0].get("hits", [])
jobs = []

for job in jobs_elements:
    city_value = (job.get("oras") or [""])[0]
    city, county = normalize_city(city_value)

    jobs.append(
        create_job(
            job_title=job.get("title"),
            job_link=f"https://cariere.auchan.ro/job/{(job.get('url_slug') or [''])[0]}",
            company=company,
            country="Romania",
            city=city,
            county=county,
        )
    )

publish_or_update(jobs)
publish_logo(
    company,
    "https://res.cloudinary.com/smartdreamers/image/upload/v1685443347/company_logos/82780f0401d4b4b2097c8f79d13fa468.svg",
)
show_jobs(jobs)
