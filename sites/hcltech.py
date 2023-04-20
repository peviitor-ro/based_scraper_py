from scraper_peviitor import Scraper, Rules, loadingData

import uuid

url = "https://www.hcltech.com/romania/careers"

scraper = Scraper()
rules = Rules(scraper)

pgeNumber = 0

finalJobs = list()
while True:

    pagesQuery = url + f"?_wrapper_format=html&field_job_geography_value=All&field_designation_value_ers=&page={pgeNumber}"
    scraper.url = pagesQuery

    try:
        jobs = rules.getTag("div", {"class": "view-hcl-ers-career-jobs"}).find("tbody").find_all("tr")
    except:
        break

    for job in jobs:
        id = uuid.uuid4()
        job_title = job.find("td", {"class": "views-field-title"}).text.strip()
        job_link = "https://www.hcltech.com" + job.find("td", {"class": "views-field-title"}).find("a").get("href")
        company = "HCLTechnologies"
        country = "Romania"
        city = job.find("td", {"class": "views-field-field-job-location"}).text.strip()

        print(job_title + " -> " + city)
        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city
        })

    pgeNumber += 1

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", "HCLTechnologies")
