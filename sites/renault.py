from scraper_peviitor import Scraper, Rules, ScraperSelenium, loadingData
from selenium.webdriver.common.by import By

import time
import json
import uuid
import os

#folosim selenium deoarece joburile sunt incarcate prin ajax
scraper = ScraperSelenium("https://alliancewd.wd3.myworkdayjobs.com/ro-RO/renault-group-careers?locationCountry=f2e609fe92974a55a05fc1cdc2852122&workerSubType=62e55b3e447c01871e63baa4ca0f9391&workerSubType=62e55b3e447c01140817bba4ca0f9891")
scraper.get()

#asteptam sa se incarce Siteul
time.sleep(10)

#se creaza o instanta a clasei Scraper
page = Scraper()
rules = Rules(page)

finaljobs = list()
idx = 0

#se extrag joburile
while True:
    try:
        #se extrage dom-ul
        dom = scraper.getDom()
        #se seteaza dom-ul pentru scraperul de pe pagina
        page.soup = dom
        #se cauta joburile care au clasa css-19uc56f
        elements = rules.getTags("li", {"class":"css-1q2dra3"})

        #pentru fiecare job, se extrage titlul, link-ul, compania, tara si orasul
        for element in elements:
            id = uuid.uuid4()
            job_title = element.find("a").text
            job_link = "https://alliancewd.wd3.myworkdayjobs.com" + element.find("a")["href"]
            company = "Renault"
            country = "Romania"
            city = element.find("li", {"class":"css-h2nt8k"})

            if "_" in city.text:
                city = "Romania"
            else:
                city = city.text

            finaljobs.append({
                "id": str(id),
                "job_title": job_title,
                "job_link": job_link,
                "company": company,
                "country": country,
                "city": city
            })

            print(job_title + " " + city)


        #se cauta butonul de next
        nextBtn = scraper.find_element(By.XPATH, "//button[@aria-label='next']")
        #se da click pe butonul de next
        scraper.driver.execute_script("arguments[0].scrollIntoView();", nextBtn)
        scraper.click(nextBtn)
        time.sleep(5)
        
        print("Next")
    except Exception as e:
        print("No more pages")
        break

#se afiseaza numarul de joburi gasite
print(len(finaljobs))

#se salveaza joburile in fisierul renault.json
with open("json/renault.json", "w") as f:
    json.dump(finaljobs, f, indent=4)


apikey = os.environ.get("apikey")

loadingData(finaljobs, apikey, "Renault")
