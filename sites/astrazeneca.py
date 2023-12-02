from scraper.Scraper import Scraper
from utils import show_jobs, translate_city, publish, publish_logo
from getCounty import get_county

url = "https://careers.astrazeneca.com/search-jobs/results?ActiveFacetID=798549&CurrentPage=1&RecordsPerPage=100&Distance=100&RadiusUnitType=0&Location=Romania&Latitude=46.00000&Longitude=25.00000&ShowRadius=False&IsPagination=False&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=1&LocationType=2&LocationPath=798549&OrganizationIds=7684&ResultsType=0"

company = {"company": "AstraZeneca"}
finalJobs = list()

scraper = Scraper()
scraper.set_headers({
    "Accept-Language": "en-GB,en;q=0.9",
})

scraper.get_from_url(url, "JSON")
scraper.__init__(scraper.markup.get("results"), "html.parser")


jobs = scraper.find_all("li")

for job in jobs:
    job_title = job.find("h2").text.strip()
    job_link = "https://careers.astrazeneca.com" + job.find("a").get("href")
    city = translate_city(
        job.find("span", {"class": "job-location"}).text.split(",")[0].strip())
    county = get_county(city)

    finalJobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city,
        "county": county
    })

for version in [1, 4]:
    publish(version, company.get("company"), finalJobs, 'APIKEY')

logoUrl = "https://tbcdn.talentbrew.com/company/7684/img/logo/logo-14641-17887.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
