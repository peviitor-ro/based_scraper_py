from scraper_peviitor import Scraper, loadingData
import uuid

apiUrl = " https://careers.kpmg.ro/api/Talentlyft/jobs/filter"

scraper = Scraper()

#Cream un header pentru a putea face request-uri POST
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

#Cream un dictionar cu datele pe care dorim sa le trimitem catre server
data = {"Departments":[],"Locations":[],"CareerLevel":None,"WorkplaceType":None,"Tags":[],"CurrentPage":1,"PageSize":10}

#Actualizam header-ul cu datele de mai sus
scraper.session.headers.update(headers)

#Facem request-ul POST si salvam numarul total de joburi
jobs = []
try:
    jobs = scraper.post(apiUrl, json=data).json().get("Results")
except:
    print({"succes":"no jobs found"})

company = {"company": "KPMG"}
finalJobs = list()

while jobs:
    for job in jobs:
        id = uuid.uuid4()
        job_title = job.get("Title")
        job_link = job.get("AbsoluteUrl")
        city = job.get("Location").get("City")

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city
        })

    data["CurrentPage"] += 1
    jobs = scraper.post(apiUrl, json=data).json().get("Results")

#afisam numarul total de joburi gasite
print(finalJobs)

#se incarca datele in baza de date
loadingData(finalJobs, company.get("company"))