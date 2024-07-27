from scraper.Scraper import Scraper
from utils import show_jobs, publish_or_update, publish_logo, translate_city, get_jobtype
from getCounty import GetCounty

_counties = GetCounty()
company = "qualitest"
# url = "https://jobs.workable.com/api/v1/jobs?location=Romania&query=qualitest"
row = 0
url = "https://careers.qualitestgroup.com/search/?q=&locationsearch=Romania&searchby=location&d=10&startrow=0"

scraper = Scraper()
scraper.get_from_url(url)

jobs = scraper.find("table", {"id": "searchresults"}).find("tbody").find_all("tr")
  
final_jobs = []

while len(jobs) > 0:
    for job in jobs:
        job_title = job.find("a", {"class": "jobTitle-link"}).text
        job_link = "https://careers.qualitestgroup.com/" + \
            job.find("a", {"class": "jobTitle-link"}).get("href")
        remote = get_jobtype(job_title.lower())
        city = translate_city(job.find("span", {"class": "jobLocation"}).text.split(",")[0].strip())

        if city:
            county = _counties.get_county(city)
        else:
            county = []

        final_jobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "remote": remote,
                "country": "Romania",
                "company": company,
                "city": city,
                "county": county,
            }
        )
    
    row += 25
    url = "https://careers.qualitestgroup.com/search/?q=&locationsearch=Romania&searchby=location&d=10&startrow=" + str(row)
    scraper.get_from_url(url)
    jobs = scraper.find("table", {"id": "searchresults"}).find("tbody").find_all("tr")

publish_or_update(final_jobs)

logourl = "https://static.otta.com/uploads/images/company-logos/12608-VWKbfxnEMQpPk5I5aK7oBSr36vMu7zE5VwQkcV6-KE4.png"
publish_logo(company, logourl)

show_jobs(final_jobs)
