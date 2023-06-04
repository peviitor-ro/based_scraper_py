from scraper_peviitor import Scraper, Rules, loadingData

import uuid
import re

import json

regex = re.compile(r'jobsCallback\((.*)\)')

apiUrl = "https://jobsapi-internal.m-cloud.io/api/job?callback=jobsCallback&facet%5B%5D=business_unit%3ARomania&sortfield=title&sortorder=ascending&Limit=100&Organization=2292&offset=1&useBooleanKeywordSearch=true"

scraper = Scraper(apiUrl)

jobs = json.loads(regex.search(scraper.soup.text).group(1)).get("queryResult")

finalJobs = list()

for job in jobs:
    id = str(uuid.uuid4())
    job_title = job.get("title")
    job_link = job.get("url")
    company = "HP"
    country = "Romania"
    city = job.get("primary_city")

    print(job_title + " -> " + city)

    finalJobs.append(
        {
            "id": id,
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city,
        }
    )

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, "HP")