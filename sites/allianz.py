from scraper_peviitor import Scraper, Rules
import re
from utils import publish, publish_logo, show_jobs

# url-ul paginii
url = "https://careers.allianz.com/search/?searchby=location&createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_department=&optionsFacetsDD_shifttype=&optionsFacetsDD_customfield3=&optionsFacetsDD_customfield2=&optionsFacetsDD_facility=&optionsFacetsDD_customfield4=&inputSearchValue=Romania&quatFlag=false"
# Numarul de rezultate de pe pagina
numberOfResults = 0

company = {"company": "Allianz"}
finaljobs = list()

# Cream un nou scraper
scraper = Scraper(url)
# Cream un nou obiect Rules
rules = Rules(scraper)

pattern = re.compile(r'jobRecordsFound: parseInt\("(.*)"\)')
# Luam numarul total de joburi
totalJobs = re.search(pattern, scraper.soup.prettify()).group(1)
# Cream o lista cu numerele de la 0 la numarul total de joburi
queryStrings = [*range(0, int(totalJobs), 25)]

for number in queryStrings:
    # Setam url-ul paginii
    scraper.url = (
        url
        + f"https://careers.allianz.com/tile-search-results?q=&locationsearch=Romania&searchby=location&d=15&startrow={number}"
    )
    # Luam toate joburile
    elements = rules.getTags("li", {"class": "job-tile"})
    finaljobs = [
        {
            "job_title": element.find("a").text.strip(),
            "job_link": "https://careers.allianz.com" + element.find("a").get("href"),
            "company": company.get("company"),
            "country": "Romania",
            "city": "Bucuresti",
            "county": "Bucuresti",
            "remote": ["Hybrid"],
        }
        for element in elements
    ]

publish(4, company.get("company"), finaljobs, "APIKEY")

logoUrl = "https://rmkcdn.successfactors.com/cdd11cc7/5d49b267-5aa1-4363-8155-d.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)
