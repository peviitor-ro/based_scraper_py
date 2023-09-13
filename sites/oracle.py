from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)
from math import ceil

url = 'https://eeho.fa.us2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations,flexFieldsFacet.values&finder=findReqs;siteNumber=CX_45001,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=1,locationId=300000000149199,sortBy=POSTING_DATES_DESC'

company = 'Oracle'
jobs = []

scraper = Scraper()
scraper.get_from_url(url, 'JSON')

total_jobs = scraper.markup.get('items')[0].get('TotalJobsCount')

step = 200
pages = ceil(total_jobs / step)

for page in range(pages):
    url = f'https://eeho.fa.us2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations,flexFieldsFacet.values&finder=findReqs;siteNumber=CX_45001,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit={step},locationId=300000000149199,sortBy=POSTING_DATES_DESC,,offset={page * step}'
    scraper.get_from_url(url, 'JSON')
    
    for job in scraper.markup.get('items')[0].get('requisitionList'):
        jobs.append(create_job(
            job_title=job.get('Title'),
            job_link=f'https://careers.oracle.com/jobs/#en/sites/jobsearch/job/{job.get("Id")}',
            company=company,
            country='Romania',
            city=job.get('PrimaryLocation').split(',')[0]
        ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://www.oracle.com/a/ocom/img/oracle-rgb-c74634.png')
show_jobs(jobs)