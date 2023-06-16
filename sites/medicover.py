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

company = {"company": "Medicover"}
finalJobs = list()

#Pentru fiecare job
for job in jobs:
    id = uuid.uuid4()
    job_title = job.get("jobTitle")
    job_link = "https://medicover.mingle.ro/en/apply/" + job.get("publicUid")
    city = job.get("locations")

    if city is None:
        city = "Romania"
    else:
        city = city[0].get("name")

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city
    })

#Numarul de joburi gasite
print(finalJobs)

#Incarc joburile in baza de date
loadingData(finalJobs, company.get("company"))