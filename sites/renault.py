from scraper.Scraper import Scraper
from utils import show_jobs, publish_or_update, publish_logo, translate_city
from getCounty import GetCounty, remove_diacritics
from math import ceil
import json

_counties = GetCounty()
apiUrl = "https://alliancewd.wd3.myworkdayjobs.com/wday/cxs/alliancewd/renault-group-careers/jobs"
scraper = Scraper()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {"appliedFacets": {"locationCountry": ["f2e609fe92974a55a05fc1cdc2852122"], "workerSubType": [
    "62e55b3e447c01871e63baa4ca0f9391", "62e55b3e447c01140817bba4ca0f9891", "62e55b3e447c01d10acebaa4ca0f9691"]}, "limit": 20, "offset": 0, "searchText": ""}

scraper.set_headers(headers)

numberOfJobs = scraper.post(apiUrl, json.dumps(data)).json().get("total")

iteration = ceil(numberOfJobs / 20)

company = {"company": "Renault"}
finaljobs = list()

for num in range(iteration):
    data["offset"] = num * 20
    jobs = scraper.post(apiUrl, json.dumps(data)).json().get("jobPostings")
    for job in jobs:
        job_title = job.get("title").replace("[", "").replace("]", "")
        job_link = "https://alliancewd.wd3.myworkdayjobs.com/ro-RO/renault-group-careers" + \
            job.get("externalPath")
        city = translate_city(remove_diacritics(job.get("bulletFields")[0]))
        county = _counties.get_county(city) or []

        if not county:
            city = "Bucuresti"
            county = "Bucuresti"

        finaljobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county
        })

publish_or_update(finaljobs)

logo_url = "https://logos-world.net/wp-content/uploads/2021/04/Renault-Logo-700x394.png"
publish_logo(company.get("company"), logo_url)
show_jobs(finaljobs)
