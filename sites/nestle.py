from scraper_peviitor import Scraper, Rules, loadingData
import time
import json
import uuid
import os

#Se creeaza o instanta a clasei Scraper
scraper = Scraper("https://www.nestle.ro/jobs/search-jobs?keyword=Romania&country=&location=&career_area=All")
rules = Rules(scraper)

finalJobs = list()

#Se extrag joburile
while True:
    #Se cauta joburile care au clasa jobs-card
    elements = rules.getTags("div", {"class":"jobs-card"})

    #Pentru fiecare job, se extrage titlul, link-ul, compania, tara si orasul
    for element in elements:
        id = uuid.uuid4()
        job_title = element.find("a").text.replace("\t", "").replace("\r", "").replace("\n", "").replace("  ", "")
        job_link = element.find("a")["href"]
        company = "Nestle"
        country = "Romania"
        city = element.find("div", {"class":"jobs-location"}).text.split(",")[0]

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city
        })

        print(job_title)

    #Se cauta butonul de next
    domain = "https://www.nestle.ro/jobs/search-jobs"
    try:
        #Daca exista butonul de next, se extrage link-ul si se pune in url-ul scraper-ului
        nextPage = rules.getTag("div", {"class":"pager__item--next"})
        nextPageLink = nextPage.find("a")["href"]
        scraper.url = domain + nextPageLink
    except:
        break

    time.sleep(3)


#Afiseaza numarul de joburi gasite
print(len(finalJobs))

#Se salveaza joburile in fisierul nestle.json
with open("json/nestle.json", "w") as f:
    json.dump(finalJobs, f, indent=4)

apikey = os.environ.get("apikey")

loadingData(finalJobs, apikey, "Nestle")
