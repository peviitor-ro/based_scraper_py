from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)
from getCounty import get_county

company = 'Selgros'
url = 'https://mingle.ro/api/boards/mingle/jobs?q=companyUid~eq~%22selgros%22&page=0&pageSize=1000&sort=modifiedDate~DESC'

scraper = Scraper()
scraper.get_from_url(url, "JSON")

acurate_city = {
    "Iasi": {
        "city": "Iasi",
        "county": "Iasi"
    },
}

jobs = []

for job in scraper.markup['data']['results']:
    try:
        locations = job['locations']
        cities = [] 
        counties = []
        for city in locations:
            if "Bucuresti" in city["name"]:
                if "Bucuresti" not in cities:
                    cities.append("Bucuresti")
                    counties.append("Bucuresti")
            else:
                
                county = get_county(city["name"])

                if county and county not in counties:
                    cities.append(city["name"])
                    counties.append(county)
                else:
                    county = get_county(
                        city["name"].replace(" ", "-")
                    )
                    if county and county not in counties:
                        cities.append(city["name"].replace(" ", "-"))
                        counties.append(county)
        jobs.append(create_job(
            job_title=job['jobTitle'],
            job_link='https://selgros.mingle.ro/ro/embed/apply/' + job['publicUid'],
            city=cities,
            country='Romania',
            company=company,
            county=counties,
        ))
    except Exception as e:
        pass

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://www.selgros.ro/themes/contrib/garnet/dist/assets/branding/logo-selgros.svg')
show_jobs(jobs)