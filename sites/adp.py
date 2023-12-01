from scraper_peviitor import Scraper, loadingData
import json
import re
from utils import translate_city
from getCounty import get_county, remove_diacritics

url = "https://jobsapi-google.m-cloud.io/api/job/search?callback=jobsCallback&pageSize=100&companyName=companies%2Fc3f83ef5-c5b8-4d56-9c79-66f4052c4c4a&languageCode%5B%5D=en&customAttributeFilter=country%3D%22RO%22&orderBy=relevance%20desc"

company = {"company": "ADP"}
finalJobs = list()

scraper = Scraper()
scraper.session.headers.update({
    "Content-Type": "application/json",
})
response = scraper.session.get(url)
pattern = re.compile(r"jobsCallback\({(.*?)}\)", re.DOTALL)

data = re.search(pattern, response.text).group(1)
jobs = json.loads("{" + data + "}").get("searchResults")

for job in jobs:
    job_title = job.get("job").get("title")
    job_link = job.get("job").get("url")
    locations = job.get("job").get("google_locations")

    cities = [
        translate_city(remove_diacritics(location.get("city")))
        for location in locations
        if location.get("country") == "RO"
    ]
    counties = [
        get_county(city)
        for city in cities
    ]

    finalJobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": cities,
        "county": counties,
    })

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))

logoUrl = "https://cdn-static.findly.com/wp-content/uploads/sites/794/2019/03/NewADP-redlogo.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post("https://api.peviitor.ro/v1/logo/add/", json.dumps([
    {
        "id": company.get("company"),
        "logo": logoUrl
    }
]))
