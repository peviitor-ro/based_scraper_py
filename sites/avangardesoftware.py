from scraper.Scraper import Scraper
from getCounty import get_county
from utils import publish, publish_logo, show_jobs, create_job

company = "AvangardeSoftware"
url = "https://avangarde-software.com/careers/"

scraper = Scraper()
response = scraper.get_from_url(url)

jobs = scraper.find_all("a", class_="stm_vacancies__single no_deco mbc_b")

final_jobs = [
    create_job(
        company=company,
        job_link=job["href"],
        job_title=job.find("div", class_="stm_vacancies__title").get_text(strip=True),
        city=job.find("div", class_="stm_vacancies__location")
        .get_text(strip=True)
        .split(",")[0],
        county=get_county(
            job.find("div", class_="stm_vacancies__location")
            .get_text(strip=True)
            .split(",")[0]
        ),
        country="Romania",
    )
    for job in jobs
]


publish(4, company, final_jobs, "Grasum_Key")

publish_logo(
    company,
    "https://avangarde-software.com/wp-content/uploads/2020/03/Avangarde-Software-Logo-1.png",
)
show_jobs(final_jobs)
