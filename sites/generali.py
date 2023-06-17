from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

#Cream o instanta a clasei Scraper
scraper = Scraper("https://cariere.generali.ro/jobs/search?cuvant_cheie=&id_location=0&search_for_jobs=Cauta&jobsno=")
rules = Rules(scraper)

#Cautam toate tagurile h3 cu clasa h3-list-job-title
jobs = rules.getTags("h3", {"class": "h3-list-job-title"})

company = {"company": "Generali"}
finaljobs = list()

#Pentru fiecare job, extragem titlul, linkul, compania, tara si orasul
for job in jobs:
    id = uuid.uuid4()
    job_title = job.text.strip()
    job_link = job.find("a").get("href")

    finaljobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": "Romania"
    })

#Afisam numarul total de joburi
print(json.dumps(finaljobs, indent=4))

#Incarcam datele in baza de date
loadingData(finaljobs, company.get("company"))