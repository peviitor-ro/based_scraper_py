from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)
from getCounty import get_county, remove_diacritics
# id_lang=1&filter-only-open=1&listing-section=job-list&kw=&id_job_department=0&id_owner_branch=0

url="https://www.jobs-continentalhotels.ro/_ajax/get-job-list.php"
company = "ContinentalHotels"
scraper = Scraper()

body = {"id_lang":1, "filter-only-open":1,"listing-section" :"job-list", "id_job_department":0, "id_owner_branch":0}
scraper.post(url, body)
response=scraper.post(url, body)
scraper.__init__(response.text, "html.parser")

jobsElements=scraper.find_all("a")

jobs=[]
def get_city(string):
    stars=[" 1*"," 2*"," 3*"," 4*"," 5*"," 6*"]
    cityChange={"Mureș":"Targu Mures", "Severin":"Drobeta-Turnu Severin"}
    for star in stars:
        string=string.replace(star, "")
    cities=string.split(' ')[-1]
    if cityChange.get(cities):
        cities=cityChange.get(cities)
    return cities

for job in jobsElements:

    job_title=job.find("h3", {"class":"job-listing-title"}).text.strip()
    job_link = job["href"]
    country = "Romania"
    city=job.find("div", {"class":"job-listing-footer"}).text.strip().split(",")
    citymap=list(map(get_city, city))
    counties=[]
    for oras in citymap:
        counties.append(get_county(oras))

    jobs.append(
         {
            "job_title": job_title,
            "job_link": job_link,
            "country": country,
            "city": citymap,
            "county": counties,
            "company": company
        })

for version in [1, 4]:
    publish(version, company, jobs, 'DAVIDMONDOC')

publish_logo(company, 'https://www.pngkey.com/png/full/396-3967606_continental-hotels-continental-forum-sibiu-sigla.png')
show_jobs(jobs)
