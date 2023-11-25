from scraper_peviitor import Scraper, Rules, loadingData
import json
from utils import translate_city

url = "https://jobs.siemens-energy.com/en_US/jobs/Jobs/?29454=964547&29454_format=11381&listFilterMode=1&folderRecordsPerPage=20&folderOffset=0"

company = {"company": "SiemensEnergy"}
finalJobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

totalJobs = int(rules.getTag("div", {
                "class": "list-controls__text__legend"}).text.split("of")[1].replace("results", "").strip())

pages = [*range(0, totalJobs, 20)]

for page in pages:
    url = "https://jobs.siemens-energy.com/en_US/jobs/Jobs/?29454=964547&29454_format=11381&listFilterMode=1&folderRecordsPerPage=20&folderOffset=" + \
        str(page)
    scraper.url = url

    jobs = rules.getTags("details", {"class": "article--result--container"})

    for job in jobs:
        job_title = job.find(
            "div", {"class": "article__header__text"}).find("a").text.strip()
        job_link = job.find(
            "div", {"class": "article__header__text"}).find("a")["href"]
        locations = job.find("div", {"class": "article__content"}).find(
            "p").text.split(",")

        country = locations[0].split(":")[-1].strip()
        city = translate_city(locations[-1].strip())
        county = translate_city(locations[-2].strip())

        job = {
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
        }

        if len(country.split("|")) == 1:
            job["country"] = "Romania"
            job["city"] = city
            job["county"] = county

            finalJobs.append(job)

        elif country.split("|")[-1].strip() != "Romania":
            job["country"] = country.split("|")[-1].strip()
            job["city"] = city
            job["county"] = county

            finalJobs.append(job)


print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Siemens_Energy_logo.svg/799px-Siemens_Energy_logo.svg.png?20200823090225"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post("https://api.peviitor.ro/v1/logo/add/", json.dumps([
    {
        "id": company.get("company"),
        "logo": logoUrl
    }
]))
