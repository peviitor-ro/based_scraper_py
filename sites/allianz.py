from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty
import json

_counties = GetCounty()

url = "https://careers.allianz.com/widgets"

payload = payload = json.dumps({
    "sortBy": "",
    "subsearch": "",
    "from": 0,
    "jobs": True,
    "counts": True,
    "all_fields": [
        "phLocSlider",
        "category",
        "country",
        "state",
        "city",
        "remote",
        "employmentType",
        "jobLevel",
        "type",
        "unit"
    ],
    "pageName": "search-results",
    "size": 99,
    "clearAll": False,
    "jdsource": "facets",
    "isSliderEnable": True,
    "pageId": "page1",
    "siteType": "external",
    "keywords": "",
    "global": True,
    "selected_fields": {
        "state": [
            "Bucuresti"
        ]
    },
    "locationData": {
        "place_id": "ChIJw3aJlSb_sUARlLEEqJJP74Q",
        "sliderRadius": 50,
        "aboveMaxRadius": False,
        "LocationUnit": "miles",
        "placeVal": "Romania"
    },
    "s": "1",
    "lang": "en_global",
    "deviceType": "desktop",
    "country": "global",
    "refNum": "AISAIPGB",
    "ddoKey": "eagerLoadRefineSearch"
})

headers = {
    "Content-Type": "application/json",
}

company = {"company": "Allianz"}
finaljobs = []

scraper = Scraper()
scraper.set_headers(headers)
res = scraper.post(url, payload)

jobs = res.json().get("eagerLoadRefineSearch").get("data").get("jobs")


finaljobs.extend(
    [
        {
            "job_title": element.get("title"),
            "job_link": "https://careers.allianz.com/global/en/job/" + element.get("jobId"),
            "company": company.get("company"),
            "country": element.get("country"),
            "city": translate_city(element.get("city")),
            "county": _counties.get_county(translate_city(element.get("city"))),
            "remote": ["Hybrid"],
        }
        for element in jobs
    ])

publish_or_update(finaljobs)

logoUrl = "https://rmkcdn.successfactors.com/cdd11cc7/5d49b267-5aa1-4363-8155-d.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)

