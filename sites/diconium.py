from scraper.Scraper import Scraper
from utils import (publish, publish_logo, show_jobs)
import json

url = "https://jobs.diconium.com/en/api/filter/offers-content-category/diconium-jobs-en"

company = "Diconium"
finalJobs = list()

post_data = {"offerIds": ["19aaf964-f367-4616-b6ce-d3ebd5fa0e49", "19b7344f-e2b2-4d2d-bc8b-215fd89ac43b", "21d39351-ca29-4685-95ba-eba1e2ec18ed", "2b7fd0ce-8fa7-4358-8169-8a96fbe4d838", "34034848-15c7-47fb-82cc-74c0387f8a1c", "3f834b44-bbb9-410c-a2b1-edc123ce525c", "3f9db239-9a34-4b4a-b6f5-b7d6524ecc45", "4021a576-a4bc-400f-bbb5-9145c954d3a8", "4c4a008e-9185-4e31-9a10-b43a4b3bdcc7",
                          "4f23b6c1-a083-4a41-b3b6-8e894d95e969", "5e1c0ed8-33c9-473e-9f9e-46053f5622d7", "801e3d35-9a53-4834-8365-79e9c0fe1c25", "907ec6c3-8394-4a5d-84df-ba625a11f7fb", "a572230f-b12d-44d8-ad87-8aae30ab9f1a", "be8abc95-1072-43c5-8259-2c67342aae9a", "db9e5466-400f-4f20-8d70-25f5775fcaca", "ed0356ac-bfaa-4d7a-a96b-f33f46f2522a"], "categoryId": "59954e8a-f49e-5d4a-b37b-6177b94e1bb4", "page": 1}

scraper = Scraper()
html = scraper.post(url, json.dumps(post_data)).json().get("html")
scraper.__init__(html, "html.parser")
jobs  = scraper.find_all("a")


for job in jobs:
        location = job.find("div", {"class": "p cityNames"}).text.strip()
        if location == "Bucharest":
            job_title = job.find("div", {"class":"h3"}).text.strip()
            job_link = job.get("href")
            city = location

            finalJobs.append({
                "job_title": job_title,
                "job_link": job_link,
                "company": company,
                "country": "Romania",
                "city": "Bucuresti"
            })

for version in [1,4]:
    publish(version, company, finalJobs, 'APIKEY')

logoUrl = "https://jobs.diconium.com/en/uploads/1623/settings/companies/diconium-jobs-en-96-6059ae9f8dd12.png"
publish_logo(company, logoUrl)
show_jobs(finalJobs)
