from urllib.parse import urljoin

from scraper.Scraper import Scraper
from utils import translate_city, publish_or_update, publish_logo, show_jobs, get_jobtype
from getCounty import GetCounty

_counties = GetCounty()
url = "https://jobdetails.nestle.com/search/jobs?q=Romania"
scraper = Scraper()
job_scraper = Scraper()
scraper.get_from_url(url)

company = {"company": "Nestle"}
finalJobs = list()

elements = scraper.find_all("tr", {"class": "data-row"})
pagination_label = scraper.find("span", {"class": "paginationLabel"})
total_jobs = len(elements)
if pagination_label:
    try:
        total_jobs = int(
            pagination_label.find_all("b")[-1].get_text(strip=True).replace(",", "")
        )
    except (AttributeError, IndexError, ValueError):
        pass

startrow = 0

while True:
    elements = scraper.find_all("tr", {"class": "data-row"})

    if not elements:
        break

    for element in elements:
        link = element.find("a", {"class": "jobTitle-link"})
        job_title = link.text.strip()
        job_link = urljoin("https://jobdetails.nestle.com", link["href"])

        job_scraper.get_from_url(job_link)
        description = job_scraper.find("span", {"itemprop": "description"})
        description_text = (
            description.get_text(" ", strip=True).lower() if description else ""
        )
        description_text = description_text.replace("hibridă", "hybrid").replace(
            "hibrida", "hybrid"
        )
        remote = get_jobtype(description_text)
        if not remote and "work from home" in description_text:
            remote = ["remote"]

        city = translate_city(
            element.find("span", {"class": "jobLocation"}).text.split(",")[0].strip()
        )
        county = _counties.get_county(city)

        finalJobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
                "county": county,
                "remote": remote,
            }
        )

    startrow += 10
    if startrow >= total_jobs:
        break
    scraper.get_from_url(f"{url}&startrow={startrow}")

show_jobs(finalJobs)

publish_or_update(finalJobs)

logo_url = "https://www.nestle.com/themes/custom/da_vinci_code/logo.svg"
publish_logo(company.get("company"), logo_url)
show_jobs(finalJobs)
