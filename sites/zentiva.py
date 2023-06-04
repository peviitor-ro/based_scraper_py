from scraper_peviitor import Scraper, loadingData
import uuid

apiUrl = "https://zentiva.wd3.myworkdayjobs.com/wday/cxs/zentiva/Zentiva/jobs"
scraper = Scraper()
#Cream un header pentru a putea face request-uri POST
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

#Cream un dictionar cu datele pe care dorim sa le trimitem catre server
data = {"appliedFacets":{"locations":["ca7924da36fa0149be9376945a35dd27"]},"limit":20,"offset":0,"searchText":""}

#Actualizam header-ul cu datele de mai sus
scraper.session.headers.update(headers)

#Facem request-ul POST si salvam numarul total de joburi
numberOfJobs = scraper.post(apiUrl, json=data).json().get("total")

#Cream o lista cu numerele de la 0 la numarul total de joburi, cu pasul de 20
iteration = [i for i in range(0, numberOfJobs, 20)]

finaljobs = list()

#Pentru fiecare numar din lista, extragem joburile
for num in iteration:
    data["offset"] = num
    jobs = scraper.post(apiUrl, json=data).json().get("jobPostings")
    for job in jobs:
        id = uuid.uuid4()
        job_title = job.get("title")
        job_link = "https://zentiva.wd3.myworkdayjobs.com/en-US/Zentiva" + job.get("externalPath")
        company = "Zentiva"
        country = "Romania"
        city = job.get("bulletFields")[1]

        finaljobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city
        })

        print(job_title + " -> " + city)

#afisam numarul total de joburi gasite
print("Total jobs: " + str(len(finaljobs)))

#se incarca datele in baza de date
loadingData(finaljobs, "Zentiva")