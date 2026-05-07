from scraper.Scraper import Scraper
from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty

_counties = GetCounty()

url = "https://iawmqy.fa.ocs.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations,flexFieldsFacet.values&finder=findReqs;siteNumber=CX_1001,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=200,sortBy=POSTING_DATES_DESC,location=Romania"

company = {"company": "Dell"}
finaljobs = list()

scraper = Scraper()
scraper.set_headers({"Accept": "application/json"})
scraper.get_from_url(url, "JSON")

jobs = scraper.markup.get("items")[0].get("requisitionList")

for job in jobs:
    job_title = job.get("Title")
    job_link = f'https://iawmqy.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/careers/job/{job.get("Id")}'

    city = translate_city(
        job.get("PrimaryLocation").split(",")[0].strip()
    )

    job_element = {
        "job_title": job_title,
        "job_link": job_link,
        "country": "Romania",
        "company": company.get("company"),
    }

    if "Remote" in city:
        job_element["remote"] = "Remote"
    else:
        job_element["city"] = city
        job_element["county"] = _counties.get_county(city)

    finaljobs.append(job_element)

publish_or_update(finaljobs)

logoUrl = "https://tbcdn.talentbrew.com/company/375/v4_0/img/logos/delltech_logo_prm_blue_rgb.jpg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)
