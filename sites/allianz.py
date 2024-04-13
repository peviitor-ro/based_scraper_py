from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs
from math import ceil
import re

url = "https://careers.allianz.com/search/?searchby=location&createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_department=&optionsFacetsDD_shifttype=&optionsFacetsDD_customfield3=&optionsFacetsDD_customfield2=&optionsFacetsDD_facility=&optionsFacetsDD_customfield4=&inputSearchValue=Romania&quatFlag=false"
numberOfResults = 0

company = {"company": "Allianz"}
finaljobs = list()

scraper = Scraper()
scraper.get_from_url(url, "HTML")

pattern = re.compile(r'jobRecordsFound: parseInt\("(.*)"\)')

totalJobs = re.search(pattern, scraper.prettify()).group(1)

queryStrings = ceil(int(totalJobs) / 25)

for number in range(queryStrings):
    scraper.get_from_url(url + f"&startrow={number * 25}")
    elements = scraper.find_all("li", {"class": "job-tile"})
    finaljobs.extend(
        [
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
        ])

publish_or_update(finaljobs)

logoUrl = "https://rmkcdn.successfactors.com/cdd11cc7/5d49b267-5aa1-4363-8155-d.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)

