from scraper.Scraper import Scraper
from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty
import json
from math import ceil

_counties = GetCounty()
apiUrl = "https://msd.wd1.myworkdayjobs.com/wday/cxs/msd/MSDExternal/jobs"
scraper = Scraper()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

data = {"appliedFacets":{},"limit":20,"offset":0,"searchText":"Romania"}

scraper.set_headers(headers)

company = {"company": "MSD"}
finalJobs = []

try:
    response = scraper.post(apiUrl, json.dumps(data))
    if response.status_code == 200:
        job_data = response.json()
        numberOfJobs = job_data.get("total", 0)
        iteration = ceil(numberOfJobs / 20) if numberOfJobs > 0 else 1
        
        for num in range(iteration):
            data["offset"] = num * 20
            response = scraper.post(apiUrl, json.dumps(data))
            if response.status_code != 200:
                break
            jobs = response.json().get("jobPostings", [])
            
            for job in jobs:
                job_title = job.get("title")
                job_link = "https://msd.wd1.myworkdayjobs.com/en-US/MSDExternal" + job.get("externalPath")
                locations_text = job.get("locationsText", "")
                city = translate_city(locations_text.split("-")[-1].strip()) if locations_text else ""
                county = _counties.get_county(city)
                
                job_element = {
                    "job_title": job_title,
                    "job_link": job_link,
                    "company": company.get("company"),
                    "country": "Romania",
                }
                
                if not county:
                    job_element["remote"] = "remote"
                else:
                    job_element["city"] = city
                    job_element["county"] = county
                
                finalJobs.append(job_element)
    else:
        print(f"API returned status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")

publish_or_update(finalJobs)

logoUrl = "https://www.msdmanuals.com/Content/Images/msd_foot_logo.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
