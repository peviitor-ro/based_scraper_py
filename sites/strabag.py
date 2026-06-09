from scraper.Scraper import Scraper
from utils import (
    publish_or_update,
    publish_logo,
    create_job,
    show_jobs,
    translate_city,
)
from getCounty import GetCounty
import re

url = "https://jobboerse.strabag.at/inc/jobsuche_2025_v1.php"

company = "Strabag"
jobs = []
_counties = GetCounty()

data = {
    "MIME Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "morejobs": 1,
    "search": "Romania",
    "radius": 50,
    "language": "RO",
    "status": 1,
}

while True:

    scraper = Scraper()
    response = scraper.post(url, data=data).text
    scraper.__init__(response, "html.parser")

    jobs_containers = scraper.find_all("div", class_="search-entry__container")

    no_jobs = scraper.find("div", class_="no-result__actions")
    if no_jobs:
        break

    for job_container in jobs_containers:
        try:
            job_title = (
                job_container.find("h4", class_="search-entry__headline")
                .text.strip()
            )
            job_link = job_container.find("a")["href"]

            location_text = ""
            for span in job_container.find_all(
                "span", class_="search-entry__tag"
            ):
                if span.find("i", class_="fa-location-dot"):
                    location_text = span.get_text(strip=True)
                    break

            cities = []
            counties_list = []

            if location_text:
                if location_text.startswith("Romania: "):
                    location_text = location_text[9:]

                if location_text and location_text.lower() != "romania":
                    parts = re.split(
                        r",\s*(?![^()]*\))", location_text
                    )

                    for part in parts:
                        part = part.strip()
                        if not part:
                            continue

                        paren_match = re.match(
                            r"^(.+?)\s*\(([^)]+)\)\s*$", part
                        )
                        if paren_match:
                            city = translate_city(
                                paren_match.group(1).strip()
                            )
                            county_raw = paren_match.group(2).strip()
                            county_raw = (
                                county_raw.replace("jud.", "")
                                .replace("Jud.", "")
                                .replace("jud ", "")
                                .replace("Jud ", "")
                                .strip()
                            )
                            if city and city.lower() != "romania":
                                cities.append(city)
                                if "," in county_raw:
                                    last = [
                                        x.strip()
                                        for x in county_raw.split(",")
                                    ][-1]
                                    county = _counties.get_county(
                                        translate_city(last)
                                    )
                                elif (
                                    county_raw.lower()
                                    == city.lower().replace("-", " ")
                                ):
                                    county = _counties.get_county(city)
                                else:
                                    county = county_raw
                                if isinstance(county, list):
                                    counties_list.append(
                                        county[0] if county else ""
                                    )
                                elif county:
                                    counties_list.append(county)
                                else:
                                    counties_list.append("")
                            continue

                        if "jud" in part.lower():
                            jud_match = re.match(
                                r"^(.+?)[,.]?\s*(?:Jud\.?|jud\.?)\s+(.+)$",
                                part,
                            )
                            if jud_match:
                                city = translate_city(
                                    jud_match.group(1).strip()
                                )
                                county_name = jud_match.group(
                                    2
                                ).strip()
                                if (
                                    city
                                    and city.lower() != "romania"
                                ):
                                    cities.append(city)
                                    county = _counties.get_county(
                                        translate_city(county_name)
                                    )
                                    if isinstance(county, list):
                                        counties_list.append(
                                            county[0] if county else ""
                                        )
                                    elif county:
                                        counties_list.append(county)
                                    else:
                                        counties_list.append(
                                            county_name
                                        )
                                continue

                        city = translate_city(part)
                        if city and city.lower() != "romania":
                            cities.append(city)
                            county = _counties.get_county(city)
                            if isinstance(county, list):
                                counties_list.append(
                                    county[0] if county else ""
                                )
                            elif county:
                                counties_list.append(county)
                            else:
                                counties_list.append("")

            job_data = create_job(
                job_title=job_title,
                job_link=job_link,
                country="Romania",
                company=company,
            )

            if cities:
                job_data["city"] = cities
                job_data["county"] = counties_list

            jobs.append(job_data)
        except Exception:
            continue

    data["morejobs"] += 1


try:
    publish_or_update(jobs)
except Exception as e:
    print(e)

publish_logo(company, "https://jobboerse.strabag.at/img/strabag-logo-300px.png")
show_jobs(jobs)
