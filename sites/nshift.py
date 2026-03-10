from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
import requests

company = "nShift"
url = "https://careers.nshift.com/jobs"

response = requests.get(url)
scraper = Scraper(response.text, "html.parser")

jobs = []

job_elements = scraper.find_all("a", href=lambda x: x and "/jobs/" in x and "locations" not in x)

target_locations = ["Bucharest", "Brasov", "Cluj-Napoca", "București"]

for job_element in job_elements:
    try:
        title_elem = job_element.find("span", class_="text-block-base-link")
        if not title_elem:
            continue
        
        job_title = title_elem.text.strip()
        job_link = job_element.get("href")
        
        spans = job_element.find_all("span")
        
        location_text = None
        for i, span in enumerate(spans):
            span_text = span.text.strip()
            for target in target_locations:
                if target.lower() in span_text.lower():
                    location_text = span_text
                    break
            if location_text:
                break
        
        if not location_text:
            continue
            
        city = location_text.split(",")[0].strip()
        
        if "București" in city:
            city = "Bucharest"
        elif "Brașov" in city:
            city = "Brasov"
            
        city = translate_city(city)
        
        jobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                city=city,
                country="Romania",
                company=company,
            )
        )
    except Exception as e:
        continue

publish_or_update(jobs)

publish_logo(
    company,
    "https://images.teamtailor-cdn.com/images/s3/teamtailor-production/logotype-v1/image_uploads/6b643d11-63d9-466b-bdc1-dfbab828db19/original.png",
)
show_jobs(jobs)
