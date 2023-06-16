from scraper_peviitor import Scraper, loadingData
import uuid
import json

url = "https://www.amazon.jobs/en/search.json?normalized_country_code%5B%5D=ROU&radius=24km&facets%5B%5D=normalized_country_code&facets%5B%5D=normalized_state_name&facets%5B%5D=normalized_city_name&facets%5B%5D=location&facets%5B%5D=business_category&facets%5B%5D=category&facets%5B%5D=schedule_type_id&facets%5B%5D=employee_class&facets%5B%5D=normalized_location&facets%5B%5D=job_function_id&facets%5B%5D=is_manager&facets%5B%5D=is_intern&offset=&result_limit=100&sort=relevant&latitude=&longitude=&loc_group_id=&loc_query=&base_query=&city=&country=&region=&county=&query_options=&location%5B%5D=bucharest-romania&"

company = {"company": "Amazon"}
finalJobs = list()

scraper = Scraper(url)

jobs = scraper.getJson().get("jobs")

for job in jobs:
    id = uuid.uuid4()
    job_title = job.get("title")
    job_link = "https://www.amazon.jobs" + job.get("job_path")
    country = "Romania"
    city = job.get("normalized_location").split(",")[0]

    print(job_title + " -> " + city)
    
    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "country": country,
        "city": city,
        "company": company.get("company")
    })

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, company.get("company"))

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/603px-Amazon_logo.svg.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))

