from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import time
import json
import os

#Cream o instanta a clasei Scraper
scraper = Scraper("https://cariere.otpbank.ro/Posturi")
rules = Rules(scraper)

#Cautam numarul total de joburi
number_of_jobs = int(rules.getTag("div", {"class": "page-subtitle-counter"}).text.split(" ")[0])

#Cream o lista cu numerele de joburi de 10 in 10
pages = [*range(1, number_of_jobs // 1, 10)]

finalJobs = list()

#Pentru fiecare numar din lista, extragem joburile
for page in range(len(pages)):
    #setam link-ul paginii
    page_url = f"https://cariere.otpbank.ro/Posturi?page={page + 1}"
    scraper.url = page_url

    #Cautam elementele care contin joburile si locatiile
    elements = rules.getTags("div", {"class": "vacancy-item"})

    #Pentru fiecare job, extragem titlul, link-ul, compania, tara si orasul
    for element in elements:
        id = uuid.uuid4()
        job_title = element.find("h2").find("a").text
        job_link = "https://cariere.otpbank.ro" + element.find("h2").find("a")["href"]
        company = "OTP Bank"
        country = "Romania"
        try:
            city = element.find("span", {"class": "more"}).text.split("-")[0].strip()
        except:
            city = city = element.find("span", {"class": "more"}).text
        print(city + " " + job_title)

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city
        })

    time.sleep(3)

#Afisam numarul total de joburi gasite
print(len(finalJobs))

#Salvam joburile in fisierul otpbank.json
with open("json/otpbank.json", "w") as f:
    json.dump(finalJobs, f, indent=4)

apikey = os.environ.get("apikey")

loadingData(finalJobs, apikey, "OTP Bank")