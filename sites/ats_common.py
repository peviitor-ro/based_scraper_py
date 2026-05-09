import html
import re

import requests

from getCounty import GetCounty, remove_diacritics
from utils import create_job, publish_logo, publish_or_update, show_jobs

_counties = GetCounty()

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
}

CITY_ALIASES = [
    ("bucharest", "Bucuresti"),
    ("bucuresti", "Bucuresti"),
    ("cluj-napoca", "Cluj-Napoca"),
    ("cluj", "Cluj-Napoca"),
    ("iasi", "Iasi"),
    ("timisoara", "Timisoara"),
    ("brasov", "Brasov"),
    ("sibiu", "Sibiu"),
    ("oradea", "Oradea"),
    ("ploiesti", "Ploiesti"),
    ("craiova", "Craiova"),
    ("jucu", "Jucu"),
]


def normalize_text(value):
    return remove_diacritics(str(value or "")).lower()


def html_to_text(value):
    plain_text = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", html.unescape(plain_text)).strip()


def join_values(values):
    return " ".join(normalize_text(value) for value in values if value)


def has_romania_signal(*values):
    text = join_values(values)
    if "romania" in text:
        return True
    return any(alias in text for alias, _ in CITY_ALIASES)


def infer_city(*values):
    text = join_values(values)
    for alias, city in CITY_ALIASES:
        if alias in text:
            return city
    return None


def infer_remote(*values):
    text = join_values(values)
    if "hybrid" in text:
        return ["hybrid"]
    if "remote" in text or "telecommute" in text or "work from home" in text:
        return ["remote"]
    return []


def build_job(company, title, link, location_signals, remote_signals=None):
    if not title or not link or not has_romania_signal(*location_signals):
        return None

    city = infer_city(*location_signals)
    county = _counties.get_county(city) or [] if city else []
    remote = infer_remote(*(remote_signals or []))

    return create_job(
        job_title=title.strip(),
        job_link=link,
        company=company,
        country="Romania",
        city=city if city else [],
        county=county,
        remote=remote,
    )


def finalize_jobs(company, logo_url, jobs):
    publish_or_update(jobs)
    publish_logo(company, logo_url)
    show_jobs(jobs)


def run_greenhouse(company, board_token, logo_url):
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true"
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()

    jobs = []
    seen_links = set()

    for job in response.json().get("jobs", []):
        job_link = job.get("absolute_url")
        if not job_link or job_link in seen_links:
            continue

        location_text = ((job.get("location") or {}).get("name") or "").strip()
        metadata_location_values = [
            item.get("value", "")
            for item in (job.get("metadata") or [])
            if "location" in normalize_text(item.get("name", "")) or "office" in normalize_text(item.get("name", ""))
        ]
        content_text = html_to_text(job.get("content") or "")

        job_data = build_job(
            company,
            job.get("title") or "",
            job_link,
            [location_text, *metadata_location_values],
            [content_text],
        )
        if not job_data:
            continue

        seen_links.add(job_link)
        jobs.append(job_data)

    finalize_jobs(company, logo_url, jobs)


def run_lever(company, site_token, logo_url):
    url = f"https://api.lever.co/v0/postings/{site_token}?mode=json"
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()

    jobs = []
    seen_links = set()

    for job in response.json():
        job_link = job.get("hostedUrl")
        if not job_link or job_link in seen_links:
            continue

        categories = job.get("categories") or {}
        all_locations = " ; ".join(categories.get("allLocations") or [])
        location_text = categories.get("location") or ""
        workplace_type = job.get("workplaceType") or ""
        description_text = html_to_text(job.get("description") or "")

        job_data = build_job(
            company,
            job.get("text") or "",
            job_link,
            [location_text, all_locations],
            [workplace_type, description_text],
        )
        if not job_data:
            continue

        seen_links.add(job_link)
        jobs.append(job_data)

    finalize_jobs(company, logo_url, jobs)


def run_workday(company, api_url, external_base_url, logo_url, search_text="Romania"):
    jobs = []
    seen_links = set()
    offset = 0
    limit = 20
    total = None

    while total is None or offset < total:
        payload = {
            "appliedFacets": {},
            "limit": limit,
            "offset": offset,
            "searchText": search_text,
        }
        response = requests.post(api_url, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        postings = data.get("jobPostings") or []
        if total is None:
            total = data.get("total") or len(postings)

        if not postings:
            break

        for job in postings:
            external_path = job.get("externalPath") or ""
            if not external_path:
                continue

            job_link = external_base_url + external_path
            if job_link in seen_links:
                continue

            location_text = job.get("locationsText") or ""
            bullet_text = " ".join(job.get("bulletFields") or [])
            remote_text = job.get("remoteType") or ""

            job_data = build_job(
                company,
                job.get("title") or "",
                job_link,
                [location_text],
                [remote_text, bullet_text],
            )
            if not job_data:
                continue

            seen_links.add(job_link)
            jobs.append(job_data)

        offset += limit

    finalize_jobs(company, logo_url, jobs)
