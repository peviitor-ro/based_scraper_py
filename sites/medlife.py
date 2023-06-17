from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

#Cream o instanta a clasei Scraper
url = "https://www.medlife.ro/cariere/lista-joburi"
scraper = Scraper(url)
rules = Rules(scraper)

#Luam numarul total de joburi
totalJobs = int(rules.getTag("div", {"class":"title-header-listing"}).find("p").text.split(" ")[0])

pageNumbers = [*range(0, totalJobs, 7 )]

company = {"company": "Medlife"}
finalJobs = list()

#Iteram prin fiecare pagina
for page in range(len(pageNumbers)):
    #Setam url-ul paginii
    pageurl = url + "/s/page/" + str(page)
    scraper.url = pageurl

    #Luam elementele de pe pagina
    elements = rules.getTags("div", {"class":"mc-hand-hover"})
    
    #Iteram prin fiecare element si luam informatiile
    for element in elements:
        id = uuid.uuid4()
        job_title = element.find("div", {"class":"card-title-joburi-detalii"}).find_all("div")[0].text
        job_link = element["onclick"].split("'")[1]
        city = element.find("div", {"class":"detaii-job"}).find_all("div")[0].text.strip()

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city
        })

#Afisam numarul total de joburi
print(json.dumps(finalJobs, indent=4))

#Incarcam datele in baza de date
loadingData(finalJobs, company.get("company"))