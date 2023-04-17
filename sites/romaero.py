from scraper_peviitor import Scraper, Rules, loadingData

url = "https://romaero.com/cariere/locuri-de-munca-romaero/"

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTags("tr")

finalJobs = list()

for job in jobs:
    try:
        job_title = job.find("strong").text.strip()
        job_link = job.find("a").get("href")
        company = "Romaero"
        country = "Romania"
        city = "Romania"

        finalJobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city
        })

        print(job_title + " -> " + city)

    except:
        pass

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", "Romaero")