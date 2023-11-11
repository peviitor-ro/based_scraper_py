from scraper_peviitor import Scraper, Rules, loadingData
import json
from getCounty import get_county
from utils import translate_city, acurate_city_and_county

url = "https://cariere.arabesque.ro"

scraper = Scraper(url)
rules = Rules(scraper)

#Luam toate categoriile de joburi
categories = rules.getTags("div", {"class": "arabesque_homepage_template_categorie"})

company = {"company": "Arabesque"}
finalJobs = list()

acurate_city = acurate_city_and_county(
    Iasi={"city": "Iasi", "county": "Iasi"},
)

#Pentru fiecare categorie de joburi
for category in categories:
    #Luam joburile din categoria respectiva
    jobs = category.find_all("article")

    #Luam link-ul catre pagina cu joburile din categoria respectiva
    categoryUrl = category.find("a",{"class", "arabesque_home_go_to"}).get("href").replace("https://cariere.arabesque.ro/jobs/", "")
    #Cream un link catre pagina cu jobul respectiv
    jobUrl = "https://cariere.arabesque.ro/jobs/" + "job/" + categoryUrl.replace(" ", "%20")


    #Daca sunt mai mult de 4 joburi in categoria respectiva atunci trebuie sa mergem pe pagina cu joburile
    if len(jobs) >= 4:
        #Luam link-ul catre pagina cu joburile din categoria respectiva
        urlPage = category.find("a",{"class", "arabesque_home_go_to"}).get("href").replace(" ", "%20")
        #Se crea un nou scraper pentru pagina cu joburile din categoria respectiva
        scraperPage = Scraper(urlPage)
        pageRules = Rules(scraperPage)
        #Se cauta div-ul cu joburile
        jobsContainer = pageRules.getTag("div", {"class": "arabesque_homepage_template"})
        #Se cauta toate joburile
        jobs = jobsContainer.find_all("article")

    for job in jobs:
        job_title = job.find("h4").text.strip()
        job_link = job.get("id").replace("post-", jobUrl + "&job_id=")
        city = translate_city(job_title.split(" ")[-1].strip().title())

        county = get_county(city)

        if acurate_city.get(city):
            city = acurate_city.get(city).get("city")
            county = acurate_city.get(city).get("county")

        elif not county:

            first_name = job_title.split(" ")[-2].strip().title()
            city = translate_city(first_name + "-" + city)
            county = get_county(city)

            if not county:

                city = "Bucuresti"
                county = "Bucuresti"

        finalJobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county
        })

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))

