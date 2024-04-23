from scraper.Scraper import Scraper
from utils import (
    translate_city,
    acurate_city_and_county,
    publish_or_update,
    publish_logo,
    show_jobs,
)
from getCounty import GetCounty
from math import ceil

_counties = GetCounty()
url = "https://d-career.org/Draexlmaier/go/DRÄXLMAIER-Job-Opportunities-in-Romania-%28Romanian%29/4196801/0/?q=&sortColumn=referencedate&sortDirection=desc"
scraper = Scraper()
scraper.get_from_url(url)

jobsnumbers = scraper.find("span", {"class": "paginationLabel"}).find_all("b")[1].text

jobsPerPage = ceil(int(jobsnumbers) / 25)

company = {"company": "Draxlmaier"}
finaljobs = list()

acurate_city = acurate_city_and_county(
    Codlea_Brasov={"city": "Codlea", "county": "Brasov"},
    Satu_Mare={"city": "Satu Mare", "county": "Satu Mare"},
)

for jobs in range(jobsPerPage):
    if jobs == 0:
        pageLink = "https://d-career.org/Draexlmaier/go/DRÄXLMAIER-Job-Opportunities-in-Romania-%28Romanian%29/4196801/?q=&sortColumn=referencedate&sortDirection=desc"
    else:
        pageLink = f"https://d-career.org/Draexlmaier/go/DRÄXLMAIER-Job-Opportunities-in-Romania-%28Romanian%29/4196801/{jobs * 25}/?q=&sortColumn=referencedate&sortDirection=desc"

    scraper.get_from_url(pageLink)

    elements = scraper.find_all("tr", {"class": "data-row"})

    for element in elements:
        job_title = element.find("a", {"class": "jobTitle-link"}).text
        job_link = (
            "https://d-career.org"
            + element.find("a", {"class": "jobTitle-link"})["href"]
        )
        city = translate_city(
            element.find("span", {"class": "jobLocation"}).text.split(",")[0].strip()
        )
        county = None

        if acurate_city.get(city.replace(" ", "_")):
            county = acurate_city.get(city.replace(" ", "_")).get("county")
            city = acurate_city.get(city.replace(" ", "_")).get("city")

        else:
            county = _counties.get_county(city)

        finaljobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
                "county": county,
            }
        )

publish_or_update(finaljobs)

logoUrl = "https://rmkcdn.successfactors.com/0141de78/80376284-e029-4c8c-8f6f-6.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)
