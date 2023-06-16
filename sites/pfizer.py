from scraper_peviitor import Scraper, loadingData
import uuid

apiUrl = "https://pfizer.wd1.myworkdayjobs.com/wday/cxs/pfizer/PfizerCareers/jobs"
scraper = Scraper()
#Cream un header pentru a putea face request-uri POST
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

#Cream un dictionar cu datele pe care dorim sa le trimitem catre server
data = {"appliedFacets":{},"limit":20,"offset":0,"searchText":"Romania"}

#Actualizam header-ul cu datele de mai sus
scraper.session.headers.update(headers)

#Facem request-ul POST si salvam numarul total de joburi
numberOfJobs = scraper.post(apiUrl, json=data).json().get("total")

#Cream o lista cu numerele de la 0 la numarul total de joburi, cu pasul de 20
iteration = [i for i in range(0, numberOfJobs, 20)]

company = {"company": "Pfizer"}
finaljobs = list()

#Pentru fiecare numar din lista, extragem joburile
for num in iteration:
    data["offset"] = num
    jobs = scraper.post(apiUrl, json=data).json().get("jobPostings")
    for job in jobs:
        id = uuid.uuid4()
        job_title = job.get("title")
        job_link = "https://pfizer.wd1.myworkdayjobs.com/en-US/PfizerCareers" + job.get("externalPath")

        finaljobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": "Romania"
        })

#afisam numarul total de joburi gasite
print(finaljobs)

#se incarca datele in baza de date
loadingData(finaljobs, company.get("company"))