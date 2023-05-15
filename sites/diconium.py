from scraper_peviitor import Scraper, loadingData
import uuid
import json

url = "https://jobs.diconium.com/en/api/filter/offers-content-category/diconium-jobs-en"

company = {"company": "Diconium"}
finalJobs = list()

d = [
    {"offerIds":["e9f7171a-bdbb-4405-973d-72a455a1a762","5fc8f4a2-f06b-47e2-b842-2af6363479af","e3819d63-721a-5592-9555-de1e4cae9bf2","5f98d15f-dcad-46d9-87de-46d2040d32fd","d161583f-af61-54ab-9cd2-6fff912ff08c","fb016d75-6033-46ea-9b15-bb047a02f385","0902bec5-aff3-4b0f-bc27-6f401db6e159","5ea2ee79-c8eb-503c-b1a7-fdd2e37a506c","757ae33c-2f57-4c8d-9fa1-7bb2febf3297","93bb2445-4bc9-452a-ba85-7375a04b06b3","a2fcec55-dea8-4841-b0e1-4a3e8a2494fb","74b6ad2b-b4bd-5df9-a366-cd5de1b5d2ec","cfcb7f4b-c708-407b-ac0b-e4ae66de7a59"],"categoryId":"59954e8a-f49e-5d4a-b37b-6177b94e1bb4","page":1},
    {"offerIds":["75e8331b-83a9-5b6b-8437-73cd93e457a3","778252c0-12d5-4a5d-966e-b870396ba3e1","b9c3df71-d6ff-476e-ba3f-7387d11782fa","65690df5-8061-5c83-844b-8580a97e1ff6","c12b1c79-3f90-5d56-b4d7-a3c2606a1f50","e4e1b328-795f-5200-9010-e1e4e13584ed","f8ce9e79-afec-4c43-a379-b0443e815ec3","c47632bc-7b65-4b51-9ea3-dfc527bcc598","5b7e4d08-12c2-57d9-a2f4-9aa947c3cc99","b497e3f1-13be-4bc3-a058-2a21d83961e6","27758c65-87b4-4f8e-8e49-33eb66fc3f1f"],"categoryId":"4f732d55-7019-52ef-acac-01ee939a35f4","page":1},
    {"offerIds":["0e255921-52f6-58c0-a2e6-64afd55fc8de"],"categoryId":"667a3ab1-2ff5-5be7-9b93-13101f4cfc2c","page":1},
    {"offerIds":["6a3c7ed8-4e80-4f7e-b304-beae23373843","c17cb685-0c4d-58a4-be4b-355241473019","db242fb7-0b0a-50be-9028-71678e9c8e6f","8cb49514-2c6c-473a-93bb-416f61ee70f4","3b9ef46e-6f06-4aa8-afa9-e321e5c39b24","407880b1-44c3-5150-a91e-4c1c4e5b3c4d","4a2c9195-12ed-5229-9955-a796cef17c5a","b55c9745-5fbb-4271-9ac1-07f059cb9d4d","64355c9f-d384-406c-8646-8e021fe6e6b7","9486dc9e-50fc-452e-aa6e-50121c014fd7","359c8985-6fcb-411f-9358-633aa981fd83","38eab780-39a9-5157-a0c6-f7ec78f20455","6ea9a2b6-575d-4774-a521-60da0af6eb6b","9eb07671-932f-5383-a217-630cc0961a2f"],"categoryId":"d9bc6913-a662-522f-8a76-93eb27a12e1b","page":1},
    {"offerIds":["da10504d-53de-4c78-aff2-d9da1623dac4","ca2e06fa-e019-4150-bd0c-33a1f84ea82f","989265f8-8ab8-430e-90be-381251501045"],"categoryId":"77f409c9-d6cd-5463-a053-36e2958a5d82","page":1}
]

scraper = Scraper()

for data in d:

    response = scraper.post(url, json.dumps(data))
    html = response.json().get("html")
    scraper.soup = html

    jobs = scraper.soup.findAll("a", {"class": "shont item"})

    for job in jobs:
        location = job.find("div", {"class": "p cityNames"}).text.strip()

        if location == "Bucharest":
            id = uuid.uuid4()
            job_title = job.find("div", {"class":"h3"}).text.strip()
            job_link = job.get("href")
            city = location

            print(job_title + " -> " + city)

            finalJobs.append({
                "id": str(id),
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": city
            })

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", company.get("company"))

logoUrl = "https://jobs.diconium.com/en/uploads/1623/settings/companies/diconium-jobs-en-96-6059ae9f8dd12.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))