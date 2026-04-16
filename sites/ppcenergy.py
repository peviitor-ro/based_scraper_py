import requests
import re
from utils import publish_or_update, publish_logo, show_jobs, translate_city, create_job
from getCounty import GetCounty


_counties = GetCounty()
company = {"company": "PPCEnergy"}
embed_url = "https://ppc.jobful.io/jobs/embed?company%5B%5D=1"
jobs_url = "https://ppc.jobful.io/jobs/load"

session = requests.Session()
embed_html = session.get(embed_url, timeout=60).text
csrf_token = re.search(r'<meta name="csrf-token" content="([^"]+)"', embed_html).group(1)

headers = {
    "X-Requested-With": "XMLHttpRequest",
    "X-CSRF-TOKEN": csrf_token,
    "Referer": embed_url,
    "Accept": "application/json",
}

finaljobs = []
page = 1
last_page = 1

remote_map = {
    "hibrid": "hybrid",
    "remote": "remote",
    "la birou": "on-site",
    "on-site": "on-site",
}

while page <= last_page:
    response = session.get(
        jobs_url,
        params={"company[]": "1", "embed": "1", "page": page},
        headers=headers,
        timeout=60,
    ).json()["data"]

    jobs = response.get("jobs") or []
    last_page = (response.get("pagination") or {}).get("last") or 1

    for job in jobs:
        job_title = job.get("title")
        job_link = job.get("url")
        locations = job.get("city") or []

        cities = []
        counties = []

        for location in locations:
            city = translate_city(location.get("name") or "")
            if city == "Iasi":
                county = ["Iasi"]
            else:
                county = _counties.get_county(city) or []

            if city and city not in cities:
                cities.append(city)

            for item in county:
                if item not in counties:
                    counties.append(item)

        overview = job.get("overview") or {}
        presence = overview.get("Prezență") or overview.get("Prezenta") or []
        remote = []

        for item in presence:
            remote_name = (item.get("name") or "").strip().lower()
            mapped_value = remote_map.get(remote_name)
            if mapped_value and mapped_value not in remote:
                remote.append(mapped_value)

        finaljobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                company=company.get("company"),
                country="Romania",
                city=cities,
                county=counties,
                remote=remote,
            )
        )

    page += 1


publish_or_update(finaljobs)

logoUrl = "https://www.ppcenergy.ro/wp-content/uploads/logo.svg?w=1024"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)
