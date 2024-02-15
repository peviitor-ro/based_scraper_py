from scraper_peviitor import Scraper
from utils import publish, publish_logo, show_jobs
from getCounty import get_county, remove_diacritics

data = {
    "locations": [],
    "workAreas": [],
    "contractType": [],
    "fulltext": "Romania",
    "order_by": "relevance",
    "page": 1,
}
url = "https://career.hm.com/wp-json/hm/v1/sr/jobs/search?_locale=user"

# Se creează o instanță a clasei ScraperSelenium pentru a accesa site-ul
scraper = Scraper()
jobs = scraper.post(url, data).json()

company = {"company": "HM"}
finalJobs = list()

# din obiectul json extragem lista de job-uri
while jobs.get("jobs"):
    for job in jobs.get("jobs"):
        job_title = job.get("title")
        job_link = job.get("permalink")
        city = remove_diacritics(job.get("city"))
        county = get_county(city)

        finalJobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
                "county": county,
            }
        )

    # Se trece la pagina următoare
    data["page"] += 1
    jobs = scraper.post(url, data).json()

publish(4, company.get("company"), finalJobs, "APIKEY")

logourl = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/H%26M-Logo.svg/709px-H%26M-Logo.svg.png?20130107164928"
publish_logo(company.get("company"), logourl)

show_jobs(finalJobs)
