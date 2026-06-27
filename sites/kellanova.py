from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty, remove_diacritics
from math import ceil

_counties = GetCounty()
url = "https://jobs.kellanova.com/search/?createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_department=&optionsFacetsDD_country="

company = {"company": "Kellanova"}
finalJobs = list()

scraper = Scraper()
scraper.get_from_url(url)

pagination_label = scraper.find("span", {"class": "paginationLabel"})
if pagination_label:
    totalJobs = int(pagination_label.find_all("b")[-1].text.strip())
    paginate = ceil(totalJobs / 50)
else:
    paginate = 1

table = scraper.find("table", {"id": "searchresults"})
if table:
    jobs = table.find("tbody").find_all("tr")
else:
    jobs = []

for row in range(paginate):

    for job in jobs:
        job_title = job.find("a").text.strip()
        job_link = "https://jobs.kellanova.com" + job.find("a").get("href")
        city = translate_city(job.find("span", {"class": "jobLocation"}).text.split(",")[0].strip())

        county = _counties.get_county(city)

        finalJobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "country": "Romania",
            "city": remove_diacritics(city),
            "county": county,
            "company": company.get("company")
        })

    if row == paginate - 1:
        break
    page_url = url + f"&startrow={(row + 1) * 50}"
    scraper.get_from_url(page_url)
    table = scraper.find("table", {"id": "searchresults"})
    if not table:
        break
    jobs = table.find("tbody").find_all("tr")

publish_or_update(finalJobs)

logoUrl = "https://rmkcdn.successfactors.com/e1d74a18/3cf7a194-92ba-497b-8c9b-a.jpg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)