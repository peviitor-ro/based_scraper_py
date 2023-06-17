from scraper_peviitor import Scraper, loadingData
import uuid
import json

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

while True:
    url = f"https://cariere.mega-image.ro/api/vacancy/?location[name]=&location[range]=10&location[latitude]=&location[longitude]=&options[sort_order]=desc&sort=date&sortDir=desc&pageNumber={pageNumber}"
    scraper.url = url

    jobs = scraper.getJson().get("vacancies")

    if len(jobs) == 0:
        break

    for job in jobs:
        id = uuid.uuid4()
        job_title = job.get("title")
        job_link = "https://cariere.mega-image.ro/post-vacant/" + str(job.get("id")) + "/" + job.get("slug")
        city = job.get("city")

        finalJobs.append({
                "id": str(id),
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
            })
    
    pageNumber += 1

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))