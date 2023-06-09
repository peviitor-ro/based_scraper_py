from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

#Cream o instanta a clasei Scraper
url = "https://www.selgros.ro/posturi-disponibile?p=1"
scraper = Scraper(url)
rules = Rules(scraper)

#Obtinem numarul total de pagini
numberPages = int(rules.getTag("a", {"class": "last"}).find_all("span")[1].text)

company = {"company": "Selgros"}
finaljobs = list()

#Iteram prin fiecare pagina
for page in range(1, numberPages + 1):
    #Setam url-ul paginii curente
    url = "https://www.selgros.ro/posturi-disponibile?p=" + str(page)
    scraper.url = url

    #Luam toate joburile de pe pagina curenta
    jobs = rules.getTags("div", {"class": "text-content"})
    
    #Iteram prin fiecare job
    for job in jobs:
        id = uuid.uuid4()
        job_title = job.find("div", {"class":"title"}).text
        job_link = job.find("a")["href"]
        city = job.find("div", {"class":"type-location"}).text.split(",")[1]

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