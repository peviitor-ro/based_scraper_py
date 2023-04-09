from time import sleep
import json
from scraper_peviitor import ScraperSelenium, loadingData
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import os
import uuid

# Inițializăm un obiect ScraperSelenium cu URL-ul dorit și obiectul Chrome
scraper = ScraperSelenium("https://jobs.vodafone.com/careers?query=Romania&pid=563018675157116&domain=vodafone.com&sort_by=relevance")
# Accesăm URL-ul
scraper.get()

# Așteptăm să apară butonul de cookie-uri și apoi îl accesăm
scraper.wait(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
cookieBtn = scraper.find_element(By.ID, "onetrust-accept-btn-handler")
scraper.click(cookieBtn)

# Extragem numărul total de rezultate de pe pagină
results = scraper.find_element(By.XPATH, '//*[@id="pcs-body-container"]/div[2]/div[1]/div/span/span/strong').text
results = results.replace(" open jobs.", "")
step = 10

# Generăm o listă cu numerele de click-uri necesare pentru a accesa toate job-urile
butonCountClick = [i for i in range(step, int(results), step)]

print(len(butonCountClick))

# Parcurgem butoanele și le accesăm succesiv, apoi așteptăm ca paginile să se încarce complet
for click in range(len(butonCountClick)):
    scraper.wait(EC.presence_of_element_located((By.CLASS_NAME, 'show-more-positions')))
    button = scraper.find_element(By.CLASS_NAME, 'show-more-positions')
    scraper.driver.execute_script("arguments[0].scrollIntoView();", button)
    scraper.click(button)
    sleep(2)

# Extragem toate job-urile de pe pagină și le parcurgem succesiv, accesând fiecare în parte și extrăgând titlul și locația
jobs = scraper.find_elements(By.CLASS_NAME, "position-card")
idx = 0

print(len(jobs))

scraper.driver.execute_script("scroll(0, 0);")

finalJobs = list()

# Parcurgem job-urile și le salvăm într-o listă de dictionare
for job in jobs:
    sleep(2)
    #Pe fiecare job il deschidem si extragem datele precum titlul, link-ul, compania, tara si orasul
    try:
        scraper.driver.execute_script("arguments[0].scrollIntoView();", job)
        scraper.click(job)
        id = uuid.uuid4()
        job_title = scraper.find_elements(By.CLASS_NAME, "position-title")[idx].text
        job_link = scraper.driver.current_url
        company = "Vodafone"
        country = "Romania"
        city = scraper.find_elements(By.CLASS_NAME, "position-location")[idx].text.split(",")[0]

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city,
        })
        print(job_title + " " + city)

    except Exception as e:
        print(e)
        break
    idx += 1
    

#Afiseaza numarul de joburi gasite
print(len(finalJobs))

# Salvăm job-urile într-un fișier JSON
with open("json/vodafone.json", "w") as f:
    json.dump(finalJobs, f, indent=4)

apikey = os.environ.get('apikey')

loadingData(finalJobs, apikey, "Vodafone")