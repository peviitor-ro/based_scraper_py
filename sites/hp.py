from scraper_peviitor import Scraper, loadingData
import uuid
import re
import json

regex = re.compile(r'jobsCallback\((.*)\)')

apiUrl = "https://jobsapi-internal.m-cloud.io/api/job?callback=jobsCallback&facet%5B%5D=business_unit%3ARomania&sortfield=title&sortorder=ascending&Limit=100&Organization=2292&offset=1&useBooleanKeywordSearch=true"
scraper = Scraper(apiUrl)

jobs = json.loads(regex.search(scraper.soup.text).group(1)).get("queryResult")

company = {"company": "HP"}
finalJobs = list()

for job in jobs:
    id = str(uuid.uuid4())
    job_title = job.get("title")
    job_link = job.get("url")
    city = job.get("primary_city")

    finalJobs.append({
            "id": id,
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
        })

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))