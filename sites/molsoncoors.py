from scraper.Scraper import Scraper
from utils import (
    translate_city,
    acurate_city_and_county,
    publish_or_update,
    publish_logo,
    show_jobs,
)
from getCounty import GetCounty
from math import ceil
import time

_counties = GetCounty()
url = "https://jobs.molsoncoors.com/MolsonCoors_GBSRomania/search/?q=Romania&startrow=1"

company = {"company": "MolsonCoors"}
finalJobs = list()

scraper = Scraper()


def fetch_with_retry(scraper, url, max_retries=2, delay=3):
    for attempt in range(max_retries):
        try:
            scraper.get_from_url(url, timeout=30, verify=False)
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed for {url}, retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2
    print(f"Warning: Could not fetch from {url} after {max_retries} attempts")
    return False


if not fetch_with_retry(scraper, url):
    print("Warning: Could not connect to Molson Coors jobs site, exiting with empty results")

print("Jobs found:", len(finalJobs))

publish_or_update(finalJobs)

logoUrl = "https://rmkcdn.successfactors.com/e2403c2e/b8073680-5e29-45a9-8c61-4.png"
publish_logo(company.get("company"), logoUrl)
show_jobs(finalJobs)
