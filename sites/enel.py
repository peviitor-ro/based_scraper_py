from scraper_peviitor import Scraper, Rules
import time
import json

#Aici se creeaza o instanta a clasei Scraper
scraper = Scraper("https://jobs.enel.com/en_US/careers/JobOpeningsRomania")

rules = Rules(scraper)

finaljobs = dict()
idx = 0


while True:
    #Cautam joburile care au clasa article--result
    elements = rules.getTags("div", {"class":"article--result"})

    #Cautam butonul de next
    nextPage = rules.getTag("a", {"class":"paginationNextLink"})

    #Pentru fiecare job, extragem titlul, locatia si link-ul
    for element in elements:
        title = element.find("h3").text.replace("\t", "").replace("\r", "").replace("\n", "").replace("  ", "")
        location = "Romania"
        link = element.find("a")["href"]

        print(element.find("h3").text.replace("\t", "").replace("\r", "").replace("\n", ""))
        finaljobs[idx] = {"title": title, "location": location, "link": link}
        idx += 1

    try:
        #Daca exista butonul de next, extraem link-ul si il punem in url-ul scraper-ului
        nextPageLink = nextPage["href"]
    except:
        break
   
    scraper.url = nextPageLink

    time.sleep(3)

#Salvam joburile in fisierul enel.json
with open("enel.json", "w") as f:
    json.dump(finaljobs, f, indent=4)



    