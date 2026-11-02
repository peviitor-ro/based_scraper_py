import requests
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()

url = "https://boards-api.greenhouse.io/v1/boards/scbitdefendersrl/jobs?content=true"
company = {"company": "Bitdefender"}
logo = "https://www.bitdefender.com/adobe/dynamicmedia/deliver/dm-aid--ff62d212-3a6d-4993-841c-7458d12cdf2f/bitdefender-blue-logo-png.webp?preferwebp=true&quality=50"

response = requests.get(url, timeout=30)
data = response.json()

final_jobs = []

for job in data.get("jobs", []):
    location = job.get("location", {}).get("name", "").strip()
    loc_lower = location.lower()

    # Filter: keep only Romania-based jobs (Bucharest, RO, or Romania)
    is_romania = (
        "romania" in loc_lower
        or "bucurești" in loc_lower
        or "bucuresti" in loc_lower
        or "bucharest" in loc_lower
        or loc_lower == "ro"
        or loc_lower.endswith(", ro")
    )
    if not is_romania:
        continue

    job_title = job.get("title", "")
    job_link = job.get("absolute_url", "")

    city = ""
    if location and loc_lower not in ("romania", "ro"):
        city_part = location.split(",")[0].strip().replace("(HQ)", "").strip()
        city = translate_city(city_part)

    county = _counties.get_county(city) if city else ""

    remote = ""
    for meta in job.get("metadata", []):
        if meta.get("name") == "Work Type":
            raw_remote = meta.get("value", "") or ""
            val = raw_remote.lower().strip()
            if "hybrid" in val:
                remote = "hybrid"
            elif "remote" in val:
                remote = "remote"
            elif "on-site" in val or "onsite" in val:
                remote = "on-site"
            else:
                remote = ""
            break

    final_jobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city,
        "county": county,
        "remote": remote,
    })

publish_or_update(final_jobs)
publish_logo(company.get("company"), logo)
show_jobs(final_jobs)
