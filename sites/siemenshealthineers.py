from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty
from math import ceil

_counties = GetCounty()
company = "SiemensHealthineers"
url = "https://jobs.siemens-healthineers.com/en_US/searchjobs/SearchJobs/?42449=%5B812022%5D&42449_format=17593&listFilterMode=1&folderRecordsPerPage=6&"

scraper = Scraper()
scraper.get_from_url(url, verify=False)
jobs = []

step = 6
total_jobs = int(scraper.find(
    "div", class_="list-controls__text__legend").text.strip().split(" ")[0]
)

pages = ceil(total_jobs / step)

for page in range(pages):
    jobs_elements = scraper.find_all("article", class_="article")
    for job in jobs_elements:
        try:
            city = translate_city(
                job.find("span", class_="list-item-jobCity").text.strip()
            )
        except Exception as e:
            city = ""
        counties = []

        county = _counties.get_county(city) or []
        counties.extend(county)

        jobs.append(
            create_job(
                job_title=job.find("a", class_="link").text.strip(),
                job_link=job.find("a", class_="link")["href"],
                city=city,
                county=counties,
                country="Romania",
                company=company
            )
        )
        
    url = f"https://jobs.siemens-healthineers.com/en_US/searchjobs/SearchJobs/?42449=%5B812022%5D&42449_format=17593&listFilterMode=1&folderRecordsPerPage=6&folderOffset={step * (page + 1)}"
    scraper.get_from_url(url, verify=False)


publish_or_update(jobs)

publish_logo(
    company,
    "https://static.vscdn.net/images/careers/demo/siemens/1677769995::Healthineers+Logo+2023",
)
show_jobs(jobs)
