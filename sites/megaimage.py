from scraper_peviitor import Scraper, loadingData
import json
from utils import translate_city, acurate_city_and_county, create_job
from getCounty import get_county

url = "https://cariere.mega-image.ro/joburi"

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-GB,en;q=0.9",
    "Host": "cariere.mega-image.ro",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15",
    "Referer": "https://cariere.mega-image.ro/joburi",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest",
}
    
scraper = Scraper(url)

headers["Cookie"] = "vacancy.scrollTop=717; PHPSESSID=" + scraper.session.cookies.get_dict().get("PHPSESSID") + "; device_view=full; hl=ro"
pageNumber = 1

scraper.session.headers.update(headers)

company = {"company": "MegaImage"}
finalJobs = list()

acurate_city = acurate_city_and_county(
    iasi={
        "city": "Iasi",
        "county": "Iasi"
    },
    municipiul_bucuresti={
        "city": "Bucuresti",
        "county": "Bucuresti"
    },
    stefanestii_de_jos={
        "city": "Stefanestii de Jos",
        "county": "Ilfov"
    },
    cluj_napoca={
        "city": "Cluj-Napoca",
        "county": "Cluj"
    },

)

while True:
    url = f"https://cariere.mega-image.ro/api/vacancy/?location[name]=&location[range]=10&location[latitude]=&location[longitude]=&options[sort_order]=desc&sort=date&sortDir=desc&pageNumber={pageNumber}"
    scraper.url = url

    jobs = scraper.getJson().get("vacancies")

    if len(jobs) == 0:
        break

    for job in jobs:
        job_title = job.get("title")
        job_link = "https://cariere.mega-image.ro/post-vacant/" + str(job.get("id")) + "/" + job.get("slug")

        job_element = create_job(
            job_title=job_title,
            job_link=job_link,
            company=company.get("company"),
            country="Romania",
        )
        
        city = translate_city(job.get("city").title())
        
        if acurate_city.get(city.replace(" ", "_").replace("-", "_").lower()):
            job_element["city"] = acurate_city.get(city.replace(" ", "_").replace("-", "_").lower()).get("city")
            job_element["county"] = acurate_city.get(city.replace(" ", "_").replace("-", "_").lower()).get("county")
        else:
            job_element["city"] = city
            job_element["county"] = get_county(city)

        finalJobs.append(job_element)
    
    pageNumber += 1
    

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))
