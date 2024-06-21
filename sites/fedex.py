from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty
import requests

_counties = GetCounty()

response = requests.get(
    "https://careers.fedex.com/jobs?location_name=Romania&location_type=4&filter%5Bcountry%5D%5B0%5D=Romania"
)

cookies = response.cookies.get_dict()
header_cookies = response.headers.get("Set-Cookie")


url = "https://careers.fedex.com/api/get-jobs?location_name=Romania&location_type=4&filter%5Bcountry%5D%5B0%5D=Romania&_pathname_=%2Fjobs&job_source=paradox&search_mode=2&enable_kilometers=false&include_remote_jobs=true"

payload = {
    "jobs_filter_options": [
        {
            "field": "category",
            "alias": "Categories",
            "facet_field_keyvalue": [
                {
                    "original_value": "Package Handler",
                    "custom_value": "Package Handler",
                    "doc_count": 1,
                },
                {
                    "original_value": "Professional",
                    "custom_value": "Professional",
                    "doc_count": 14,
                },
            ],
        },
        {
            "field": "brand",
            "alias": "Companies",
            "facet_field_keyvalue": [
                {
                    "original_value": "Federal Express Corporation",
                    "custom_value": "Federal Express Corporation",
                    "doc_count": 4,
                },
                {
                    "original_value": "Federal Express Corporation EU",
                    "custom_value": "Federal Express Corporation EU",
                    "doc_count": 7,
                },
                {
                    "original_value": "FedEx Dataworks",
                    "custom_value": "FedEx Dataworks",
                    "doc_count": 3,
                },
                {
                    "original_value": "FedEx Office",
                    "custom_value": "FedEx Office",
                    "doc_count": 1,
                },
            ],
        },
        {
            "field": "is_remote",
            "alias": "Remote",
            "facet_field_keyvalue": [
                {"original_value": "false", "custom_value": "No", "doc_count": 7},
                {"original_value": "true", "custom_value": "Yes", "doc_count": 8},
            ],
        },
        {
            "field": "employment_type",
            "alias": "Employment",
            "facet_field_keyvalue": [
                {
                    "original_value": "FULL_TIME",
                    "custom_value": "Full Time",
                    "doc_count": 15,
                }
            ],
        },
        {
            "field": "country",
            "alias": "Country",
            "facet_field_keyvalue": [
                {
                    "original_value": "Romania",
                    "custom_value": "Romania",
                    "doc_count": 7,
                },
                {
                    "original_value": "United States",
                    "custom_value": "United States",
                    "doc_count": 8,
                },
            ],
        },
        {
            "field": "state",
            "alias": "State",
            "facet_field_keyvalue": [
                {
                    "original_value": "Arizona",
                    "custom_value": "Arizona",
                    "doc_count": 2,
                },
                {
                    "original_value": "Arkansas",
                    "custom_value": "Arkansas",
                    "doc_count": 2,
                },
                {
                    "original_value": "București",
                    "custom_value": "București",
                    "doc_count": 2,
                },
                {
                    "original_value": "Florida",
                    "custom_value": "Florida",
                    "doc_count": 2,
                },
                {
                    "original_value": "Județul Cluj",
                    "custom_value": "Județul Cluj",
                    "doc_count": 2,
                },
                {
                    "original_value": "Județul Ilfov",
                    "custom_value": "Județul Ilfov",
                    "doc_count": 1,
                },
                {
                    "original_value": "Județul Timiș",
                    "custom_value": "Județul Timiș",
                    "doc_count": 2,
                },
                {
                    "original_value": "Pennsylvania",
                    "custom_value": "Pennsylvania",
                    "doc_count": 4,
                },
                {
                    "original_value": "Tennessee",
                    "custom_value": "Tennessee",
                    "doc_count": 7,
                },
                {"original_value": "Texas", "custom_value": "Texas", "doc_count": 5},
            ],
        },
        {
            "field": "city",
            "alias": "City",
            "facet_field_keyvalue": [
                {
                    "original_value": "Bucharest",
                    "custom_value": "Bucharest",
                    "doc_count": 2,
                },
                {
                    "original_value": "Ghiroda",
                    "custom_value": "Ghiroda",
                    "doc_count": 2,
                },
                {
                    "original_value": "Harrison",
                    "custom_value": "Harrison",
                    "doc_count": 2,
                },
                {
                    "original_value": "Judetul Cluj",
                    "custom_value": "Judetul Cluj",
                    "doc_count": 2,
                },
                {
                    "original_value": "Memphis",
                    "custom_value": "Memphis",
                    "doc_count": 7,
                },
                {
                    "original_value": "Orlando",
                    "custom_value": "Orlando",
                    "doc_count": 2,
                },
                {
                    "original_value": "Otopeni",
                    "custom_value": "Otopeni",
                    "doc_count": 1,
                },
                {
                    "original_value": "Phoenix",
                    "custom_value": "Phoenix",
                    "doc_count": 2,
                },
                {
                    "original_value": "Pittsburgh",
                    "custom_value": "Pittsburgh",
                    "doc_count": 4,
                },
                {"original_value": "Plano", "custom_value": "Plano", "doc_count": 5},
            ],
        },
    ],
    "jobs_target_list": {
        "language": ["en"],
        "feed_id": {
            "Paradox Feed": ["paradox-fedexapi.paradox.ai-2634"],
            "FedEx Supply Chain": ["158901-53669"],
            "Federal Express Corporation - PROD external": ["25_2634_external"],
        },
        "cf_posting_type": ["External", "Internal/External"],
    },
    "oeid": 25,
    "page_attributes": {
        "custom_fields": {
            "employment_contractor": None,
            "employment_entrylevel": None,
            "employment_fellowship": None,
            "employment_fulltime": "Full Time",
            "employment_intern": None,
            "job_remote_false": "No",
            "job_remote_true": "Yes",
            "employment_parttime": None,
            "employment_perdiem": None,
            "employment_resident": None,
            "employment_seasonal": None,
            "employment_temporary": None,
            "employment_volunteer": None,
        },
        "jobs_target_language": "",
        "jobs_radius_enable_kilometers": False,
    },
}

headers = {
    "Content-Type": "application/json",
}

response = requests.post(url, json=payload, headers=headers, cookies=cookies).json()

jobs = response.get("jobs")

company = {"company": "FedEx"}
finaljobs = list()

for job in jobs:
    job_title = job.get("title")
    job_link = f"https://careers.fedex.com/{job.get('originalURL')}"
    locations = job.get("locations")
    cities = [
        translate_city(location.get("city"))
        for location in locations
        if location.get("city")
    ]

    counties = []

    for city in cities:

        if city == "Judetul Cluj":
            city = "Cluj-Napoca"

        county = _counties.get_county(city)
        counties.extend(county)

    finaljobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": counties,
        }
    )

publish_or_update(finaljobs)

logoUrl = "https://1000logos.net/wp-content/uploads/2021/04/Fedex-logo-500x281.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)
