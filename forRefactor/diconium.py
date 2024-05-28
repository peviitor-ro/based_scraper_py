from scraper.Scraper import Scraper
from utils import publish, publish_logo, show_jobs
import json

url = "https://jobs.diconium.com/en/category/automotive-engineering/fa67fad6-6ef8-4cea-b522-88e27c433458"
company = "Diconium"

scraper = Scraper()
scraper.get_from_url(url)

jobs = scraper.find_all("a", {"data-type": "category"})
print(len(jobs))

# url = "https://jobs.diconium.com/en/api/filter/offers/diconium-jobs-en"
# company = "Diconium"

# post_data = {
#     "offerIds": [
#         "04f5d025-f570-4b42-8535-e3f58254758d",
#         "28b554da-a78e-43f6-8042-e277d6bed3a9",
#         "4039539f-7c98-4c8d-a7b1-6b04cada8b02",
#         "6e0c01e9-f454-4d57-a83b-105194ee701b",
#         "713db2b7-eca7-48f4-819c-b546110ca451",
#         "87d0af76-2780-4c04-a597-677ba0624618",
#         "a95672f8-6749-4d9a-aac1-35a0fbd86b8f",
#         "b267cbc3-4ecd-4ec4-897d-6e57b51705b2",
#         "c6e0c203-f505-4e41-aebb-c283d6136c47",
#         "d7603612-ba40-485e-82df-f1629ca24124",
#         "080dd414-0312-4755-95db-0e17b5d77162",
#         "181f957b-23a3-4a72-b7be-66a244589698",
#         "4418642d-7190-4d88-91a9-e54156b1f0c8",
#         "64ba335f-0537-4d80-a47a-883a0f19bbd7",
#         "68294479-cc38-4bae-8d8b-bd049791dab5",
#         "76070df7-4048-4da3-b081-c64dab2a6847",
#         "8ca2ad4a-0b29-43a8-96e9-927c04f11829",
#         "9cd9a7c2-3ce5-4362-a50e-644e5c41f92e",
#         "c8139668-0664-4279-bcd0-709218669496",
#         "1cc41f33-9226-47fa-b786-a2f238516041",
#         "a76311d6-f452-4dc9-8ae7-976fb9975e87",
#         "3de12183-ff92-4d30-a433-b491a41bd025",
#         "29fa1f8d-4ab5-443b-8ced-f655b169fd39",
#         "7d4f5557-7b6e-44fb-8c10-350052c680ba",
#         "84ef5c2c-e951-4f75-847a-8d39969df2b9",
#         "92e38685-24f8-4f11-b5ec-4faf94184bcc",
#         "bb604428-bf7b-4d9e-879d-8543d50aab8b",
#         "824363ca-590e-4691-8946-3ef4b7d0a77f",
#         "90aef9a9-d1ea-4848-8609-df677213795a",
#         "9d38ff49-6871-4de8-bc15-00b19d90376d",
#         "a7448835-52ca-401f-9652-eefc99de400a",
#         "c9bba5b8-37d4-4904-922e-9785de89bf7c",
#         "cdac876a-aeaf-443b-84fd-e480726985ee",
#         "0511837a-0185-4776-818d-95e5a70ccb77",
#         "19b7344f-e2b2-4d2d-bc8b-215fd89ac43b",
#         "3f834b44-bbb9-410c-a2b1-edc123ce525c",
#         "4021a576-a4bc-400f-bbb5-9145c954d3a8",
#         "4c4a008e-9185-4e31-9a10-b43a4b3bdcc7",
#         "5b26024c-b72c-43c2-bb65-77ce5a887604",
#         "614db216-63fd-43d8-9349-3bfdc231f1cd",
#         "71931fd5-7316-466e-a9d0-ebf09cac4b67",
#         "7290a6db-1da8-4262-b26a-ad9ec6948bcf",
#         "76b2b497-bcac-45e4-ac09-29f93856fec3",
#         "801e3d35-9a53-4834-8365-79e9c0fe1c25",
#         "907ec6c3-8394-4a5d-84df-ba625a11f7fb",
#         "9bbf12eb-4692-47df-9801-b39ae40dd205",
#         "9c758d62-2df5-4b1f-8d41-ee989507a387",
#         "a572230f-b12d-44d8-ad87-8aae30ab9f1a",
#         "bd90564c-b956-4a7b-9920-7eaee11a2e1e",
#         "c9eb1af4-7b94-407a-87f0-e58d8d7e1abe",
#         "d7ddda71-854a-4a1a-8b52-d80a8ef3e638",
#         "eb48460d-da05-49a0-a8eb-4b829a2d6022",
#         "0756f29e-6a3d-4bfd-9fa9-ae4f21874406",
#         "36a41054-6d1f-4f6f-845e-e6f6d8c64f69",
#         "4efc91e8-a9f1-46e7-983f-c1cbb989c403",
#         "61056063-f13e-46c8-9db2-ab6472c7f634",
#         "848a57c2-7b45-4c6f-a71c-cbf5ec8f0ccb",
#         "8c42a9ca-8f36-45fc-8e38-11166fc2a2fa",
#         "f2cec267-dc11-4407-b3cb-ae69a4a38766",
#         "f4dbbd93-e51a-4d7b-9afa-ecac6c2f57bd",
#         "3a653f7d-2d2e-4d0a-b8a6-22a5baf60240",
#         "977dc8bb-95df-4e6a-9ba2-cce87dd66ee6",
#         "c0537eb0-10ff-49de-be5d-f1e305aa7207",
#         "c18d9d3e-66c0-4159-b27c-d1ee930a4b94",
#         "f5dcb0a3-1002-4332-9e8c-cb3131f72ba1",
#         "697b48d2-2941-4527-bcb4-c5b07e69e5e6",
#         "f17d16a4-a64a-44fa-b7b2-f27d89cbe5df",
#         "058487b6-8739-4137-94e5-44e60dc59994",
#         "08a005b5-a75e-46c8-82a6-db684d8f375a",
#         "baaccde1-248a-415b-9d83-2b5ec24a2e27",
#         "c11911e8-3985-4caf-8df9-7f2d65d0d1ac",
#         "f597af2f-b6a3-4f00-9667-d0442c36ed48",
#         "6f93fa41-4caf-44e2-9eae-b5e3d6fc559b",
#         "9f830770-7207-4e40-9540-88067b584594",
#         "fb8fbdf6-164d-4c7c-b252-338234baddc4",
#         "fff9d2b1-6eba-4ef1-8956-ffb41f571d7e",
#         "48aca31d-72cb-4e11-8cbf-3410c5c6d75d",
#         "c7bdd6ae-77e3-4d43-91cb-a3aa692a3f13",
#         "cc63b6e7-4fd1-4daf-84a8-571641ad9aab",
#     ]
# }

# scraper = Scraper()
# scraper.set_headers({"Content-Type": "application/json"})
# response= scraper.post(url, json.dumps(post_data))

# print(response.json().get("offerIdsFound"))

# post_data = {
#     "offerIds": response.json().get("offerIdsFound"),
#     "categoryId": "59954e8a-f49e-5d4a-b37b-6177b94e1bb4",
#     "page": 1,
# }
# html = scraper.post(url, json.dumps(post_data)).json().get("html")
# scraper.__init__(html, "html.parser")
# jobs = scraper.find_all("a")

# finalJobs = [
#     {
#         "job_title": job.find("div", {"class": "h3"}).text.strip(),
#         "job_link": job.get("href"),
#         "company": company,
#         "country": "Romania",
#         "city": "Bucuresti",
#         "county": "Bucuresti",
#     }
#     for job in jobs
#     if job.find("div", {"class": "p cityNames"}).text.strip() == "Bucharest"
# ]

# publish(4, company, finalJobs, "APIKEY")

# logoUrl = "https://jobs.diconium.com/en/uploads/1623/settings/companies/diconium-jobs-en-96-6059ae9f8dd12.png"
# publish_logo(company, logoUrl)

# show_jobs(finalJobs)
