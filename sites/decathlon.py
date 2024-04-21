from scraper.Scraper import Scraper
from getCounty import GetCounty, remove_diacritics
from utils import (
    translate_city,
    acurate_city_and_county,
    publish_or_update,
    publish_logo,
    show_jobs,
)

_counties = GetCounty()

scraper = Scraper()
post_data = {
    "query": "",
    "location": [],
    "department": [],
    "worktype": [],
    "remote": [],
    "workplace": [],
}
url = "https://apply.workable.com/api/v3/accounts/decathlon-romania/jobs"
result = scraper.post(url, post_data).json()

jobs = result.get("results")
acurate_city = acurate_city_and_county()

company = {"company": "Decathlon"}
finalJobs = list()

while result.get("nextPage"):
    for job in jobs:
        job_title = job.get("title")
        job_link = "https://apply.workable.com/decathlon-romania/j/" + job.get(
            "shortcode"
        )
        cities = [
            (
                acurate_city.get(
                    remove_diacritics(city.get("city").replace(" ", "_"))
                ).get("city")
                if acurate_city.get(
                    remove_diacritics(city.get("city").replace(" ", "_"))
                )
                else translate_city(remove_diacritics(city.get("city")))
            )
            for city in job.get("locations")
        ]

        counties = []

        for city in cities:
            if acurate_city.get(remove_diacritics(city.replace(" ", "_"))):
                counties.append(
                    acurate_city.get(remove_diacritics(city.replace(" ", "_"))).get(
                        "county"
                    )
                )
            else:
                counties.extend(_counties.get_county(city))

        remote = job.get("workplace").replace("_", "-")

        finalJobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": cities,
                "county": counties,
                "remote": remote,
            }
        )
    post_data["token"] = result.get("nextPage")
    result = scraper.post(url, post_data).json()
    jobs = result.get("results")


publish_or_update(finalJobs)

logoUrl = "https://workablehr.s3.amazonaws.com/uploads/account/logo/404273/logo"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
