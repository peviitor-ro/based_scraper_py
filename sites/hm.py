from scraper_peviitor import Scraper, loadingData

import uuid

data = {"locations": [], "workAreas": [], "contractType": [], "fulltext": "Romania", "order_by": "relevance", "page": 1}
url = "https://career.hm.com/wp-json/hm/v1/sr/jobs/search?_locale=user"
# Se creează o instanță a clasei ScraperSelenium pentru a accesa site-ul
scraper = Scraper()
jobs = scraper.post(url, data)

finalJobs = list()

#din obiectul json extragem lista de job-uri
while jobs.get("jobs"):
    for job in jobs.get("jobs"):
        id = str(uuid.uuid4())
        job_title = job.get("title")
        job_link = job.get("permalink")
        company = "HM"
        country = "Romania"
        location = job.get("city")

        finalJobs.append(
            {
                "id": id,
                "job_title": job_title,
                "job_link": job_link,
                "company": company,
                "country": country,
                "city": location,
            }
        )

        print(job_title + " -> " + location)

    # Se trece la pagina următoare
    data["page"] += 1
    jobs = scraper.post(url, data)

# Se afișează numărul de job-uri extrase
print("Total jobs: " + str(len(finalJobs)))

#Salvarea datelor în baza de date
loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", "HM")







