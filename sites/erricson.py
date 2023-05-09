from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://jobs.ericsson.com/search/?q=&locationsearch=Romania"

company = {"company": "Ericsson"}
finaljobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

totaljobs = int(scraper.soup.find("span", {"class": "paginationLabel"}).find_all("b")[1].text)
step = 25

querystings = [*range(0, totaljobs, step)]

for number in querystings:
    scraper.url = url + f"&startrow={number}"
    jobs = rules.getTag("table", {"class": "searchResults"}).find("tbody").find_all("tr")
    for job in jobs:
        id = uuid.uuid4()
        job_title = job.find("a").text.strip()
        job_link = "https://jobs.ericsson.com" + job.find("a").get("href")
        country = "Romania"
        company = "Ericsson"
        city = job.find("span", {"class": "jobLocation"}).text.split(",")[0].strip()

        print(job_title + " -> " + city)
        
        finaljobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "country": country,
            "company": company,
            "city": city
        })

print("Total jobs: " + str(len(finaljobs)))

loadingData(finaljobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", "Ericsson")

logoUrl = "https://1000logos.net/wp-content/uploads/2021/05/Ericsson-logo-500x281.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":"Ericsson",
        "logo":logoUrl
    }
]))