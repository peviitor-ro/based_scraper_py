from scraper.Scraper import Scraper
from utils import create_job, publish_logo, publish_or_update, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()

company = "Amazon"
jobs = []

scraper = Scraper()
offset = 0

while True:
    url = f"https://www.amazon.jobs/en/search.json?radius=24km&facets%5B%5D=normalized_country_code&facets%5B%5D=normalized_state_name&facets%5B%5D=normalized_city_name&facets%5B%5D=location&facets%5B%5D=business_category&facets%5B%5D=category&facets%5B%5D=schedule_type_id&facets%5B%5D=employee_class&facets%5B%5D=normalized_location&facets%5B%5D=job_function_id&facets%5B%5D=is_manager&facets%5B%5D=is_intern&offset={offset}&result_limit=100&sort=relevant&latitude=&longitude=&loc_group_id=&loc_query=Romania&base_query=&city=&country=ROU&region=&county=&query_options=&"
    scraper.get_from_url(url, type="JSON")

    jobs_elements = scraper.markup.get("jobs")

    if len(jobs_elements) == 0:
        break

    for job in jobs_elements:
        city = translate_city(job.get("city"))
        job_element = create_job(
            job_title=job.get("title"),
            job_link="https://www.amazon.jobs" + job.get("job_path"),
            country="Romania",
            city=city,
            county=_counties.get_county(city),
            company=company,
        )
        if city == "Virtual":
            job_element["remote"] = "Remote"
            del job_element["city"]
            del job_element["county"]

        jobs.append(job_element)
    offset += 100

publish_or_update(jobs)

publish_logo(
    company,
    "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/603px-Amazon_logo.svg.png",
)
show_jobs(jobs)
