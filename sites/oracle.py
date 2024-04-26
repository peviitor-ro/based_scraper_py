from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty
from math import ceil

_counties = GetCounty()
url = "https://eeho.fa.us2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations,flexFieldsFacet.values&finder=findReqs;siteNumber=CX_45001,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=200,locationId=300000000149199,sortBy=POSTING_DATES_DESC"

company = "Oracle"
jobs = []

scraper = Scraper()
scraper.get_from_url(url, "JSON")

total_jobs = scraper.markup.get("items")[0]

step = 200
pages = ceil(total_jobs.get("TotalJobsCount") / step)

for page in range(pages):
    for job in total_jobs.get("requisitionList"):
        city = translate_city(job.get("PrimaryLocation").split(",")[0])
        county = _counties.get_county(city)

        if not county:
            city = "All"
            county = "All"

        jobs.append(
            create_job(
                job_title=job.get("Title"),
                job_link=f'https://careers.oracle.com/jobs/#en/sites/jobsearch/job/{job.get("Id")}',
                company=company,
                country="Romania",
                city=city,
                county=county,
            )
        )

    url = f"https://eeho.fa.us2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations,flexFieldsFacet.values&finder=findReqs;siteNumber=CX_45001,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit={step},locationId=300000000149199,sortBy=POSTING_DATES_DESC,,offset={page * step}"
    scraper.get_from_url(url, "JSON")
    total_jobs = scraper.markup.get("items")[0]

publish_or_update(jobs)

publish_logo(
    company,
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Oracle_logo.svg/512px-Oracle_logo.svg.png",
)
show_jobs(jobs)
