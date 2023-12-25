from scraper_peviitor import Scraper, loadingData
import json
import re
from utils import translate_city
from getCounty import get_county

url = "https://careers.adobe.com/us/en/search-results" #&from=10

company = {"company": "Adobe"}
finalJobs = list()

scraper = Scraper()
response = scraper.session.get(url)

pattern = re.compile(r"phApp.ddo = {(.*?)};", re.DOTALL)

data = re.search(pattern, response.text).group(1)
totalJobs = json.loads("{" + data + "}").get("eagerLoadRefineSearch").get("totalHits")

querys = [*range(0, totalJobs, 10)]

for query in querys:
    url = "https://careers.adobe.com/us/en/search-results?keywords=Romania&from=" + str(query) + "&s=1"
    response = scraper.session.get(url)
    data = re.search(pattern, response.text).group(1)
    jobs = json.loads("{" + data + "}").get("eagerLoadRefineSearch").get("data").get("jobs")

    for job in jobs:
        job_title = job.get("title")
        job_link = "https://careers.adobe.com/us/en/job/" + job.get("jobId")
        city = job.get("city")
        country = job.get("country")
        remote = []

        if not city:
            city = job.get("cityStateCountry").split(",")[0]

        if city == "Remote":
            city = ""
            remote.append("Remote")
        
        job_element = {
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": country,
            "city": city,
            "remote": remote,
        }

        if country == "Romania":
            if city:
                city = translate_city(city)
                county = get_county(city)

                job_element.update({
                    "city": city,
                    "county": county
                })

        finalJobs.append(job_element)

print(json.dumps(finalJobs, indent=4)) 

loadingData(finalJobs, company.get("company"))

logoUrl = "https://cdn.phenompeople.com/CareerConnectResources/ADOBUS/images/Header-1649064948136.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))