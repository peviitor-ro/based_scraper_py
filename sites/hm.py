from scraper_peviitor import Scraper, loadingData
import uuid
import json

data = {"locations": [], "workAreas": [], "contractType": [], "fulltext": "Romania", "order_by": "relevance", "page": 1}
url = "https://career.hm.com/wp-json/hm/v1/sr/jobs/search?_locale=user"

# Se creează o instanță a clasei ScraperSelenium pentru a accesa site-ul
scraper = Scraper()
jobs = scraper.post(url, data).json()

company = {"company": "HM"}
finalJobs = list()

#din obiectul json extragem lista de job-uri
while jobs.get("jobs"):
    for job in jobs.get("jobs"):
        id = str(uuid.uuid4())
        job_title = job.get("title")
        job_link = job.get("permalink")
        location = job.get("city")

        finalJobs.append({
                "id": id,
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": location,
            })

    # Se trece la pagina următoare
    data["page"] += 1
    jobs = scraper.post(url, data).json()

# Se afișează numărul de job-uri extrase
print(json.dumps(finalJobs, indent=4))

#Salvarea datelor în baza de date
loadingData(finalJobs, company.get("company"))