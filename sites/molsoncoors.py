from scraper_peviitor import Scraper, loadingData, Rules
import uuid
import json

url = "https://jobs.molsoncoors.com/MolsonCoors_GBSRomania/search/?q=Romania&startrow=1"

company = {"company": "MolsonCoors"}
finalJobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

totalJobs = int(rules.getTag("span", {"class": "paginationLabel"}).find_all("b")[-1].text.strip())

paginate = [*range(0, totalJobs, 25)]

for page in paginate:
    url = f"https://jobs.molsoncoors.com/MolsonCoors_GBSRomania/search/?q=Romania&startrow={page}"
    scraper.url = url

    jobs = rules.getTag("table", {"id": "searchresults"}).find("tbody").find_all("tr")

    for job in jobs:
        id = uuid.uuid4()
        job_title = job.find("a").text.strip()
        job_link = "https://jobs.molsoncoors.com" + job.find("a").get("href")
        city = job.find("span", {"class": "jobLocation"}).text.split(",")[0].strip()

        print(job_title + " -> " + city)

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "country": "Romania",
            "city": city,
            "company": company.get("company")
        })

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, company.get("company"))

logoUrl = "https://rmkcdn.successfactors.com/e2403c2e/b8073680-5e29-45a9-8c61-4.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))