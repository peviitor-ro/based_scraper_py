from scraper_peviitor import Scraper, loadingData
import uuid
import json

url = "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams"

company = {"company": "docker"}
finalJobs = list()

scraper = Scraper()
scraper.session.headers.update({
    "Content-Type": "application/json",
    "Accept": "application/json",
})
data = {
    "operationName":"ApiJobBoardWithTeams",
    "variables":{"organizationHostedJobsPageName":"docker"},
    "query":"query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {\n  jobBoard: jobBoardWithTeams(\n    organizationHostedJobsPageName: $organizationHostedJobsPageName\n  ) {\n    teams {\n      id\n      name\n      parentTeamId\n      __typename\n    }\n    jobPostings {\n      id\n      title\n      teamId\n      locationId\n      locationName\n      employmentType\n      secondaryLocations {\n        ...JobPostingSecondaryLocationParts\n        __typename\n      }\n      compensationTierSummary\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment JobPostingSecondaryLocationParts on JobPostingSecondaryLocation {\n  locationId\n  locationName\n  __typename\n}"
    }

# scraper.post(url, data=json.dumps(data))

jobs = scraper.post(url, data=json.dumps(data)).json().get("data").get("jobBoard").get("jobPostings")

for job in jobs:
    id = uuid.uuid4()
    job_title = job.get("title")
    job_link = "https://www.docker.com/career-openings/?ashby_jid=" + job.get("id")

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": "Romania"
    })

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))

logoUrl = "https://www.docker.com/wp-content/uploads/2022/03/vertical-logo-monochromatic.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))
