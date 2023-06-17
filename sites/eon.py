from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

#Folosim ScraperSelenium deoarece numarul de joburi este incarcat prin AJAX
scraper = Scraper("https://careers.eon.com/romania/go/Toate-joburile-din-Romania/3727401?utm_source=pagina-cariere-ro")
rules = Rules(scraper)

#Luam numarul total de joburi
jobs = rules.getTag("span", {"class": "paginationLabel"}).find_all("b")[1]
step = 25

# Calculam numarul de pagini
totalJobs = [*range(0, int(jobs.text), step)]

company = {"company": "Eon"}
finalJobs = list()

#Pentru fiecare pagina, luam joburile si le adaugam in lista finalJobs
for page in totalJobs:
    pageurl = f"https://careers.eon.com/romania/go/Toate-joburile-din-Romania/3727401/{page}/?q=&sortColumn=referencedate&sortDirection=desc"
    pageScaper = Scraper(pageurl)
    rules = Rules(pageScaper)

    jobs = rules.getTags("tr", {"class": "data-row"})

    for job in jobs:
        id = uuid.uuid4()
        job_title = job.find("a").text
        job_link = "https://careers.eon.com" + job.find("a")["href"]
        city = job.find("span", {"class": "jobLocation"}).text.split(",")[0]

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city.strip(),
        })

#Afisam numarul de joburi extrase
print(json.dumps(finalJobs, indent=4))

#Incarcam joburile in baza de date
loadingData(finalJobs, company.get("company"))