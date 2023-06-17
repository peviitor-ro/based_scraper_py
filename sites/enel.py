from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

#Aici se creeaza o instanta a clasei Scraper
scraper = Scraper("https://jobs.enel.com/en_US/careers/JobOpeningsRomania")

rules = Rules(scraper)

company = {"company": "Enel"}
finaljobs = list()

while True:
    #Cautam joburile care au clasa article--result
    elements = rules.getTags("div", {"class":"article--result"})

    #Cautam butonul de next
    nextPage = rules.getTag("a", {"class":"paginationNextLink"})

    #Pentru fiecare job, extragem titlul, locatia si link-ul
    for element in elements:
        id = uuid.uuid4()
        job_title = element.find("h3").text.strip()
        job_link = element.find("a")["href"]

        finaljobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": "Romania"
        })

    try:
        #Daca exista butonul de next, extraem link-ul si il punem in url-ul scraper-ului
        nextPageLink = nextPage["href"]
    except:
        break
   
    scraper.url = nextPageLink
#Afisam numarul total de joburi
print(json.dumps(finaljobs, indent=4))

#Incarcam datele in baza de date
loadingData(finaljobs, company.get("company"))



    