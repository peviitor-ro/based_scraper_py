from scraper.Scraper import Scraper
from utils import show_jobs, translate_city, publish, publish_logo
from getCounty import get_county, remove_diacritics

url = "https://mingle.ro/api/boards/mingle/jobs?q=companyUid~eq~%22crowe%22&page=0&pageSize=100&sort=modifiedDate~DESC"
scraper = Scraper()
scraper.get_from_url(url, "JSON")

company = "Crowe"
jobs = list()

jobs_elements = scraper.markup.get("data").get("results")

for job in jobs_elements:
    job_title = job.get("jobTitle")
    job_link = "https://crowe.mingle.ro/en/apply/" + job.get("publicUid")
    cities = []
    counties = []

    if job.get("locations"):
        for location in job.get("locations"):
            city = translate_city(remove_diacritics(location.get("name")))
            county = get_county(city)

            if not county:
                city = city.replace(" ", "-")
                county = get_county(city)

            if county:
                cities.append(city)
                counties.append(county)
    else:
        cities = ["Bucuresti", "Timisoara", "Cluj-Napoca"]
        counties = ["Bucuresti", "Timis", "Cluj"]

    jobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": "Romania",
            "city": cities,
            "county": counties,
        }
    )


publish(4, company, jobs, "APIKEY")

logoUrl = "https://i.ytimg.com/vi/dTmm3WNIpnc/maxresdefault.jpg"
publish_logo(company, logoUrl)
show_jobs(jobs)
