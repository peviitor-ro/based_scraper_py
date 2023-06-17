from scraper_peviitor import Scraper, loadingData
import uuid
import json

url = "https://jobs.diconium.com/en/api/filter/offers-content-category/diconium-jobs-en"

company = {"company": "Diconium"}
finalJobs = list()

d = [
    {"offerIds":["06685770-9ad1-4df6-850e-23ffb6447edd","e706bfc7-7468-43ee-b905-f2f4ae2092ad","e9f7171a-bdbb-4405-973d-72a455a1a762","5fc8f4a2-f06b-47e2-b842-2af6363479af","e3819d63-721a-5592-9555-de1e4cae9bf2","24363614-9610-4f7c-a1cb-d538b9fd1e07","d161583f-af61-54ab-9cd2-6fff912ff08c","fb016d75-6033-46ea-9b15-bb047a02f385","757ae33c-2f57-4c8d-9fa1-7bb2febf3297","74b6ad2b-b4bd-5df9-a366-cd5de1b5d2ec","74f9177c-4f59-4795-991e-0ad4c9d20010","cfcb7f4b-c708-407b-ac0b-e4ae66de7a59"],"categoryId":"59954e8a-f49e-5d4a-b37b-6177b94e1bb4","page":1},
    {"offerIds":["4ce04501-feff-4819-afc7-d61a0f86fff6","778252c0-12d5-4a5d-966e-b870396ba3e1","b9c3df71-d6ff-476e-ba3f-7387d11782fa","65690df5-8061-5c83-844b-8580a97e1ff6","c12b1c79-3f90-5d56-b4d7-a3c2606a1f50","e4e1b328-795f-5200-9010-e1e4e13584ed","f8ce9e79-afec-4c43-a379-b0443e815ec3","5b7e4d08-12c2-57d9-a2f4-9aa947c3cc99","b497e3f1-13be-4bc3-a058-2a21d83961e6","27758c65-87b4-4f8e-8e49-33eb66fc3f1f"],"categoryId":"4f732d55-7019-52ef-acac-01ee939a35f4","page":1},
    {"offerIds":["6a3c7ed8-4e80-4f7e-b304-beae23373843","d1fd0ff5-c60b-4e53-aa48-1914a1798ba5","db242fb7-0b0a-50be-9028-71678e9c8e6f","291ada3e-87bf-412c-bacc-1e0ff7aa06cd","3b9ef46e-6f06-4aa8-afa9-e321e5c39b24","407880b1-44c3-5150-a91e-4c1c4e5b3c4d","4a2c9195-12ed-5229-9955-a796cef17c5a","b55c9745-5fbb-4271-9ac1-07f059cb9d4d","64355c9f-d384-406c-8646-8e021fe6e6b7","9486dc9e-50fc-452e-aa6e-50121c014fd7","38eab780-39a9-5157-a0c6-f7ec78f20455","6ea9a2b6-575d-4774-a521-60da0af6eb6b","9eb07671-932f-5383-a217-630cc0961a2f"],"categoryId":"d9bc6913-a662-522f-8a76-93eb27a12e1b","page":1},
    {"offerIds":["630e5130-96d0-48dc-8350-9c54fa07fefa","96bf6540-b5f9-44bd-8ff2-6450c563bbb8","0ceeb2f5-100a-4581-9e58-385ff091a5cb","1c7b7180-a4cc-416e-9efc-3b06b6a06625","6c5a005f-4da9-4724-b853-9a10379cb234","501bf87f-27c8-4241-9738-25180f74d632","81739d5f-75af-4f7a-9675-070a82580dd9","78adef6e-85f8-4163-9e7a-274fecce3e74"],"categoryId":"fa67fad6-6ef8-4cea-b522-88e27c433458","page":1},
    {"offerIds":["da10504d-53de-4c78-aff2-d9da1623dac4","fefbcfbf-f8ab-457a-bd5e-33a0a9cc083a","ca2e06fa-e019-4150-bd0c-33a1f84ea82f","a2fcec55-dea8-4841-b0e1-4a3e8a2494fb","2c47f37a-3dc6-4fca-81ab-c79750a3ca0d"],"categoryId":"77f409c9-d6cd-5463-a053-36e2958a5d82","page":1}
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

            finalJobs.append({
                "id": str(id),
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": city
            })

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))

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