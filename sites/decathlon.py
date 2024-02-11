from scraper_peviitor import Scraper
from getCounty import get_county, remove_diacritics
from utils import translate_city, acurate_city_and_county, publish, publish_logo, show_jobs

scraper = Scraper("https://apply.workable.com//api/v1/widget/accounts/404273")
jobs = scraper.getJson().get("jobs")
show_jobs(jobs)

company = {"company": "Decathlon"}
finalJobs = list()

acurate_city = acurate_city_and_county(
    Iasi={"city": "Iasi", "county": "Iasi"},
    Satu_Mare={"city": "Satu Mare", "county": "Satu Mare"},
)
for job in jobs:
    job_title = job.get("title")
    job_link = job.get("url")
    city = translate_city(remove_diacritics(job.get("city")))

    if acurate_city.get(city.replace(" ", "_")):
        city = acurate_city.get(city.replace(" ", "_")).get("city")
        county = acurate_city.get(city.replace(" ", "_")).get("county")
    else:
        county = get_county(city)

    if not county:
        city = city.replace(" ", "-")
        county = get_county(city)

    finalJobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county,
        }
    )

publish(4, company.get("company"), finalJobs, "APIKEY")

logoUrl = "https://workablehr.s3.amazonaws.com/uploads/account/logo/404273/logo"
publish_logo(company.get("company"), logoUrl)

# show_jobs(finalJobs)
