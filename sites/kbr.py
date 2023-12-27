from scraper_peviitor import Scraper, loadingData
from utils import (translate_city, show_jobs)
from getCounty import get_county

apiUrl = "https://kbr.wd5.myworkdayjobs.com/wday/cxs/kbr/KBR_Careers/jobs"

company = {"company": "KBR"}
finalJobs = list()

scraper = Scraper()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {"appliedFacets":{},"limit":20,"offset":0,"searchText":"Romania"}

scraper.session.headers.update(headers)

numberOfJobs = scraper.post(apiUrl, json=data).json().get("total")

iteration = [i for i in range(0, numberOfJobs, 20)]

for num in iteration:
    data["offset"] = num
    jobs = scraper.post(apiUrl, json=data).json().get("jobPostings")
    for job in jobs:
        job_title = job.get("title")
        job_link = "https://kbr.wd5.myworkdayjobs.com/en-US/KBR_Careers" + job.get("externalPath")
        city = translate_city(job.get("locationsText").split(",")[0])
        county = None

        if "Romania" in city:
            city = "All"
            county = "All"
        else:
            county = get_county(city)

        finalJobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county,
        })

show_jobs(finalJobs)

loadingData(finalJobs, company.get("company"))

logoUrl = "https://kbr.wd5.myworkdayjobs.com/KBR_Careers/assets/logo"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))
