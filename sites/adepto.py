from scraper.Scraper import Scraper
from utils import show_jobs, translate_city
from getCounty import remove remove_diacritics

url = "https://jobs.workable.com/api/v1/companies/3N1Vi5vkmhbtLoUoe4xVH9/"
logo = "https://workablehr.s3.amazonaws.com/uploads/account/logo/586136/logo"


scraper = Scraper()
scraper.get_from_url(url, "JSON")

jobs = scraper.markup.get("jobs")
final_jobs = []


for job in jobs:
    if job["location"]["countryName"] == "Romania":

        county = job["location"]["subregion"].replace("ș", "s")
        county = remove_diacritics(job["location"]["subregion"])
        city = remove_diacriticsjob["location"]["city"])

        final_jobs.append({
                           "company": job["company"]["title"],
                           "job_title": job["title"],
                           "job_link": job["url"],
                           "remote": remote,
                           "country": "Romania",
                           "county": translate_city(county),
                           "city": translate_city(city),
                           })

show_jobs(final_jobs)
