from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://www.inetum.com/en/jobs?f%5B0%5D=region%3A1068"

company = {"company": "Inetum"}
finalJobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

totalJobs = int(rules.getTag("li", {"id": "1068"}).find("span", {"class":"facet-item__count"}).text.replace("(", "").replace(")", "").strip())

paginations = [*range(1, totalJobs, 9)]

for page in range(len(paginations)):
    scraper.url = "https://www.inetum.com/en/jobs?f%5B0%5D=region%3A1068&page=" + str(page)
    rules = Rules(scraper)

    jobs = rules.getTags("div", {"class": "node node-job node-teaser"})

    for job in jobs:
        id = uuid.uuid4()
        job_title = job.find("h3", {"class":"card-title"}).text.strip()
        job_link = "https://www.inetum.com" + job.find("a").get("href")
        city = job.find("p", {"class": "card-text"}).text.split("-")[-1].strip()

        print(job_title + " -> " + city)

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city
        })

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", company.get("company"))

logoUrl = "https://vtlogo.com/wp-content/uploads/2021/05/inetum-vector-logo-small.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))

