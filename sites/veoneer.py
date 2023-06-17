from scraper_peviitor import Scraper, loadingData, Rules
import uuid
import json

url = "https://veoneerro.teamtailor.com/jobs"

company = {"company": "Veoneer"}
finalJobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTag("div", {"class":"mx-auto text-lg block-max-w--lg"}).find_all("li", {"class": "w-full"})

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("span", {"class": "company-link-style"}).text.strip()
    job_link = job.find("a").get("href")
    city = ""
    try:
        city = job.find("div", {"class": "mt-1 text-md"}).find_all("span")[2].split(",")[0].strip()
    except:
        city = job.find("div", {"class": "mt-1 text-md"}).find_all("span")[2].text.strip()

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "country": "Romania",
        "city": city,
        "company": company.get("company")
    })

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))

logoUrl = "https://seekvectorlogo.com/wp-content/uploads/2020/02/veoneer-inc-vector-logo-small.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))