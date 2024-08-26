from scraper.Scraper import Scraper
from utils import (
    publish_or_update,
    publish_logo,
    create_job,
    show_jobs,
    translate_city,
    get_jobtype
    )
from getCounty import GetCounty

_counties = GetCounty()
url = "https://careers.smartrecruiters.com/NEXT2"
company = "nextgh"


def get_aditional_city(url):
    scraper = Scraper()
    scraper.get_from_url(url)
    country = (
        scraper.find("spl-job-location")["formattedaddress"].split(",")[-1].strip()
    )
    city = scraper.find("spl-job-location")["formattedaddress"].split(",")[-2].strip()
    remote = scraper.find("spl-job-location").get("workplacetype").capitalize()
    data = {}

    if country == "Romania":
        city = translate_city(city.replace(" 440247", ""))
        if city == "Satu Mare":
            county = "Satu Mare"
        else:
            county = _counties.get_county(translate_city(city))

        data.update(
            {"city": city, "county": county, "remote": remote, "country": country}
        )
    else:
        data.update({"city": city, "county": [], "remote": remote, "country": country})

    return data


scraper = Scraper()
scraper.get_from_url(url)

jobs_elements = scraper.find_all(
    "li", class_="opening-job job column wide-1of2 medium-1of2"
)
final_jobs = []

for job in jobs_elements:
    job_title = job.find(
        "h4", class_="details-title job-title link--block-target"
    ).text.strip()
    job_url = job.find("a")["href"]

    city, county, remote, country = get_aditional_city(job_url).values()

    final_jobs.append(
        create_job(
            job_title=job_title,
            job_link=job_url,
            company=company,
            country=country,
            city=city,
            county=county,
            remote=get_jobtype(remote.replace("_", "-"))
        )
    )

publish_or_update(final_jobs)

publish_logo(
    company,
    "https://c.smartrecruiters.com/sr-careersite-image-prod-aws-dc5/61dc56cb32959e6e268adf29/247fbdf2-3893-443e-ac5b-114e4516d6de?r=s3-eu-central-1",
)

show_jobs(final_jobs)
