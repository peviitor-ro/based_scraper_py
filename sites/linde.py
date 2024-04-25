from scraper.Scraper import Scraper
import re
import json
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty() 
regex = re.compile(r'"token":"(.*?)"')

url = "https://linde.csod.com/ux/ats/careersite/20/home?c=linde&country=ro"
apiUrl = "https://eu-fra.api.csod.com/rec-job-search/external/jobs"

scraper = Scraper(url)
scraper.get_from_url(url)

body = scraper.find("body")

token = regex.search(str(body)).group(1)
autorization = f"Bearer {token}"

headers = {
    "Content-Type": "application/json",
    "Authorization": autorization
}
scraper.set_headers(headers)

data = {"careerSiteId":20,"careerSitePageId":20,"pageNumber":1,"pageSize":100,"cultureId":1,"searchText":"","cultureName":"en-US","states":[],"countryCodes":["ro"],"cities":[],"placeID":"","radius":"","postingsWithinDays":"","customFieldCheckboxKeys":[],"customFieldDropdowns":[],"customFieldRadios":[]}

jobs = scraper.post(apiUrl, json.dumps(data)).json().get("data").get("requisitions")

company = {"company": "Linde"}
finalJobs = list()

for job in jobs:
    job_title = job.get("displayJobTitle")
    job_link = "https://linde.csod.com/ux/ats/careersite/20/home/requisition/" + str(job.get("requisitionId")) + "?c=linde"

    if job.get("locations")[-1].get("city"):
        city = translate_city(job.get("locations")[-1].get("city").split(",")[0])
        county = _counties.get_county(city)
    else:
        city = "All"
        county = "All"

    finalJobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county
        })
    
publish_or_update(finalJobs)

logo_url = "https://linde.csod.com/clientimg/linde/logo/careersitenew_69223024ee0146479b6dae10819fbef1_b384c240-1957-4949-88e3-6df75abb4755.png"
publish_logo(company.get("company"), logo_url)
show_jobs(finalJobs)
