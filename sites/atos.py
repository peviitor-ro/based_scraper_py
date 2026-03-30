from scraper.Scraper import Scraper
from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty, remove_diacritics
import time

_counties = GetCounty()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

def fetch_with_retry(scraper, url, max_retries=3, delay=5):
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

def get_aditional_city(url):
    scraper = Scraper()
    scraper.set_headers(headers)
    fetch_with_retry(scraper, url)
    locations = scraper.find_all("span", {"class": "jobGeoLocation"})

    cities = []
    counties = []

    for location in locations:
        city = remove_diacritics(translate_city(location.text.split(",")[0].strip()))
        county = _counties.get_county(city)

        if county:
            cities.append(city)
            counties.extend(county)

    return list(set(cities)), list(set(counties))


url = "https://jobs.atos.net/go/Jobs-in-Romania/3686501/0/?q=&sortColumn=referencedate&sortDirection=desc"

company = "Atos"
finalJobs = list()

scraper = Scraper()
scraper.set_headers(headers)

try:
    fetch_with_retry(scraper, url)
except Exception as e:
    print(f"Warning: Could not connect to {url}: {e}")
    print("Publishing empty results.")
    publish_or_update(finalJobs)
    logoUrl = "https://rmkcdn.successfactors.com/a7d5dbb6/c9ab6ccb-b086-47f2-b25b-2.png"
    publish_logo(company, logoUrl)
    show_jobs(finalJobs)
    exit(0)

totalJobs = int(
    scraper.find("span", {"class": "paginationLabel"}).find_all("b")[-1].text.strip()
)

paginate = [*range(0, totalJobs, 50)]

jobs = scraper.find("table", {"id": "searchresults"}).find("tbody").find_all("tr")

for page in paginate:

    for job in jobs:
        job_title = job.find("a").text.strip()
        job_link = "https://jobs.atos.net" + job.find("a").get("href")
        city = translate_city(
            job.find("span", {"class": "jobLocation"}).text.split(",")[0].strip()
        )
        county = _counties.get_county(city)

        job_element = {
            "job_title": job_title,
            "job_link": job_link,
            "country": "Romania",
            "city": [city],
            "county": county,
            "company": company,
        }

        if not county:
            city, county = get_aditional_city(job_link)
            job_element["city"] = city
            job_element["county"] = county

        finalJobs.append(job_element)

    url = f"https://jobs.atos.net/go/Jobs-in-Romania/3686501/{page}/?q=&sortColumn=referencedate&sortDirection=desc"
    fetch_with_retry(scraper, url)
    jobs = scraper.find("table", {"id": "searchresults"}).find("tbody").find_all("tr")

publish_or_update(finalJobs)
logoUrl = "https://rmkcdn.successfactors.com/a7d5dbb6/c9ab6ccb-b086-47f2-b25b-2.png"
publish_logo(company, logoUrl)

show_jobs(finalJobs)
