from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs

url = "https://jobs.telusdigital.com/en_US/careers/SearchPipelines/?2952=5170&2952_format=8850&listFilterMode=1"

company = "TelusDigital"

scraper = Scraper()
header = {
    "Cookie": "aws-waf-token=9c9763c5-07ff-4155-9a21-7ec80d88cf9a:EQoApP2V8kxFAQAA:DPP3PT7CcsQ7VRWZT48yUxYAcG+oKPNaMWHbQ0kLhhBcf6BxtQ5FO1I55ks2AREA96BI2FI5CzdvnlDVFo7QmenLckU1RM+cZkaI+WtImwqxvbQZ9KqUP7QhfkUX+4xmmMhXMmFDUXar/UayBCkfKkzk1WAU4Qxx51yUt8GGt/tRL2+96GOOXTuXlmwVB3l1wVDBsb3KOc0=; ScustomPortal-11=apl7clg0h888mf3ksmqbsekool; portalLanguage-11=en_US; _gcl_au=1.1.2116609567.1734816773; _pk_id.1.4519=b59ab3422a724e9f.1734816773.; _pk_ses.1.4519=1; TAsessionID=b84dafa1-0ef2-4b80-9365-063dec1cf681|NEW; notice_behavior=expressed,eu; _gid=GA1.2.1720182607.1734816773; _gat_UA-127033133-1=1; _tt_enable_cookie=1; _ttp=e95CQep40vLcsS9UCukimSbcWDs.tt.1; _hjSession_1951975=eyJpZCI6IjE3MTRiZWZkLWE3NDctNDM2MC04YjIyLTM4ZWNiNzZhYjM4MSIsImMiOjE3MzQ4MTY3NzMwMDUsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; geoForGtm=RO; notice_preferences=2:; notice_gdpr_prefs=0,1,2:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; _ga_T6FDVD598X=GS1.1.1734816772.1.1.1734816797.35.0.0; _hjSessionUser_1951975=eyJpZCI6ImY5NTIwYzViLTE0MmItNWEwMS1hNjVlLTk1YzE1ODk4YjAxOCIsImNyZWF0ZWQiOjE3MzQ4MTY3NzMwMDUsImV4aXN0aW5nIjp0cnVlfQ==; _ga=GA1.2.583769459.1734816773; _ga_MQSHH38K07=GS1.1.1734816772.1.1.1734816820.0.0.551024211"
}

scraper.set_headers(header)
scraper.get_from_url(url, verify=False)

jobs = scraper.find_all("li", {"class": "listSingleColumnItem"})


finalJobs = [
    {
        "job_title": job.find("h3").text.strip(),
        "job_link": job.find("h3").find("a").get("href"),
        "company": company,
        "country": "Romania",
        "city": "Bucuresti",
        "county": "Bucuresti",
    }
    for job in jobs
]


publish_or_update(finalJobs)
publish_logo(
    company,
    "https://jobs.telusinternational.com/portal/11/images/logo_telus-international_header-v2.svg",
)
show_jobs(finalJobs)
