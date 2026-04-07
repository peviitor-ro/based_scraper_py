from scraper.Scraper import Scraper
from utils import create_job, show_jobs, publish_or_update, publish_logo
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://www.wtb.ro/category/careers/"

company = "WTB"
finalJobs = list()

scraper = Scraper()

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

try:
    fetch_with_retry(scraper, url)
except Exception as e:
    print(f"Warning: Could not fetch from {url}: {e}")

page = 1

try:
    jobs = scraper.find_all(
        "h3", {"class": "t-entry-title h5"}
    )
except Exception as e:
    print(f"Warning: Could not parse jobs: {e}")
    jobs = []

while jobs:
    for job in jobs:
        job_title = job.text.replace("JOB:", "").strip()
        job_link = job.find("a").get("href")

        finalJobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                company=company,
                country="Romania",
                city="Bucuresti",
                county="Bucuresti",
            )
        )

    page += 1
    try:
        fetch_with_retry(scraper, url + f"?%&upage={page}")
        jobs = scraper.find_all( "h3", {"class": "t-entry-title h5"})
    except Exception as e:
        print(f"Warning: Could not fetch page {page}: {e}")
        break

publish_or_update(finalJobs)
publish_logo(company, "https://www.wtb.ro/wp-content/uploads/2018/04/logoblack.svg")
show_jobs(finalJobs)