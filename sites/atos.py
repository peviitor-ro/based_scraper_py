from scraper_peviitor import Scraper, loadingData, Rules
import uuid
import json

url = "https://jobs.atos.net/go/Jobs-in-Romania/3686501/0/?q=&sortColumn=referencedate&sortDirection=desc"

company = {"company": "Atos"}
finalJobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

totalJobs = int(rules.getTag("span", {"class": "paginationLabel"}).find_all("b")[-1].text.strip())

paginate = [*range(1, totalJobs, 50)]

for page in paginate:
    url = f"https://jobs.atos.net/go/Jobs-in-Romania/3686501/{page}/?q=&sortColumn=referencedate&sortDirection=desc"
    scraper.url = url

    jobs = rules.getTag("table", {"id": "searchresults"}).find("tbody").find_all("tr")

    for job in jobs:
        id = uuid.uuid4()
        job_title = job.find("a").text.strip()
        job_link = "https://jobs.atos.net" + job.find("a").get("href")
        city = job.find("span", {"class": "jobLocation"}).text.split(",")[0].strip()

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "country": "Romania",
            "city": city,
            "company": company.get("company")
        })

print(finalJobs)

loadingData(finalJobs, company.get("company"))

logoUrl = "https://rmkcdn.successfactors.com/a7d5dbb6/c9ab6ccb-b086-47f2-b25b-2.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))