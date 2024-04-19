from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, acurate_city_and_county
from getCounty import GetCounty

_coubties = GetCounty()

url = "https://www.ejobs.ro/company/cartofisserie/286239"
company = "CARTOFISSERIE"

scraper = Scraper()
scraper.get_from_url(url)

job_elements = scraper.find("main", class_="CDInner__Main").find_all(
    "div", class_="JobCard"
)
acurate_city = acurate_city_and_county()

final_jobs = []

for job in job_elements:
    job_title = job.find("h2", class_="JCContentMiddle__Title").text.strip()
    job_url = job.find("h2", class_="JCContentMiddle__Title").find("a")["href"]
    job_url = "https://www.ejobs.ro" + job_url

    location_info = job.find("span", class_="JCContentMiddle__Info")
    city_parts = location_info.get_text(separator=",").split(",")

    cities = []
    for part in city_parts:
        part = part.strip().replace("\u0218", "S").replace("\u0219", "s")
        if acurate_city.get(part.replace(" ", "_").replace("-", "_")):
            cities.append(
                acurate_city.get(part.replace(" ", "_").replace("-", "_")).get("city")
            )
        elif (
            part
            and not any(word in part for word in ["orase", "si alte"])
            and not part.isdigit()
        ):
            cities.append(part)

    additional_cities_span = location_info.find("span", class_="PartialList__Rest")
    if additional_cities_span and additional_cities_span.has_attr("title"):
        additional_cities = additional_cities_span["title"].split(",")
        for city in additional_cities:
            city = city.strip().replace("\u0218", "S").replace("\u0219", "s")
            if acurate_city.get(city.replace(" ", "_").replace("-", "_")):
                cities.append(
                    acurate_city.get(city.replace(" ", "_").replace("-", "_")).get(
                        "city"
                    )
                )

            elif (
                city
                and not any(word in city for word in ["orase", "si alte"])
                and not city.isdigit()
            ):
                cities.append(city)

    counties = []

    for city in cities:
        if acurate_city.get(city.replace(" ", "_").replace("-", "_")):
            counties.append(
                acurate_city.get(city.replace(" ", "_").replace("-", "_")).get("county")
            )
        else:
            counties.extend(_coubties.get_county(city))

    country = "Romania"
    final_jobs.append(
        {
            "job_title": job_title,
            "job_link": job_url,
            "city": cities,
            "county": counties,
            "country": country,
            "company": company,
        }
    )

publish_or_update(final_jobs)
publish_logo(company, "https://content.ejobs.ro/img/logos/2/286239.png")

show_jobs(final_jobs)
