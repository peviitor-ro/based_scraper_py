from scraper_peviitor import Scraper
from utils import publish, publish_logo, show_jobs, translate_city
from getCounty import get_county

apiUrl = "https://thales.wd3.myworkdayjobs.com/wday/cxs/thales/Careers/jobs"

company = {"company": "ThalesGroup"}
finalJobs = list()

scraper = Scraper()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {
    "appliedFacets": {"locationCountry": ["f2e609fe92974a55a05fc1cdc2852122"]},
    "limit": 20,
    "offset": 0,
    "searchText": "",
}

scraper.session.headers.update(headers)

numberOfJobs = scraper.post(apiUrl, json=data).json().get("total")

iteration = [i for i in range(0, numberOfJobs, 20)]

for num in iteration:
    data["offset"] = num
    jobs = scraper.post(apiUrl, json=data).json().get("jobPostings")
    for job in jobs:
        job_title = job.get("title")
        job_link = "https://thales.wd3.myworkdayjobs.com/en-US/Careers" + job.get(
            "externalPath"
        )
        city = translate_city(job.get("locationsText").split(",")[0])
        county = get_county(city)

        finalJobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
                "county": county,
            }
        )

publish(4, company.get("company"), finalJobs, "APIKEY")

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Thales_Logo.svg/484px-Thales_Logo.svg.png?20210518101610"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
