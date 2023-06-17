from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

page = 0
scraper = Scraper()
rules = Rules(scraper)

company = {"company": "Crowe"}
finalJobs = list()

while True:
    url = f"https://www.crowe.com/api/sitecore/ListWithFilter/GetTable?sc_mode=normal&id=%7B7D8ADF0E-32CD-4955-8B4C-C4F8561881AE%7D&languageName=ro-RO&page={page}&isDateDesc=true&enforceNormal=True"
    scraper.url = url

    jobs = rules.getTags("div", {"class": "news-list-table__table__item__link"})

    if len(jobs) != 0:
        for job in jobs:
            id = uuid.uuid4()
            job_title = job.find("a").text.strip()
            job_link = job.find("a").get("href")
            
            finalJobs.append({
                "id": str(id),
                "job_title": job_title,
                "job_link": job_link,
                "country": "Romania",
                "city": "Romania",
                "company": company.get("company")
            })
    else:
        break

    page += 1

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))

logoUrl = "https://i.ytimg.com/vi/dTmm3WNIpnc/maxresdefault.jpg"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))
