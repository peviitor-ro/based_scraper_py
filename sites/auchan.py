from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import re
import json

#Folosim ScraperSelenium pentru a putea naviga pe pagini
url = "https://cariere.auchan.ro/jobs?per_page=1000"
scraper = Scraper()
scraper.session.verify = False
scraper.session.headers.update({"X-Requested-With": "XMLHttpRequest"})
scraper.url = url
html = scraper.getJson().get("html")
totalJobs = scraper.getJson().get("search_result_info").split(" ")[-3]
print(totalJobs)
scraper.soup = html

jobs = list()

pages = [*range(1000, int(totalJobs) , 1000)]
pages.append(int(totalJobs) - pages[-1])

for page in range(len(pages)):
    if pages[page] % 1000 == 0:
        url = f"https://cariere.auchan.ro/jobs?page={page + 1}&per_page={pages[page] % 1000 + 1000}"
    else:
        url = f"https://cariere.auchan.ro/jobs?page={page + 1}&per_page={pages[page]}"

    scraper.url = url
    html = scraper.getJson().get("html")
    scraper.soup = html

    rules = Rules(scraper)

    jobs = [*jobs, *rules.getTags("a", {"class": "job editable-cursor"})]


company = {"company": "Auchan"}
finaljobs = list()

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("div", {"class":"job-title"}).text.strip()
    job_link = job.get("href")
    city = job.find("div", {"class":"location-inline"}).text.strip()
    
    finaljobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city
    })

#Afisam numarul total de joburi
print(json.dumps(finaljobs, indent=4))
print(len(finaljobs)) 

#Incarcam datele in baza de date
loadingData(finaljobs, company.get("company"))