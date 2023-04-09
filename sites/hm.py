from time import sleep
import json
from scraper_peviitor import Scraper, Rules, ScraperSelenium, loadingData
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import os
import uuid

# Se creează o instanță a clasei ScraperSelenium pentru a accesa site-ul
scraper = ScraperSelenium("https://career.hm.com/search/?l=cou%3Aro")

# Se accesează site-ul
scraper.get()

# Se așteaptă apariția butonului pentru acceptarea cookies
cookieBtn = scraper.wait(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))

# Se dă click pe butonul pentru acceptarea cookies
cookieBtn = scraper.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
scraper.click(cookieBtn)

# Se așteaptă încărcarea completă a paginii
scraper.wait(EC.presence_of_element_located((By.CLASS_NAME, "load-more-heading")))

# Se adună numărul total de rezultate și numărul de rezultate afișate pe pagină
totalResults = int(
    scraper.find_element(By.CLASS_NAME, "load-more-heading").get_attribute("data-total")
)
step = int(
    scraper.find_element(By.CLASS_NAME, "load-more-heading").get_attribute("data-items-shown")
)

# Se calculează numărul de click-uri necesare pentru a afișa toate rezultatele
butonCountClick = [i for i in range(step, totalResults, step)]
print(len(butonCountClick))

# Se accesează butonul "Load More Results" și se face click de un număr de ori
# corespunzător numărului de click-uri necesare
button = scraper.find_element(By.CLASS_NAME, "load_more_cta")
for click in range(len(butonCountClick)):
    scraper.click(button)
    sleep(3)

# Se preia codul HTML al paginii
dom = scraper.getDom()

# Se închide browser-ul
scraper.close()

# Se creează o nouă instanță a clasei Scraper pentru a prelucra codul HTML
scraper = Scraper()
scraper.soup = dom
rules = Rules(scraper)

# Se extrag job-urile din pagină și se salvează într-un dicționar
jobs = rules.getTags("a", {"class": "jobs-card--link"})
idx = 0
finaljobs = list()
for job in jobs:
    scraper.url = job["href"]
    rules = Rules(scraper)

    id = str(uuid.uuid4())
    job_title = rules.getTag("div", {"class": "text--title-large"}).text.replace("\n", "").replace("\t", "").replace("Stores", "")
    job_link = job["href"]
    company = "HM"
    country = "Romania"
    city = rules.getTag("div", {"class": "jobs-card__group-td"}).find("b").text
    
    finaljobs.append({
        "id": id,
        "job_title": job_title,
        "job_link": job_link,
        "company": company,
        "country": country,
        "city": city,
    })

    print(finaljobs[idx])
    idx += 1
    sleep(3)

# Se afișează numărul de job-uri extrase
print(len(finaljobs))

# Se salvează dicționarul cu job-uri într-un fișier JSON
with open("json/hm.json", "w") as f:
    json.dump(finaljobs, f, indent=4)

apikey = os.environ.get("apikey")

loadingData(finaljobs, apikey, "HM")







