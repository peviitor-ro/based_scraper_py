from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json 
import os

#Cream o instanta a clasei Scraper
scraper = Scraper("https://cariere.generali.ro/jobs/search?cuvant_cheie=&id_location=0&search_for_jobs=Cauta&jobsno=")
rules = Rules(scraper)

#Cautam toate tagurile h3 cu clasa h3-list-job-title
jobs = rules.getTags("h3", {"class": "h3-list-job-title"})

finaljobs = list()

#Pentru fiecare job, extragem titlul, linkul, compania, tara si orasul
for job in jobs:
    id = uuid.uuid4()
    job_title = job.text.strip()
    job_link = job.find("a").get("href")
    company = "Generali"
    country = "Romania"
    city = "Romania"

    print(job_title)

    finaljobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company,
        "country": country,
        "city": city
    })

#Afisam numarul total de joburi
print("Total jobs: " + str(len(finaljobs)))

#Salvam datele in fisierul json
with open("json/generali.json", "w") as f:
    json.dump(finaljobs, f, indent=4)

#Incarcam datele in baza de date
apikey = os.environ.get("apikey")
loadingData(finaljobs, apikey, "Generali")