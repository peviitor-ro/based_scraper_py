from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import re
import json

#Folosim ScraperSelenium pentru a putea naviga pe pagini
url = "https://cariere.auchan.ro"
scraper = Scraper()
scraper.session.verify = False
scraper.url = url
rules = Rules(scraper)

doomBody = rules.getTag("body")
regex = re.compile(r'vmCfg = {(.*)}')

jobs = re.search(regex, doomBody.prettify()).group(1)

jobs = json.loads("{" + jobs + "}")

company = {"company": "Auchan"}
finaljobs = list()

for job in jobs.get("PositionList"):
    id = uuid.uuid4()
    job_title = job.get("PositionName")
    job_link = "https://cariere.auchan.ro/" + f"Position/Details?id={job.get('PositionId')}"
    city = job.get("CityList")
    
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

#Incarcam datele in baza de date
loadingData(finaljobs, company.get("company"))