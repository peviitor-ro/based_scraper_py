from scraper_peviitor import Scraper, Rules, loadingData, ScraperSelenium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import uuid 
import json
import os

#Folosim ScraperSelenium deoarece paginatia se face cu ajutorul unui buton
scraper = ScraperSelenium("https://www.autonom.ro/cariere")
scraper.get()

#Asteptam sa se incarce cookie-ul
scraper.wait(EC.presence_of_element_located((By.CLASS_NAME, 'autonom_gdpr_cookie_bar_accept')))

#Acceptam cookie-ul
cookieBtn = scraper.find_element(By.CLASS_NAME, 'autonom_gdpr_cookie_bar_accept')
scraper.click(cookieBtn)

#Asteptam sa se incarce butonul de load more
moreJobsBtn = scraper.find_element(By.ID, 'loadMore')
scraper.driver.execute_script("arguments[0].scrollIntoView();", moreJobsBtn)

#Daca butonul de load more este afisat, atunci il apasam
while moreJobsBtn.is_displayed():
    scraper.click(moreJobsBtn)
    time.sleep(2)
else:
    print("No more jobs")

#Obtinem DOM-ul
dom = scraper.getDom()

#Incarcam DOM-ul in BeautifulSoup
scraper = Scraper()
scraper.soup = dom
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

#Salvam datele in fisierul json/autonome.json
with open("json/autonome.json", "w") as f:
    json.dump(finalJobs, f, indent=4)

#Incarcam datele in baza de date
apikey = os.environ.get('apikey')
loadingData(finalJobs, apikey, "Autonom")