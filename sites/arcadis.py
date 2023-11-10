from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs, translate_city, acurate_city_and_county)
from getCounty import get_county
import json

url = 'https://careers.arcadis.com/widgets'
company = 'Arcadis'

scraper = Scraper()
headers = {
    'Content-Type': 'application/json',
}
scraper.set_headers(headers)

data = {
    "lang":"en_global",
    "deviceType":"desktop",
    "country":"global",
    "pageName":"search-results",
    "ddoKey":"refineSearch",
    "sortBy":"",
    "subsearch":"",
    "from":0,"jobs":True,
    "counts":True,
    "all_fields":["category","country","city","state","workplaceTypeCode"],
    "size":1000,
    "clearAll":False,
    "jdsource":"facets",
    "isSliderEnable":False,
    "pageId":"page1-migration",
    "siteType":"external",
    "location":"","keywords":"",
    "global":True,
    "selected_fields":{"country":["Romania"]},
    "locationData":{}}

response = scraper.post(url, json.dumps(data))

jobs = list()

for job in response.json().get('refineSearch').get('data').get('jobs'):
    job_title=job.get("title")
    job_link=job.get("applyUrl")
    country="Romania"
    city=job.get("city")
    aditional_location = job.get("multi_location")

    cities = []
    counties = []

    exclude_city = acurate_city_and_county(Iasi={"city": "Iasi", "county": "Iasi"}, Moldavia={"city":"Iasi", "county": "Iasi"})

    if exclude_city.get(city):
        cities.append(exclude_city.get(city).get("city"))
        counties.append(exclude_city.get(city).get("county"))

    elif get_county(translate_city(city)):
        cities.append(translate_city(city))
        counties.append(
            get_county(translate_city(city))
        )

    for location in aditional_location:
        aditional_location_city = location.split(",")[0]
        
        if exclude_city.get(aditional_location_city) and not exclude_city.get(aditional_location_city).get("city") in cities:
            cities.append(exclude_city.get(aditional_location_city).get("city"))
            counties.append(exclude_city.get(aditional_location_city).get("county"))
        elif get_county(translate_city(aditional_location_city)) and not translate_city(aditional_location_city) in cities:
            cities.append(translate_city(aditional_location_city))
            counties.append(
                get_county(translate_city(aditional_location_city))
            )

    jobs.append(create_job(
        job_title=job_title,
        job_link=job_link,
        company=company,
        country=country,
        city=cities,
        county=counties,
    ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')
publish_logo(company, "https://cdn.phenompeople.com/CareerConnectResources/ARCAGLOBAL/images/header-1679586076111.svg")
show_jobs(jobs)
