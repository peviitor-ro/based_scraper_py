from scraper.Scraper import Scraper
from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty, remove_diacritics
from math import ceil

_counties = GetCounty()
url = "https://cariere.otpbank.ro/Posturi"
scraper = Scraper()
scraper.get_from_url(url)

number_of_jobs = int(scraper.find("div", {"class": "page-subtitle-counter"}).text.split(" ")[0])

pages = ceil(number_of_jobs / 10)

company = {"company": "OTPBank"}
finalJobs = list()

for page in range(1,pages + 1):
    page_url = f"https://cariere.otpbank.ro/Posturi?page={page}"
    scraper.get_from_url(page_url)
    elements = scraper.find_all("div", {"class": "vacancy-item"})

    for element in elements:
        job_title = element.find("h2").find("a").text
        job_link = "https://cariere.otpbank.ro" + element.find("h2").find("a")["href"]

        try:
            city = translate_city(remove_diacritics(element.find("span", {"class": "more"}).text.split("-")[0].strip()))
        except:
            city = translate_city(remove_diacritics(element.find("span", {"class": "more"}).text))

        county = _counties.get_county(city)

        if not county:
            city = city.replace(" ", "-")
            county = _counties.get_county(city)

        finalJobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county
        })


publish_or_update(finalJobs)

logo_url = "https://www.otpbank.ro/themes/otpbank/logo.svg"
publish_logo(company.get("company"), logo_url)
show_jobs(finalJobs)
