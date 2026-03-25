from utils import show_jobs, publish_or_update, publish_logo
import requests


company = "hcltechnologies"
finalJobs = []

ROMANIA_LOCATIONS = {
    "city": ["Brasov", "Iasi", "Bucuresti"],
    "county": ["Brasov", "Iasi", "Bucuresti"],
}

post_data = {
    "locale": "en_US",
    "pageNumber": 0,
    "sortBy": "",
    "keywords": "",
    "location": "",
    "facetFilters": {},
    "brand": "",
    "skills": [],
    "categoryId": 9556055,
    "alertId": "",
    "rcmCandidateId": "",
}

url = "https://careers.hcltech.com/services/recruiting/v1/jobs"
pageNumber = 0
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://careers.hcltech.com",
    "Referer": "https://careers.hcltech.com/go/Romania/9556055/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
}

jobs = requests.post(url, json=post_data, headers=headers, timeout=20).json()

total_jobs = jobs.get("totalJobs", 0)
pages = (total_jobs // 10) + 1

while pageNumber < pages:
    for job in jobs.get("jobSearchResult", []):
        obj = job.get("response") or {}
        locales = obj.get("supportedLocales") or ["en_US"]
        finalJobs.append(
            {
                "job_title": obj.get("unifiedStandardTitle"),
                "job_link": f"https://careers.hcltech.com/job/{obj.get('urlTitle')}/{obj.get('id')}-{locales[0]}",
                "company": company,
                "country": "Romania",
                "city": ROMANIA_LOCATIONS["city"],
                "county": ROMANIA_LOCATIONS["county"],
            }
        )

    pageNumber += 1
    post_data["pageNumber"] = pageNumber
    jobs = requests.post(url, json=post_data, headers=headers, timeout=20).json()


publish_or_update(finalJobs)

publish_logo(
    company,
    "https://www.hcltech.com/themes/custom/hcltech/images/hcltech-new-logo.svg",
)
show_jobs(finalJobs)
