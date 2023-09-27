from scraper_peviitor import Scraper, loadingData
import uuid
import json

apiUrl = "https://alliancewd.wd3.myworkdayjobs.com/wday/cxs/alliancewd/renault-group-careers/jobs"
scraper = Scraper()
# Cream un header pentru a putea face request-uri POST
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

# Cream un dictionar cu datele pe care dorim sa le trimitem catre server
data = {"appliedFacets": {"locationCountry": ["f2e609fe92974a55a05fc1cdc2852122"], "workerSubType": [
    "62e55b3e447c01871e63baa4ca0f9391", "62e55b3e447c01140817bba4ca0f9891", "62e55b3e447c01d10acebaa4ca0f9691"]}, "limit": 20, "offset": 0, "searchText": ""}

# Actualizam header-ul cu datele de mai sus
scraper.session.headers.update(headers)

# Facem request-ul POST si salvam numarul total de joburi
numberOfJobs = scraper.post(apiUrl, json=data).json().get("total")

# Cream o lista cu numerele de la 0 la numarul total de joburi, cu pasul de 20
iteration = [i for i in range(0, numberOfJobs, 20)]

company = {"company": "Renault"}
finaljobs = list()



# Pentru fiecare numar din lista, extragem joburile
for num in iteration:
    data["offset"] = num
    jobs = scraper.post(apiUrl, json=data).json().get("jobPostings")
    for job in jobs:
        id = uuid.uuid4()
        job_title = job.get("title").replace("[", "").replace("]", "")
        job_link = "https://alliancewd.wd3.myworkdayjobs.com/ro-RO/renault-group-careers" + \
            job.get("externalPath")
        city = job.get("bulletFields")[0]

        finaljobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city
        })

# afisam numarul total de joburi gasite
print(json.dumps(finaljobs, indent=4))

# se incarca datele in baza de date
loadingData(finaljobs, company.get("company"))
