from scraper_peviitor import Scraper, loadingData
from utils import translate_city, publish, publish_logo, show_jobs
from getCounty import get_county

apiUrl = (
    "https://analogdevices.wd1.myworkdayjobs.com/wday/cxs/analogdevices/External/jobs"
)

company = {"company": "ADI"}
finalJobs = list()

scraper = Scraper()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": "Romania"}

scraper.session.headers.update(headers)

numberOfJobs = scraper.post(apiUrl, json=data).json().get("total")

iteration = [i for i in range(0, numberOfJobs, 20)]

for num in iteration:
    data["offset"] = num
    jobs = scraper.post(apiUrl, json=data).json().get("jobPostings")
    for job in jobs:
        job_title = job.get("title")
        job_link = (
            "https://analogdevices.wd1.myworkdayjobs.com/en-US/External"
            + job.get("externalPath")
        )
        location = job.get("locationsText").split(",")
        city = location[1].strip()

        finalJobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
                "county": get_county(city),
            }
        )

publish(4, company.get("company"), finalJobs, "APIKEY")

logoUrl = "https://d1yjjnpx0p53s8.cloudfront.net/styles/logo-original-577x577/s3/072011/analog-logo.ai_.png?itok=RM5-oQ34"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
