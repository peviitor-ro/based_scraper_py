from scraper_peviitor import Scraper, Rules, loadingData
import json
from getCounty import get_county, remove_diacritics
from utils import translate_city

# Cream o instanta a clasei Scraper
scraper = Scraper("https://www.synevo.ro/cariere/")
rules = Rules(scraper)

# Luam toate categoriile de joburi
jobsCategory = rules.getTags("div", {"class": "job-cat-post"})

company = {"company": "Synevo"}
finaljobs = list()

# Pentru fiecare categorie de joburi luam linkul si mergem pe pagina
for jobCategory in jobsCategory:
    # Luam linkul categoriei de joburi
    jobCategoryLink = jobCategory.find("a")["href"]
    # Mergem pe pagina categoriei de joburi
    scraper.url = jobCategoryLink

    # Luam toate joburile din categoria respectiva
    job_link = rules.getTags("a", {"class": "jobs-link"})

    for job in job_link:
        # Mergem pe pagina jobului
        scraper.url = job["href"]
        # Luam titlul jobului si orasele in care se poate lucra
        job_title = rules.getTag("h1", {"class": "entry-title"}).text
        # Daca sunt mai multe orase le impartim in lista
        # try :
        locations = rules.getTag(
            "div", {"class": "jobs-info-city"}).find("b").text.split(",")

        cities = list()
        counties = set()

        for city in locations:
            if "Chiajna" in city:
                city = "Chiajna"
            else:
                city = translate_city(
                    remove_diacritics(city.strip())
                )

            cities.append(city)
            counties.add(get_county(city))

        # Cream un dictionar cu jobul si il adaugam in lista finala

        finaljobs.append({
            "job_title": job_title,
            "job_link": scraper.url,
            "company": company.get("company"),
            "country": "Romania",
            "city": cities,
            "county": list(counties),
        })

# #Afisam numarul total de joburi
print(json.dumps(finaljobs, indent=4))

# #Incarcam datele in baza de date
loadingData(finaljobs, company.get("company"))
