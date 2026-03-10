import requests
from utils import show_jobs, translate_city, publish_or_update, publish_logo
from getCounty import GetCounty

_counties = GetCounty()
apiUrl = "https://uipath.com/api/getjobs"

response = requests.get(apiUrl).json()

company = "UiPath"
finalJobs = list()

romania_keywords = ["Romania", "Bucharest", "Cluj", "Timisoara", "Iasi", "Sibiu"]

for job in response:
    location = job.get("locationName", "")
    if not any(kw.lower() in location.lower() for kw in romania_keywords):
        continue

    job_title = job.get("title")
    job_link = job.get("externalLink")
    city = translate_city(location)
    county = _counties.get_county(city) or []

    remote = []
    location_type = job.get("locationType", "")
    if location_type == "Remote":
        remote.append("Remote")
    elif location_type == "Hybrid":
        remote.append("Hybrid")

    finalJobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": "Romania",
            "city": city,
            "county": county,
            "remote": remote,
        }
    )

publish_or_update(finalJobs)

publish_logo(
    company,
    "https://cms.jibecdn.com/prod/uipath/assets/HEADER-NAV_LOGO-en-us-1663079214804.svg",
)
show_jobs(finalJobs)
