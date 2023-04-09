#TODO: De verificat cand sunt joburi noi

from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json 
import os 

#Cream o instanta de tip Scraper
scraper = Scraper("https://cariere.romstal.ro/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_location=&optionsFacetsDD_department=")
rules = Rules(scraper)

#Luam toate joburile
jobs = rules.getTags('li', {'class': 'job-tile'})

finalJobs = list()

#Pentru fiecare job luam titlul, linkul, compania, tara si orasul
for job in jobs:
    id = uuid.uuid4()
    job_title = job.find('a', {"class":"jobTitle-link"}).text.strip()
    job_link ="https://cariere.romstal.ro" + job.find('a', {"class":"jobTitle-link"})['href']
    company = "Romstal"
    country = "Romania"
    city = job.find('div', {"class":"location"}).find('div').text.split(',')[0].strip()

    if "SECTOR" in city:
        city = "Bucharest"

    print(job_title + " " + city)

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

#Salvam datele in fisierul json
with open('json/romstal.json', 'w') as f:
    json.dump(finalJobs, f, indent=4)

#Incarcam datele in baza de date
apikey = os.environ.get('apikey')
loadingData(finalJobs, apikey, "Romstal")