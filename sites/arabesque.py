from scraper.Scraper import Scraper
from getCounty import GetCounty
from utils import (
    translate_city,
    acurate_city_and_county,
    publish_or_update,
    publish_logo,
    show_jobs,
)

_counties = GetCounty()

url = "https://cariere.arabesque.ro"

scraper = Scraper()
scraper.get_from_url(url, verify=False)

categories = scraper.find_all("div", {"class": "arabesque_homepage_template_categorie"})

company = {"company": "Arabesque"}
finalJobs = list()

acurate_city = acurate_city_and_county(
    Iasi={"city": "Iasi", "county": "Iasi"},
)

for category in categories:
    jobs = category.find_all("article")

    categoryUrl = (
        category.find("a", {"class", "arabesque_home_go_to"})
        .get("href")
        .replace("https://cariere.arabesque.ro/jobs/", "")
    )

    jobUrl = (
        "https://cariere.arabesque.ro/jobs/" + "job/" + categoryUrl.replace(" ", "%20")
    )

    if len(jobs) >= 4:
        urlPage = (
            category.find("a", {"class", "arabesque_home_go_to"})
            .get("href")
            .replace(" ", "%20")
        )

        scraper.get_from_url(urlPage, verify=False)

        jobsContainer = scraper.find("div", {"class": "arabesque_homepage_template"})

        jobs = jobsContainer.find_all("article")

    for job in jobs:
        job_title = job.find("h4").text.strip()
        job_link = job.get("id").replace("post-", jobUrl + "&job_id=")
        city = translate_city(job_title.split(" ")[-1].strip().title())

        county = _counties.get_county(city)

        if acurate_city.get(city):
            city = acurate_city.get(city).get("city")
            county = acurate_city.get(city).get("county")

        elif not county:
            first_name = job_title.split(" ")[-2].strip().title()
            city = translate_city(first_name + "-" + city)
            county = _counties.get_county(city)

            if not county:
                city = "Bucuresti"
                county = "Bucuresti"

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

publish_or_update(finalJobs)
logoUrl = (
    "https://cariere.arabesque.ro/wp-content/uploads/2016/09/cropped-logo-blog.png"
)
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
