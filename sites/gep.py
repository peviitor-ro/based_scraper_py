import html
import math
import re

import requests

from utils import publish_or_update, publish_logo, create_job, show_jobs

company = "GEP"
careers_url = "https://geppeoplecentral.darwinbox.com/ms/candidatev2/main/careers/allJobs"
api_url = "https://geppeoplecentral.darwinbox.com/ms/candidateapi/job/alljobs"
job_url = "https://geppeoplecentral.darwinbox.com/ms/candidatev2/main/careers/jobDetails/{}"
index_url = "https://freehire.me/companies/gep-worldwide-nb-ventures"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml",
}


def build_job(title, link):
    return create_job(
        job_title=re.sub(r"\s+", " ", html.unescape(title)).strip(),
        job_link=link,
        city="Cluj-Napoca",
        county="Cluj",
        country="Romania",
        company=company,
        remote=[],
    )


def api_jobs(session):
    try:
        session.get(careers_url, timeout=30)
        response = session.post(
            api_url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Origin": "https://geppeoplecentral.darwinbox.com",
                "Referer": careers_url,
                "X-Requested-With": "XMLHttpRequest",
            },
            json={
                "companyId": "main",
                "page": 1,
                "limit": 100,
                "sort_option": "new",
                "country": ["Romania"],
                "count": 1,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return []

    rows = data.get("jobs") or data.get("data") or []
    if isinstance(rows, dict):
        rows = rows.get("jobs") or rows.get("data") or []

    jobs = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        location = " ".join(
            str(row.get(key) or "")
            for key in ("locations", "location", "city", "tool_tip_locations")
        )
        if "romania" not in location.lower():
            continue
        title = row.get("title") or row.get("job_title") or row.get("jobTitle")
        job_id = row.get("id") or row.get("job_id") or row.get("jobId")
        if not title or not job_id:
            continue
        link = row.get("job_link") or job_url.format(job_id)
        jobs.append(build_job(str(title), link))
    return jobs


def source_job(session, job_id):
    try:
        response = session.get(job_url.format(job_id), timeout=30)
        response.raise_for_status()
    except requests.RequestException:
        return None

    match = re.search(r'<meta property="og:title" content="([^"]+)"', response.text)
    if not match:
        return None

    _, _, detail = html.unescape(match.group(1)).partition("|")
    detail = re.sub(r"\s+", " ", detail).strip()
    match = re.match(r"^(.*)\s+\(([^()]*)\)$", detail)
    if not match:
        return None
    title, location = match.groups()
    if not re.search(r"\bCluj\b", location, re.I) or "Romania" not in location:
        return None
    if not title.strip():
        return None
    return build_job(title, job_url.format(job_id))


def indexed_jobs(session):
    try:
        response = session.get(index_url, timeout=30)
        response.raise_for_status()
        first_page = response.text
    except requests.RequestException:
        return []

    total_match = re.search(r"\btotal:(\d+)", first_page)
    total_pages = min(math.ceil(int(total_match.group(1)) / 20), 10) if total_match else 1
    pages = [first_page]
    for page in range(2, total_pages + 1):
        try:
            page_response = session.get(f"{index_url}?page={page}", timeout=30)
            page_response.raise_for_status()
        except requests.RequestException:
            break
        pages.append(page_response.text)

    pattern = re.compile(
        r'external_id:"geppeoplecentral\.darwinbox\.com:([a-f0-9]{10,})"'
        r"[^}]*?location:\"([^\"]*)\"",
        re.S | re.I,
    )
    job_ids = []
    for page in pages:
        for job_id, location in pattern.findall(page):
            if "romania" in location.lower() and job_id not in job_ids:
                job_ids.append(job_id)

    jobs = []
    for job_id in job_ids:
        job = source_job(session, job_id)
        if job and job not in jobs:
            jobs.append(job)
    return jobs


session = requests.Session()
session.headers.update(headers)

jobs = api_jobs(session)
if not jobs:
    jobs = indexed_jobs(session)

publish_or_update(jobs)
publish_logo(
    company,
    "https://gep.icims.com/icims2/servlet/icims2?module=AppInert&action=download&id=96578&hashed=855987836",
)
show_jobs(jobs)
