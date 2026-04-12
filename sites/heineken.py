from scraper.Scraper import Scraper
from utils import (
    translate_city,
    acurate_city_and_county,
    publish_or_update,
    publish_logo,
    show_jobs,
)
from getCounty import GetCounty, remove_diacritics
import time

_counties = GetCounty()
scraper = Scraper()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

def fetch_with_retry(scraper, url, max_retries=5, delay=10):
    last_error = None
    for attempt in range(max_retries):
        try:
            scraper.get_from_url(url, timeout=30, verify=False)
            return True
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed for {url}, retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2
    if last_error:
        raise last_error

jobsFound = True
startRow = 0

company = {"company": "Heineken"}
finalJobs = list()

acurate_city = acurate_city_and_county(
    Mures={"city": "Satu Mare", "county": "Satu Mare"},
    Ciuc={"city": "Miercurea Ciuc", "county": "Harghita"},
)

scraper.set_headers(headers)

while jobsFound:
    url = f"https://careers.theheinekencompany.com/search/?createNewAlert=false&q=&optionsFacetsDD_country=RO&startrow={startRow}"
    fetch_with_retry(scraper, url)
    jobs = scraper.find_all("tr", {"class": "data-row"})
    
    if not jobs:
        jobsFound = False
        break
        
    for job in jobs:
        job_location_elem = job.find("span", {"class": "jobLocation"})
        if not job_location_elem:
            continue
            
        location_text = job_location_elem.text.strip()
        location_parts = [part.strip() for part in location_text.split(",")]
        
        if len(location_parts) < 2 or location_parts[-1] != "RO":
            jobsFound = False
            break

        job_title = job.find("span", {"class": "jobTitle"}).text.strip()
        job_link = "https://careers.theheinekencompany.com" + job.find(
            "a", {"class": "jobTitle-link"}
        ).get("href")
        
        city_raw = location_parts[0]
        city = translate_city(remove_diacritics(city_raw))

        job = {
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
        }

        if acurate_city.get(city):
            job["city"] = acurate_city.get(city).get("city")
            job["county"] = acurate_city.get(city).get("county")
        else:
            job["city"] = city
            job["county"] = _counties.get_county(city)

        finalJobs.append(job)

    startRow += 25

publish_or_update(finalJobs)

logoUrl = "https://agegate.theheinekencompany.com/assets/img/logo-corporate.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
