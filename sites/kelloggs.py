from scraper_peviitor import Scraper, loadingData, Rules
import uuid
import json

url = "https://jobs.kellogg.com/search/?createNewAlert=false&q=&locationsearch=Romania"

company = {"company": "Kelloggs"}
finalJobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

totalJobs = int(rules.getTag("span", {"class": "paginationLabel"}).find_all("b")[-1].text.strip())

paginate = [*range(1, totalJobs, 50)]

for row in paginate:
    url = url + f"&startrow={row}"
    scraper.url = url

    jobs = rules.getTag("table", {"id": "searchresults"}).find("tbody").find_all("tr")

    for job in jobs:
        id = uuid.uuid4()
        job_title = job.find("a").text.strip()
        job_link = "https://jobs.kellogg.com" + job.find("a").get("href")
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

logoUrl = "https://rmkcdn.successfactors.com/e1d74a18/3cf7a194-92ba-497b-8c9b-a.jpg"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))