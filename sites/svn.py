from scraper.Scraper import Scraper
from utils import (
    publish,
    publish_logo,
    create_job,
    show_jobs,
    translate_city
)
from getCounty import get_county, remove_diacritics


def remove_umlaut(string):
    """
    Removes umlauts from strings and replaces them with the letter+e convention
    :param string: string to remove umlauts from
    :return: unumlauted string
    """

    t = "\u0083"
    a = "\u00c4\u0083"
    aa = "\u00c3\u00a2"

    string = string.replace(t, "t")
    string = string.replace(a, "a")
    string = string.replace(aa, "a")

    return string


company = "SVN"
url = "https://jobs.svn.ro/posturi-vacante.html"

scraper = Scraper()
scraper.get_from_url(url)

jobs = []

jobs_elements = scraper.find("div", class_="jobs").find_all("div", class_="job")

for job in jobs_elements:
    job_title = remove_diacritics(
        job.find("h3").text.encode("raw_unicode_escape").decode("utf-8")
    )
    job_link = "https://jobs.svn.ro" + job.find("a")["href"]
    city = translate_city(job.find("ul").find_all("li")[-1].text).replace("È", "s")
    county = get_county(city)

    jobs.append(
        create_job(
            job_title=job_title,
            job_link=job_link,
            company=company,
            country="Romania",
            city=city,
            county=county,
        )
    )


publish(4, company, jobs, "APIKEY")

publish_logo(company, "https://www.svn.ro/assets/images/logo/3.png")
show_jobs(jobs)
