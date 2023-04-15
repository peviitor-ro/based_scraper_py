from scraper_peviitor import Scraper, Rules, loadingData

import uuid


#Folosim ScraperSelenium deoarece numarul de joburi este incarcat prin AJAX
scraper = Scraper("https://careers.eon.com/romania/go/Toate-joburile-din-Romania/3727401?utm_source=pagina-cariere-ro")
rules = Rules(scraper)


#Luam numarul total de joburi
jobs = rules.getTag("span", {"class": "paginationLabel"}).find_all("b")[1]
step = 25

# Calculam numarul de pagini
totalJobs = [*range(0, int(jobs.text), step)]

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
        company = "Eon"
        country = "Romania"
        city = job.find("span", {"class": "jobLocation"}).text.split(",")[0]
        print(job_title + " -> " + city.strip())

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city.strip(),
        })

#Afisam numarul de joburi extrase
print("Total jobs: " + str(len(finalJobs)))

#Incarcam joburile in baza de date
loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", "Eon")