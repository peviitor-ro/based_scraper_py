from scraper.Scraper import Scraper
from utils import (
    translate_city,
    publish_or_update,
    publish_logo,
    show_jobs,
    acurate_city_and_county,
)
from getCounty import GetCounty, remove_diacritics

_counties = GetCounty()
acurate_city = acurate_city_and_county(
    Iasi={"city": "Iasi", "county": ["Iasi"]}, Ilfov={"city": "All", "county": ["Ilfov"]}
)


def get_aditional_city(url):
    scraper = Scraper()
    scraper.get_from_url(url)

    locations = scraper.find("meta", {"data-hid": "cXenseParse:b19-ejobs_city"})[
        "content"
    ].split(",")

    cities = []
    counties = []

    for location in locations:
        city = (
            translate_city(remove_diacritics(location.strip()))
            if acurate_city.get(remove_diacritics(location.strip()))
            or _counties.get_county(location.strip())
            else None
        )

        if city:
            if acurate_city.get(city):
                county = acurate_city.get(city)["county"]
                city = acurate_city.get(city)["city"]
            else:
                county = _counties.get_county(city)

            cities.append(city)
            counties.extend(county)

    return cities, counties


url = "https://www.ejobs.ro/company/veo/161798"
page = 1

company = "VEO"
final_jobs = []

scraper = Scraper()
scraper.get_from_url(url)

jobs = scraper.find("main", class_="CDInner__Main").find_all("div", class_="JobCard")

while jobs:
    for job in jobs:
        job_title = job.find("h2", class_="JCContentMiddle__Title").text.strip()
        job_url = job.find("h2", class_="JCContentMiddle__Title").find("a")["href"]
        job_url = "https://www.ejobs.ro" + job_url
        locations = (
            job.find("div", class_="JCContentMiddle__Info").text.strip().split(",")
        )

        if "și alte" in locations[-1]:
            cities, counties = get_aditional_city(job_url)
        else:
            cities = []
            counties = []

            for location in locations:
                city = (
                    translate_city(remove_diacritics(location.strip()))
                    if acurate_city.get(remove_diacritics(location.strip()))
                    or _counties.get_county(location.strip())
                    else None
                )

                if city:
                    if acurate_city.get(city):
                        county = acurate_city.get(city)["county"]
                        city = acurate_city.get(city)["city"]
                    else:
                        county = _counties.get_county(city)

                    cities.append(city)
                    counties.extend(county)

        final_jobs.append(
            {
                "job_title": job_title,
                "job_link": job_url,
                "city": cities,
                "county": counties,
                "company": company,
                "country": "Romania",
            }
        )

    page += 1
    scraper.get_from_url(url + "/" + str(page))
    jobs = scraper.find("main", class_="CDInner__Main").find_all(
        "div", class_="JobCard"
    )

publish_or_update(final_jobs)

publish_logo(company, "https://content.ejobs.ro/img/logos/1/161798.png")
show_jobs(final_jobs)
