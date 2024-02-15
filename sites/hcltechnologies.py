from scraper.Scraper import Scraper
from utils import (
    show_jobs,
    translate_city,
    publish,
    publish_logo,
    acurate_city_and_county,
)
from getCounty import get_county

company = "hcltechnologies"
finalJobs = list()

acurate_city = acurate_city_and_county(Iasi={"city": "Iasi", "county": "Iasi"})

url = "https://www.hcltech.com/views/ajax?_wrapper_format=drupal_ajax&view_name=hcl_ers_career_jobs&view_display_id=block_1&view_args=romania_job&page="
pageNumber = 0
headers = {
    "X-Requested-With": "XMLHttpRequest",
}
scraper = Scraper()
scraper.set_headers(headers)
scraper.get_from_url(url + str(pageNumber), "JSON")

html = scraper.markup[3].get("data")

scraper.__init__(html, "html.parser")

jobs = (
    scraper.find("div", {"class": "view-hcl-ers-career-jobs"})
    .find("tbody")
    .find_all("tr")
)

while jobs:
    for job in jobs:
        job_title = job.find("td", {"class": "views-field-title"}).text.strip()
        job_link = "https://www.hcltech.com" + job.find(
            "td", {"class": "views-field-title"}
        ).find("a").get("href")
        location = job.find(
            "td", {"class": "views-field-field-job-location"}
        ).text.strip()

        city = []
        county = []
        remote = []

        job_element = {
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": "Romania",
        }

        if "Remote" in location:
            remote.append("Remote")
        elif "Hybrid" in location:
            remote.append("Hybrid")

        if "(Bucharest/Iasi)" in location:
            city = ["Bucuresti", "Iasi"]
            county = ["Bucuresti", "Iasi"]

        else:
            city = translate_city(location.split(" ")[0])
            if acurate_city.get(city):
                city = acurate_city.get(city).get("city")
                county = acurate_city.get(city).get("county")
            else:
                county = get_county(city)

                if not county:
                    city = []
                    county = []

        job_element.update({"city": city, "county": county, "remote": remote})

        finalJobs.append(job_element)

    pageNumber += 1
    scraper = Scraper()
    scraper.set_headers(headers)
    scraper.get_from_url(url + str(pageNumber), "JSON")
    html = scraper.markup[3].get("data")
    scraper.__init__(html, "html.parser")
    try:
        jobs = (
            scraper.find("div", {"class": "view-hcl-ers-career-jobs"})
            .find("tbody")
            .find_all("tr")
        )
    except AttributeError:
        jobs = False

publish(4, company, finalJobs, "APIKEY")

publish_logo(
    company, "https://www.hcltech.com/themes/custom/hcltech/images/hcltech-new-logo.svg"
)
show_jobs(finalJobs)
