from scraper_peviitor import Scraper, loadingData, Rules
import uuid
import re
import json

regex = re.compile(r'"token":"(.*?)"')

#Folosim ScraperSelenium deoarece joburile sunt incarcate prin AJAX
url = "https://linde.csod.com/ux/ats/careersite/20/home?c=linde&country=ro"
apiUrl = "https://eu-fra.api.csod.com/rec-job-search/external/jobs"

scraper = Scraper(url)
rules = Rules(scraper)

body = rules.getTag("body")

#Se extrage tokenul din pagina
token = regex.search(str(body)).group(1)
autorization = f"Bearer {token}"

#Se updateaza header-ul cu tokenul
scraper.session.headers.update({"Authorization": autorization})

data = {"careerSiteId":20,"careerSitePageId":20,"pageNumber":1,"pageSize":100,"cultureId":1,"searchText":"","cultureName":"en-US","states":[],"countryCodes":["ro"],"cities":[],"placeID":"","radius":"","postingsWithinDays":"","customFieldCheckboxKeys":[],"customFieldDropdowns":[],"customFieldRadios":[]}

#Se face request-ul catre API
jobs = scraper.post(apiUrl, json=data).json().get("data").get("requisitions")

company = {"company": "Linde"}
finalJobs = list()

#Se extrag joburile din raspunsul API-ului
for job in jobs:
    id = str(uuid.uuid4())
    job_title = job.get("displayJobTitle")
    job_link = "https://linde.csod.com/ux/ats/careersite/20/home/requisition/" + str(job.get("requisitionId")) + "?c=linde"

    if job.get("locations")[-1].get("city"):
        city = job.get("locations")[-1].get("city")
    else:
        city = "Romania"

    finalJobs.append({
            "id": id,
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
        })

#Se afiseaza numarul de joburi extrase
print(json.dumps(finalJobs, indent=4))

#Incarcam joburile in baza de date
loadingData(finalJobs, company.get("company"))