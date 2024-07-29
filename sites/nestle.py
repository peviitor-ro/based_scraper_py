from scraper.Scraper import Scraper
from utils import translate_city, publish_or_update, publish_logo, show_jobs, get_jobtype
from getCounty import GetCounty

_counties = GetCounty()
url = "https://www.nestle.ro/jobs/search-jobs?keyword=Romania&country=&location=&career_area=All"
scraper = Scraper()
scraper.get_from_url(url)

company = {"company": "Nestle"}
finalJobs = list()

while True:
    elements = scraper.find_all("div", {"class": "jobs-card"})

    for element in elements:
        job_title = (
            element.find("a")
            .text.replace("\t", "")
            .replace("\r", "")
            .replace("\n", "")
            .replace("  ", "")
        )
        job_link = element.find("a")["href"]
        remote = get_jobtype(element.find("div", {"class": "jobs-type"}).text)
        city = translate_city(
            element.find("div", {"class": "jobs-location"}).text.split(",")[0]
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

    domain = "https://www.nestle.ro/jobs/search-jobs"
    try:
        nextPage = scraper.find("div", {"class": "pager__item--next"})
        nextPageLink = nextPage.find("a")["href"]
        scraper.get_from_url(domain + nextPageLink)
    except:
        break

show_jobs(finalJobs)

publish_or_update(finalJobs)

logo_url = "https://www.nestle.com/themes/custom/da_vinci_code/logo.svg"
publish_logo(company.get("company"), logo_url)
show_jobs(finalJobs)
