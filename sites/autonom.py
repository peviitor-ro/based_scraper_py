from scraper_peviitor import Scraper, Rules, loadingData
import uuid 

url = "https://www.autonom.ro/cariere"

scraper = Scraper(url)
rules = Rules(scraper)

#Obtinem toate joburile
jobs = rules.getTags('a', {'class': 'box-listing-job'})

finalJobs = list()

#Pentru fiecare job, extragem datele si le adaugam in lista finalJobs
for job in jobs:
    id = uuid.uuid4()
    job_title = job.find('p', {"class":"nume-listing-job"}).text
    job_link = job['href']
    company = "Autonom"
    country = "Romania"
    citys = job.find_all('span', {"class":"locatie-job"})

    for city in citys:
        city = city.text

        print(job_title + " -> " + city)
        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city
        })

#Afisam numarul de joburi
print("Total jobs: " + str(len(finalJobs)))

#Incarcam datele in baza de date
loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", "Autonom")