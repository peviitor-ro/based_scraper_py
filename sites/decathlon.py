from getCounty import GetCounty, remove_diacritics
from utils import translate_city, acurate_city_and_county, publish_or_update, publish_logo, show_jobs
import requests
from bs4 import BeautifulSoup


_counties = GetCounty()

company = {"company": "Decathlon"}
base_url = (
    "https://cariere.decathlon.ro/JobList?layoutId=Jobs-1&websiteUrl=https://cariere.decathlon.ro"
    "&themeId=2&language=ro&subdomain=cariere-decathlonromania&page={page}&pageSize=80&contains="
)
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://cariere.decathlon.ro/",
}

acurate_city = acurate_city_and_county(
    Iasi={"city": "Iasi", "county": "Iasi"},
    Piatra_Neamt={"city": "Piatra-Neamt", "county": "Neamt"},
    Ramnicu_Valcea={"city": "Ramnicu Valcea", "county": "Valcea"},
    Stefanestii_de_Jos={"city": "Stefanestii de Jos", "county": "Ilfov"},
    Selimbar={"city": "Selimbar", "county": "Sibiu"},
    Floresti={"city": "Floresti", "county": "Cluj"},
    Varsatura={"city": "Varsatura", "county": "Braila"},
    Blejoi={"city": "Blejoi", "county": "Prahova"},
    Bistrita={"city": "Bistrita", "county": "Bistrita-Nasaud"},
    Targoviste={"city": "Targoviste", "county": "Dambovita"},
    Satu_Mare={"city": "Satu Mare", "county": "Satu Mare"},
    Sector_1={"city": "Bucuresti", "county": "Bucuresti"},
    Sector_2={"city": "Bucuresti", "county": "Bucuresti"},
    Sector_3={"city": "Bucuresti", "county": "Bucuresti"},
    Sector_4={"city": "Bucuresti", "county": "Bucuresti"},
    Sector_6={"city": "Bucuresti", "county": "Bucuresti"},
)

finalJobs = []


def normalize_location(location_text):
    remote = ["Hybrid"] if "Hybrid" in location_text else []
    location_text = (
        location_text.replace(", România", "")
        .replace(", Romania", "")
        .replace("(Hybrid)", "")
        .strip()
    )
    location_text = remove_diacritics(location_text)
    location_text = " ".join(location_text.split())
    city_key = location_text.replace("-", "_").replace(" ", "_")

    if city_key in acurate_city:
        city = acurate_city[city_key]["city"]
        county = [acurate_city[city_key]["county"]]
    else:
        city = translate_city(location_text)
        county = _counties.get_county(city) or []

    return city, county, remote


page = 1

while True:
    response = requests.get(base_url.format(page=page), headers=headers, timeout=20)
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.select("a.jobs__box")

    if not jobs:
        break

    for job in jobs:
        job_title = job.select_one("h3.jobs__box__heading").get_text(" ", strip=True)
        job_link = job.get("href")
        location_text = job.select_one("p.jobs__box__text").get_text(" ", strip=True)
        city, county, remote = normalize_location(location_text)

        finalJobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
                "county": county,
                "remote": remote,
            }
        )

    page += 1


publish_or_update(finalJobs)

logoUrl = "https://adoptoprod.blob.core.windows.net/careers/bcab4933-05c3-45a0-9f93-3ee234531098.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
