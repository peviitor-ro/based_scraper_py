from scraper.Scraper import Scraper
from utils import (
    show_jobs,
    publish_or_update,
    publish_logo,
    acurate_city_and_county,
)
import json

company = "hcltechnologies"
finalJobs = list()

acurate_city = acurate_city_and_county(Iasi={"city": "Iasi", "county": "Iasi"})

post_data = {"locale": "en_US", "pageNumber": 0, "sortBy": "", "keywords": "", "location": "", "facetFilters": {
}, "brand": "", "skills": [], "categoryId": 9556055, "alertId": "", "rcmCandidateId": ""}

url = "https://careers.hcltech.com/services/recruiting/v1/jobs"
pageNumber = 0
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15"
}
scraper = Scraper()
scraper.set_headers(headers)

jobs = scraper.post(url, json.dumps(post_data)).json()

total_jobs = jobs.get("totalJobs", 0)
pages = (total_jobs //10) + 1

while pageNumber < pages:
    for job in jobs.get("jobSearchResult", []):
        obj = job.get("response")
        job_title = obj.get("unifiedStandardTitle")
        job_link = f"https://careers.hcltech.com/job/{obj.get('urlTitle')}/{obj.get('id')}-{obj.get('supportedLocales')[0]}"
        finalJobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "company": company,
                "country": "Romania",
            }
        )
    pageNumber += 1
    post_data["pageNumber"] = pageNumber
    jobs = scraper.post(url, json.dumps(post_data)).json()


 

publish_or_update(finalJobs)

publish_logo(
    company, "https://www.hcltech.com/themes/custom/hcltech/images/hcltech-new-logo.svg"
)
show_jobs(finalJobs)
