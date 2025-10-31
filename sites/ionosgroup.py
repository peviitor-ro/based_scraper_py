from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city, get_jobtype
from getCounty import GetCounty

url = "https://www.1and1.ro/jobs.json"
company = {"company": "ionosgroup"}

data = {
    "tx_cisocareer_jobsearchform[__referrer][@extension]": "CisoCareer",
    "tx_cisocareer_jobsearchform[__referrer][@controller]": "JobOffer",
    "tx_cisocareer_jobsearchform[__referrer][@action]": "find",
    "tx_cisocareer_jobsearchform[__referrer][arguments]": "YTo2OntzOjEwOiJ0ZXh0U2VhcmNoIjtzOjA6IiI7czo4OiJjYXRlZ29yeSI7czowOiIiO3M6MTE6ImNhcmVlckxldmVsIjtzOjA6IiI7czoxNjoibW9kZU9mRW1wbG95bWVudCI7czowOiIiO3M6MTI6ImxvY2F0aW9uTmFtZSI7czo2OiJiZXJsaW4iO3M6MTE6ImNvbXBhbnlOYW1lIjtzOjA6IiI7fQ == 7e81641e41d3a9f030f8a847b0221d4511d0ae3b",
    "tx_cisocareer_jobsearchform[__referrer][@request]": '{"@extension": "CisoCareer", "@controller": "JobOffer", "@action": "find"}70ddfbe9634ffb03829ec95fe9baf5eaf3c478ff',
    "tx_cisocareer_jobsearchform[__trustedProperties]": '{"textSearch": 1, "category": 1, "careerLevel": 1, "modeOfEmployment": 1, "locationName": 1, "companyName": 1}8458397472593a1c8ae53526144be7905bfc001e',
    "tx_cisocareer_jobsearchform[textSearch]": "",
    "tx_cisocareer_jobsearchform[category]": "",
    "tx_cisocareer_jobsearchform[careerLevel]": "",
    "tx_cisocareer_jobsearchform[modeOfEmployment]": "",
    "tx_cisocareer_jobsearchform[locationName]": "bucharest",
    "tx_cisocareer_jobsearchform[companyName]": "",
}

scraper = Scraper()
scraper.set_headers(
    {

        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
)

html = scraper.post(url, data=data)
scraper.__init__(html.text, "html.parser")
jobs_elements = scraper.find_all("a", class_="joboffer-list-job")


finalJobs = [
    {
        "job_title": job.find("h4").text.strip(),
        "job_link": "https://www.ionos-group.com" + job["href"],
        "city": "Bucuresti",
        "county": "Bucuresti",
        "remote": get_jobtype(job.find("h4").text.strip()),
        "company": company.get("company"),
        "country": "Romania",
    }
    for job in jobs_elements
]

publish_or_update(finalJobs)

logoUrl = "https://www.ionos-group.com/_assets/debf05b51933fca5f1c347f2aabc0cf0/Media/ionos-group.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
