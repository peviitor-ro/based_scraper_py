from scraper.Scraper import Scraper
from based_scraper_py import create_job, publish, publish_logo, show_jobs
(create_job, publish, publish_logo, show_jobs)
url = "https://external-weatherford.icims.com/jobs/search?ss=1&searchRelation=keyword_all&searchLocation=--PLOIESTI&mobile=false&width=1424&height=500&bga=true&needsRedirect=false&jan1offset=120&jun1offset=180&in_iframe=1"
company = "Weatherford"
jobs = []
scraper = Scraper()
rendered = scraper.get_from_url(url)
jobs_elements = scraper.find("div", class_="iCIMS_JobsTable").find_all("div", class_="row")
for job in jobs_elements:
    jobs.append(create_job(
        company=company,
        job_title=job.find("div", class_="title").find("a").text,
        job_link=job.find("div", class_="title").find("a")["href"],
        country="Romania",
        city="Ploiesti"
    ))
for version in [1, 4]:
    publish(version, company, jobs, "APIKEY")
publish_logo(company, "https://www.weatherford.com/Content/Images/logo-weatherford-text.png")
show_jobs(jobs)
