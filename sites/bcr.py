from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

#Cream o instanta a clasei Scraper
scraper = Scraper("https://erstegroup-careers.com/bcr/search/?createNewAlert=false&q=&locations")
rules = Rules(scraper)

#Cautam elementele care contin joburile
elements = rules.getTags("tr", {"class" : "data-row"})

company = {"company": "BCR"}
finalJobs = list()

#Iteram prin elementele gasite si extragem informatiile necesare
for element in elements:
    id = uuid.uuid4()
    job_title = element.find("a", {"class": "jobTitle-link"}).text
    job_link = "https://erstegroup-careers.com" + element.find("a", {"class": "jobTitle-link"})["href"]
    city = element.find("span", {"class": "jobShifttype"}).text

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city
    })

#afișăm numărul total de joburi
print(json.dumps(finalJobs, indent=4))

#Salvăm datele in baza de date
loadingData(finalJobs, company.get("company"))