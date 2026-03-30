from playwright.sync_api import sync_playwright
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty
import re

_counties = GetCounty()
company = {"company": "Medicover"}


def scrape_ejobs():
    jobs_list = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto("https://www.ejobs.ro/company/medicover/3862", wait_until="networkidle")
        page.wait_for_timeout(3000)
        
        job_cards = page.query_selector_all(".job-card-wrapper")
        
        for card in job_cards:
            try:
                title_elem = card.query_selector(".job-card-content-middle__title")
                job_title = title_elem.inner_text().strip() if title_elem else ""
                
                link_elem = card.query_selector(".job-card-content-middle__title a")
                job_link = "https://www.ejobs.ro" + link_elem.get_attribute("href") if link_elem else ""
                
                info_text = card.inner_text()
                
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
        
        browser.close()
    
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
