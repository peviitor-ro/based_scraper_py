import requests
from bs4 import BeautifulSoup
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty
import re

_counties = GetCounty()
company = {"company": "Medicover"}


def scrape_ejobs():
    jobs_list = []
    
    url = "https://www.ejobs.ro/company/medicover/3862"
    response = requests.get(url, timeout=20)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    
    job_cards = soup.select(".job-card-wrapper")
    
    for card in job_cards:
        try:
            title_elem = card.select_one(".job-card-content-middle__title")
            job_title = title_elem.get_text(strip=True) if title_elem else ""
            
            link_elem = card.select_one(".job-card-content-middle__title a")
            job_link = "https://www.ejobs.ro" + link_elem.get("href") if link_elem else ""
            
            info_text = card.get_text()
            
            city = ""
            cities_to_check = ["București", "Pipera", "Cluj", "Iași", "Timișoara", "Brașov", "Constanța", "Craiova"]
            for city_name in cities_to_check:
                if city_name in info_text:
                    city = translate_city(city_name)
                    break
            
            counties = []
            if city:
                county = _counties.get_county(city) or []
                counties.extend(county)
            
            jobs_list.append({
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": [city] if city else [],
                "county": counties,
            })
        except Exception:
            continue
    
    return jobs_list


finalJobs = scrape_ejobs()

seen = set()
unique_jobs = []
for job in finalJobs:
    key = (job["job_title"], job["job_link"])
    if key not in seen:
        seen.add(key)
        unique_jobs.append(job)

finalJobs = unique_jobs

publish_or_update(finalJobs)

logo_url = "https://upload.wikimedia.org/wikipedia/commons/d/d7/Logo-medicover.png"
publish_logo(company.get("company"), logo_url)
show_jobs(finalJobs)
