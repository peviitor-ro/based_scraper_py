from scraper_peviitor import Scraper, Rules, loadingData
import uuid

#Aici se creeaza o instanta a clasei Scraper
scraper = Scraper("https://jobs.enel.com/en_US/careers/JobOpeningsRomania")

rules = Rules(scraper)

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
        company = "Enel"
        country = "Romania"
        city = "Romania"

        print(job_title + " -> " + city)

        finaljobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city
        })

    try:
        #Daca exista butonul de next, extraem link-ul si il punem in url-ul scraper-ului
        nextPageLink = nextPage["href"]
    except:
        break
   
    scraper.url = nextPageLink
#Afisam numarul total de joburi
print("Total jobs: " + str(len(finaljobs)))

#Incarcam datele in baza de date
loadingData(finaljobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", "Enel")



    