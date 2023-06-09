from scraper_peviitor import Scraper, loadingData
import uuid
import json

#urlul pentru a veadea numarul total de joburi
jobsUrl = "https://jobs.vodafone.com/api/apply/v2/jobs/"

scraper = Scraper(jobsUrl)

#extragem numarul total de joburi
number_of_jobs = scraper.getJson().get("facets").get("country").get("Romania")

#Cream o lista cu numerele de la 0 la numarul total de joburi, cu pasul de 10 pentru a putea extrage joburile
iteratii = [i for i in range(0, number_of_jobs, 10)]

company = {"company": "Vodafone"}
finalJobs = list()

#Iteram prin lista de numere si extragem joburile
for num in iteratii:
    url = f"https://jobs.vodafone.com/api/apply/v2/jobs?domain=vodafone.com&start={num}&num=10&query=Romania&domain=vodafone.com&sort_by=relevance"
    scraper.url = url

    jobs = scraper.getJson().get("positions")
    
    for job in jobs:
        country = job.get("location").split(",")[-1].strip()
        if country == "ROU" or country == "Romania":
            id = uuid.uuid4()
            job_title = job.get("name")
            job_link = f"https://jobs.vodafone.com/careers?query=Romania&pid={job.get('id')}&domain=vodafone.com&sort_by=relevance"
            location = job.get("location").split(",")[0]

            finalJobs.append({
                "id": str(id),
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": country,
                "city": location
            })

#Afisam numarul total de joburi
print(json.dumps(finalJobs, indent=4))

# Încărcăm job-urile în baza de date
loadingData(finalJobs, company.get("company"))