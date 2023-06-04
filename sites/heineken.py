from scraper_peviitor import Scraper, Rules, loadingData
import uuid

scraper = Scraper()
rules = Rules(scraper)

jobsFound = True

startRow = 0

finalJobs = list()

while jobsFound:
    scraper.url = f"https://careers.theheinekencompany.com/search/?createNewAlert=false&q=&locationsearch=Romania&startrow={startRow}"
    jobs= rules.getTags("tr", {"class": "data-row"})
    for job in jobs:
        if job.find("span", {"class": "jobLocation"}).text.split(",")[1].strip() != "RO":
            jobsFound = False
            break
        id = uuid.uuid4()
        job_title = job.find("span", {"class": "jobTitle"}).text.strip()
        job_link = "https://careers.theheinekencompany.com" + job.find("a", {"class": "jobTitle-link"}).get("href")
        company = "Heineken"
        country = "Romania"
        city = job.find("span", {"class": "jobLocation"}).text.split(",")[0].strip()

        print(job_title + " -> " + city)

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city
        })

    startRow += 25

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, "Heineken")
