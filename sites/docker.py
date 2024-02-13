from scraper_peviitor import Scraper
from utils import publish, publish_logo, show_jobs
import json

url = "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams"

company = {"company": "docker"}
finalJobs = list()

scraper = Scraper()
scraper.session.headers.update(
    {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
)
data = {
    "operationName": "ApiJobBoardWithTeams",
    "variables": {"organizationHostedJobsPageName": "docker"},
    "query": "query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {\n  jobBoard: jobBoardWithTeams(\n    organizationHostedJobsPageName: $organizationHostedJobsPageName\n  ) {\n    teams {\n      id\n      name\n      parentTeamId\n      __typename\n    }\n    jobPostings {\n      id\n      title\n      teamId\n      locationId\n      locationName\n      employmentType\n      secondaryLocations {\n        ...JobPostingSecondaryLocationParts\n        __typename\n      }\n      compensationTierSummary\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment JobPostingSecondaryLocationParts on JobPostingSecondaryLocation {\n  locationId\n  locationName\n  __typename\n}",
}

jobs = (
    scraper.post(url, data=json.dumps(data))
    .json()
    .get("data")
    .get("jobBoard")
    .get("jobPostings")
)

for job in jobs:
    job_title = job.get("title")
    job_link = "https://www.docker.com/career-openings/?ashby_jid=" + job.get("id")
    countrys = job.get("secondaryLocations")

    for country in countrys:
        city = country.get("locationName")
        if city == "Romania":
            finalJobs.append(
                {
                    "job_title": job_title,
                    "job_link": job_link,
                    "company": company.get("company"),
                    "country": "Romania",
                    "remote": "Remote",
                }
            )

publish(4, company.get("company"), finalJobs, "APIKEY")

logoUrl = (
    "https://www.docker.com/wp-content/uploads/2022/03/vertical-logo-monochromatic.png"
)
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
