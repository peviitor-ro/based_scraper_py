from scraper.Scraper import Scraper
from utils import (create_job, publish, publish_logo, show_jobs)
from getCounty import get_county


url = "https://external-weatherford.icims.com/jobs/search?ss=1&searchRelation=keyword_all&searchLocation=13526--&mobile=false&width=1424&height=500&bga=true&needsRedirect=false&jan1offset=120&jun1offset=180&in_iframe=1"

company = "Weatherford"
jobs = []

scraper = Scraper()
rendered = scraper.get_from_url(url)

jobs_elements = scraper.find("div", class_="iCIMS_JobsTable").find_all("div", class_="row")

for job in jobs_elements:
    if job.find("div", {'class':'title'}):
        job_title = job.find("div", class_="title").find("a", {'class': 'iCIMS_Anchor'}).text.strip()
        job_link = job.find("div", class_="title").find("a")["href"]
        country = "Romania"
        city = job.find('div', {'class': 'header'}).find_all('span')[-1].text.strip().split("|")
        cities=[]
        counties=[]
        for county in city:
            city = county.replace('RO-','').strip().capitalize()
            if city == "Cimpina":
                city = "Campina"
            judet=get_county(city)
            if judet and judet not in counties:
                counties.append(judet)
            if judet and city not in cities:
                cities.append(city)
        if cities and counties:
            jobs.append(create_job
                (job_title= job_title,
                job_link= job_link,
                city=cities,
                county=counties,
                country=country,
                company=company )
            )

for version in [1, 4]:
   publish(version, company, jobs, "APIKEY")

publish_logo(company, "https://www.weatherford.com/Content/Images/logo-weatherford-text.png")
show_jobs(jobs)
    