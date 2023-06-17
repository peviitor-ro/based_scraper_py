from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import re 
import json

#url-ul paginii
url = "https://careers.allianz.com/search/?searchby=location&createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_department=&optionsFacetsDD_shifttype=&optionsFacetsDD_customfield3=&optionsFacetsDD_customfield2=&optionsFacetsDD_facility=&optionsFacetsDD_customfield4=&inputSearchValue=Romania&quatFlag=false"
#Numarul de rezultate de pe pagina
numberOfResults = 0

company = {"company": "Allianz"}
finaljobs = list()

#Cream un nou scraper
scraper = Scraper(url)
#Cream un nou obiect Rules
rules = Rules(scraper)

pattern = re.compile(r'jobRecordsFound: parseInt\("(.*)"\)')
#Luam numarul total de joburi
totalJobs = re.search(pattern, scraper.soup.prettify()).group(1)
#Cream o lista cu numerele de la 0 la numarul total de joburi
queryStrings = [*range(0, int(totalJobs), 25)]

for number in queryStrings:
    #Setam url-ul paginii
    scraper.url = url + f"https://careers.allianz.com/tile-search-results?q=&locationsearch=Romania&searchby=location&d=15&startrow={number}"
    #Luam toate joburile
    elements = rules.getTags("li", {"class": "job-tile"})
    #Pentru fiecare job luam titlul, linkul, compania, tara si orasul
    for element in elements:
        id = uuid.uuid4()
        job_title = element.find("a").text.strip()
        job_link = "https://careers.allianz.com" + element.find("a").get("href")

        finaljobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": "Romania",
        })

#Afisam numarul de total de joburi
print(json.dumps(finalJobs, indent=4))

#Incarcam datele in baza de date
loadingData(finaljobs, company.get("company"))