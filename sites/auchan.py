from scraper_peviitor import Scraper, Rules, loadingData

import uuid
import re
import json
import os 
import subprocess

import asyncio

#Folosim ScraperSelenium pentru a putea naviga pe pagini
url = "https://cariere.auchan.ro"

print(os.path.dirname(os.path.abspath(__file__)))

async def getHtml():


    process = subprocess.run(["wget", url , "--no-check-certificate", "-O",f"{os.path.dirname(os.path.abspath(__file__))}/auchan.html"], capture_output=True)


loop = asyncio.get_event_loop()
loop.run_until_complete(getHtml())

file = open(f"{os.path.dirname(os.path.abspath(__file__))}/auchan.html", "r")
doomBody = file.read()

print(doomBody)

# print(process.stdout.decode('utf-8'))
# scraper = Scraper()
# scraper.session.verify = False
# scraper.url = url
# rules = Rules(scraper)

# doomBody = rules.getTag("body")
# regex = re.compile(r'vmCfg = {(.*)}')

# jobs = re.search(regex, doomBody.prettify()).group(1)

# jobs = json.loads("{" + jobs + "}")

# finaljobs = list()

# for job in jobs.get("PositionList"):
#     id = uuid.uuid4()
#     job_title = job.get("PositionName")
#     job_link = "https://cariere.auchan.ro/" + f"Position/Details?id={job.get('PositionId')}"
#     company = "Auchan"
#     country = "Romania"
#     city = job.get("CityList")
    
#     print(job_title + " -> " + city)
#     finaljobs.append({
#         "id": str(id),
#         "job_title": job_title,
#         "job_link": job_link,
#         "company": company,
#         "country": country,
#         "city": city
#     })

# #Afisam numarul total de joburi
# print("Total jobs: " + str(len(finaljobs)))

# #Incarcam datele in baza de date
# loadingData(finaljobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", "Auchan")