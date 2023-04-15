from scraper_peviitor import Scraper, loadingData

import uuid

url = "https://mingle.ro/api/session?company=medicover"
apiUrl = "https://mingle.ro/api/boards/mingle/jobs?q=companyUid~eq~%22medicover%22&page=0&pageSize=30&sort=modifiedDate~DESC"

scraper = Scraper(url)
#Luam cookie-ul XSRF-TOKEN
cookies = scraper.session.cookies.get_dict().get("XSRF-TOKEN")

#Setam header-ul XSRF-TOKEN
scraper.session.headers.update({"XSRF-TOKEN": cookies})
#Setam header-ul Content-Type
scraper.url = apiUrl

#Luam json-ul
jobs = scraper.getJson().get("data").get("results")

finalJobs = list()

#Pentru fiecare job
for job in jobs:
    id = uuid.uuid4()
    job_title = job.get("jobTitle")
    job_link = "https://medicover.mingle.ro/en/apply/" + job.get("publicUid") 
    company = "Medicover"
    country = "Romania"
    city = job.get("locations")

    if city is None:
        city = "Romania"
    else:
        city = city[0].get("name")

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company,
        "country": country,
        "city": city
    })

    print(job_title + " -> " + city)

#Numarul de joburi gasite
print("Total jobs: " + str(len(finalJobs)))

#Incarc joburile in baza de date
loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", "Medicover")


