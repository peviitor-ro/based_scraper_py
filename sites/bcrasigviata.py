import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()

API_URL = "https://gateway.bcradvinternal.com/api/admin/content/generic/cariere"
BASE_URL = "https://www.bcrasigviata.ro/cariere"
LOGO_URL = "https://www.bcrasigviata.ro/assets/shared/icons/logo_BCR_AdV_footer.svg"
COMPANY = "BCR Asigurări de Viață"

scraper = Scraper()
scraper.set_headers({
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.bcrasigviata.ro/",
})

scraper.get_from_url(API_URL, "JSON")
data = scraper.markup

finalJobs = []

for section in data.get("sections", []):
    if section.get("templateRoute") != "cariere":
        continue
    if "tabs" not in section:
        continue
    for tab in section["tabs"]:
        if tab.get("label") != "Posturi disponibile":
            continue
        for idx, job in enumerate(tab.get("characteristics", [])):
            job_title = job.get("label", "")
            value = job.get("value", "")

            loc_match = re.search(
                r"(?:Locație|Locaţie|Locatie)(?:</strong>)?[:\s]*([^<.]+)",
                value,
                re.IGNORECASE,
            )
            location = loc_match.group(1).strip() if loc_match else ""

            emoji_match = re.search(r"📍\s*([^<\n]+)", value)
            if not location and emoji_match:
                location = emoji_match.group(1).strip()

            city_part = location.split("-")[0].split("/")[0].strip()
            city = translate_city(city_part)
            counties = _counties.get_county(city) or []

            finalJobs.append({
                "job_title": job_title,
                "job_link": f"{BASE_URL}#{idx}",
                "company": COMPANY,
                "country": "Romania",
                "city": [city] if city else [],
                "county": counties,
            })
        break
    break

publish_or_update(finalJobs)
publish_logo(COMPANY, LOGO_URL)
show_jobs(finalJobs)
