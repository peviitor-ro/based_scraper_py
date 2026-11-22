from scraper.Scraper import Scraper
from getCounty import GetCounty, remove_diacritics
from utils import publish_or_update, publish_logo, show_jobs, translate_city
import json


JOBS_URL = "https://intel.wd1.myworkdayjobs.com/wday/cxs/intel/External/jobs"
JOB_URL = "https://intel.wd1.myworkdayjobs.com/wday/cxs/intel/External"
JOB_PAGE_URL = "https://intel.wd1.myworkdayjobs.com/en-US/External"

headers = {"Content-Type": "application/json", "Accept": "application/json"}


def get_aditional_city(url):
    scraper = Scraper()
    scraper.get_from_url(url)

    locations = scraper.find(
        "span", {"class": "job-description__location-pin"}
    ).text.split("|")

    cities = []
    counties = []

    for location in locations:
        city = remove_diacritics(translate_city(
            location.split(",")[0].strip()))
        county = _counties.get_county(city)

        if county:
            cities.append(city)
            counties.extend(county)

    return cities, counties


def get_jobs_page(post_data):
    scraper = Scraper()
    scraper.set_headers(headers)
    try:
        return scraper.post(JOBS_URL, json.dumps(post_data)).json()
    except ValueError:
        return {}


def get_job_info(external_path):
    scraper = Scraper()
    for _ in range(5):
        try:
            scraper.get_from_url(JOB_URL + external_path, type="JSON")
            markup = scraper.markup
            info = markup.get("jobPostingInfo", {}) if isinstance(markup, dict) else {}
            if info:
                return info
        except (ValueError, OSError):
            continue
    return {}


def get_romania_facet(data):
    for facet in data.get("facets") or []:
        for group in facet.get("values") or []:
            for value in group.get("values") or []:
                if "Romania" in (value.get("descriptor") or ""):
                    return value.get("id")
    return None


def get_city(location):
    parts = [part.strip() for part in (location or "").split(",")]
    return parts[-1] if parts else ""


_counties = GetCounty()
company = "Intel"
finalJobs = list()

post_data = {
    "appliedFacets": {},
    "limit": 20,
    "offset": 0,
    "searchText": "",
}

data = get_jobs_page(post_data)
facet_id = get_romania_facet(data)
if facet_id:
    romania_data = get_jobs_page(dict(post_data, appliedFacets={"locations": [facet_id]}))
    if romania_data.get("jobPostings"):
        data = romania_data

jobs = data.get("jobPostings") or []

for job in jobs:
    external_path = job.get("externalPath") or ""
    info = get_job_info(external_path)
    if not info:
        continue

    location = info.get("location") or job.get("locationsText") or ""
    country = (info.get("country") or {}).get("descriptor")
    if not country:
        country = location.split(",")[0].strip() or "Romania"

    city = get_city(location)
    if country == "Romania":
        city = remove_diacritics(translate_city(city))
        counties = _counties.get_county(city)
    else:
        counties = []

    finalJobs.append(
        {
            "job_title": job.get("title"),
            "job_link": JOB_PAGE_URL + external_path,
            "company": company,
            "country": country,
            "city": city,
            "county": counties,
        }
    )


publish_or_update(finalJobs)

logoUrl = (
    "https://tbcdn.talentbrew.com/company/599/gst-v1_0/img/logo/logo-intel-blue.svg"
)
publish_logo(company, logoUrl)
show_jobs(finalJobs)
