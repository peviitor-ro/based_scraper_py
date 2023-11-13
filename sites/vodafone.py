from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)
from math import ceil
from getCounty import get_county
from utils import translate_city

url = "https://jobs.vodafone.com/api/apply/v2/jobs?domain=vodafone.com&start=0&num=10&exclude_pid=563018677368453&query=Romania&pid=563018677368453&domain=vodafone.com&sort_by=relevance"

countrys = {
    "ALB":"Albania",
    "AUS":"Australia",
    "CHN":"China",
    "CZE":"Czech Republic",
    "EGY":"Egypt",
    "DEU":"Germany",
    "Ghana":"Ghana",
    "GRC":"Greece",
    "HUN":"Hungary",
    "IND":"India",
    "IRL":"Ireland",
    "ITA":"Italy",
    "LUX":"Luxembourg",
    "MLT":"Malta",
    "MOZ":"Mozambique",
    "PRT":"Portugal",
    "ROU":"Romania",
    "SGO":"Singapore",
    "ZAF":"South Africa",
    "ESP":"Spain",
    "TZA":"Tanzania, United Republic Of",
    "TUR":"Turkey",
    "GBR":"United Kingdom",
    "USA":"United States"
}

company = 'Vodafone'
jobs = []

scraper = Scraper(url)
scraper.get_from_url(url, "JSON")

total_jobs = scraper.markup["count"]
step = 10
pages = ceil(total_jobs / step)

for page in range(0, pages):
    
    for job in scraper.markup["positions"]:
        locations = job["location"].split(",")
        country = locations[-1].strip()
        city = translate_city(locations[0].strip())

        if country == "ROU":
            county = get_county(city)


            jobs.append(create_job(
                job_title=job["name"],
                job_link=job["canonicalPositionUrl"],
                city=city,
                country="Romania",
                company=company,
                county=county,
            ))
    url = f"https://jobs.vodafone.com/api/apply/v2/jobs?domain=vodafone.com&start={page * step}&num={step}&domain=vodafone.com&sort_by=relevance"
    scraper.get_from_url(url, "JSON")

for version in [1,4]:
    publish(version, company, jobs, 'Grasum_Key')

publish_logo(company, 'https://static.vscdn.net/images/careers/demo/eightfolddemo-vodafone2/8d898eb4-685e-441a-9b64-9.png')

show_jobs(jobs)
