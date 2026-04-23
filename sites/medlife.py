import requests
from bs4 import BeautifulSoup
from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty
from urllib.parse import urljoin
import re

_counties = GetCounty()
company_name = "Medlife"
base_url = "https://www.ejobs.ro/company/medlife/57255"

session = requests.Session()
session.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
)

finalJobs = []
base_url_full = "https://www.ejobs.ro"

cities = [
    "București", "Bucuresti", "Cluj-Napoca", "Timișoara", "Iași", "Brașov", 
    "Constanța", "Craiova", "Ploiești", "Sibiu", "Galați", "Pitești", 
    "Bacău", "Arad", "Oradea", "Suceava", "Drobeta", 
    "Târgu Mureș", "Botoșani", "Voluntari", "Chitila", "Pantelimon",
    "Floresti", "Zalău", "Deva", "Hunedoara", "Mioveni", "Popesti-Leordeni",
    "Focsani", "Baia Mare", "Zalău", "Tulcea", "Alexandria", "Caracal"
]

def extract_jobs_from_response(response_text):
    jobs = []
    soup = BeautifulSoup(response_text, "html.parser")
    
    job_links = soup.find_all("a", href=re.compile(r"/user/locuri-de-munca/"))
    seen_links = set()
    
    for link in job_links:
        href = link.get("href")
        if not href or href in seen_links:
            continue
        seen_links.add(href)
        
        job_link = urljoin(base_url_full, href)
        
        parent = link.parent
        while parent:
            h2 = parent.find("h2")
            if h2:
                break
            parent = parent.parent
        
        if not h2:
            h2 = link.find_previous("h2")
        
        job_title = h2.text.strip() if h2 and h2.text else None
        if not job_title:
            continue
        
        container = link.find_parent()
        city = "București"
        while container:
            text = container.get_text()
            for c in cities:
                if c.lower() in text.lower():
                    city = translate_city(c)
                    break
            if city != "București":
                break
            container = container.parent if container.parent else None
        
        county = _counties.get_county(city)
        
        jobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "company": company_name,
                "country": "Romania",
                "city": city,
                "county": county,
            }
        )
    
    return jobs

for page in range(1, 5):
    page_url = base_url if page == 1 else f"{base_url}?page={page}"
    response = session.get(page_url)
    
    if response.status_code != 200:
        break
    
    jobs_on_page = extract_jobs_from_response(response.text)
    if not jobs_on_page:
        break
    
    finalJobs.extend(jobs_on_page)
    print(f"Page {page}: found {len(jobs_on_page)} jobs")

seen = set()
unique_jobs = []
for job in finalJobs:
    key = (job["job_title"], job["job_link"])
    if key not in seen:
        seen.add(key)
        unique_jobs.append(job)

print(f"Total unique jobs: {len(unique_jobs)}")

publish_or_update(unique_jobs)

logo_url = "https://rmkcdn.successfactors.com/d1204926/7da4385b-5dfa-431c-9772-9.png"
publish_logo(company_name, logo_url)
show_jobs(unique_jobs)