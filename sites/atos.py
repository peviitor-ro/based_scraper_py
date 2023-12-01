from scraper.Scraper import Scraper
from utils import translate_city, publish, publish_logo, show_jobs
from getCounty import get_county, remove_diacritics


def get_aditional_city(url):
    scraper = Scraper()
    scraper.get_from_url(url)

    locations = scraper.find_all(
        'span', {'class': 'jobGeoLocation'})

    cities = []
    counties = []

    for location in locations:
        city = remove_diacritics(
            translate_city(
                location.text.split(',')[0].strip()
            )
        )
        county = get_county(city)

        if county and county not in counties:
            cities.append(city)
            counties.append(county)

    return cities, counties


url = "https://jobs.atos.net/go/Jobs-in-Romania/3686501/0/?q=&sortColumn=referencedate&sortDirection=desc"

company = "Atos"
finalJobs = list()

scraper = Scraper(url)
scraper.get_from_url(url)

totalJobs = int(scraper.find(
    "span", {"class": "paginationLabel"}).find_all("b")[-1].text.strip())

paginate = [*range(0, totalJobs, 50)]

jobs = scraper.find("table", {"id": "searchresults"}).find(
    "tbody").find_all("tr")

for page in paginate:

    for job in jobs:
        job_title = job.find("a").text.strip()
        job_link = "https://jobs.atos.net" + job.find("a").get("href")
        city = translate_city(
            job.find("span", {"class": "jobLocation"}).text.split(",")[0].strip())
        county = get_county(city)

        job_element = {
            "job_title": job_title,
            "job_link": job_link,
            "country": "Romania",
            "city": [city],
            "county": [county],
            "company": company
        }

        if not county:
            city, county = get_aditional_city(job_link)
            job_element["city"] = city
            job_element["county"] = county

        finalJobs.append(job_element)

    url = f"https://jobs.atos.net/go/Jobs-in-Romania/3686501/{page}/?q=&sortColumn=referencedate&sortDirection=desc"
    scraper.get_from_url(url)
    jobs = scraper.find("table", {"id": "searchresults"}).find(
        "tbody").find_all("tr")

for version in [1, 4]:
    publish(version, company, finalJobs, 'APIKEY')
logoUrl = "https://rmkcdn.successfactors.com/a7d5dbb6/c9ab6ccb-b086-47f2-b25b-2.png"

publish_logo(company, logoUrl)
show_jobs(finalJobs)
