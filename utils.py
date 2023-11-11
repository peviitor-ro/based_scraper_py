import requests
import os
import json

def create_job(**kwargs):
    job = {}
    job.update(kwargs)
    return job

def clean(version, company, apikey):
    apikey = os.environ.get(apikey)
    content_type = "application/x-www-form-urlencoded"
    requests.post("https://api.peviitor.ro/v" + str(version) + "/clean/", headers={"apikey": apikey, "Content-Type": content_type}, data={"company": company})

def update(version, apikey, data):
    apikey = os.environ.get(apikey)
    content_type = "application/json"
    requests.post("https://api.peviitor.ro/v" + str(version) + "/update/", headers={"apikey": apikey, "Content-Type": content_type}, json=data)

def dataset(company, data):
    content_type = "application/json"
    requests.post(f"https://dev.laurentiumarian.ro/dataset/based_scraper_py/{company.lower()}.py/", headers={"Content-Type": content_type}, json={"data": len(data)})

def publish(version, company, data, apikey):
    clean(version, company, apikey)
    update(version, apikey, data)
    dataset(company, data)

def publish_logo(company, logo_url):
    content_type = "application/json"
    requests.post("https://api.peviitor.ro/v1/logo/add/", headers={"Content-Type": content_type}, json=[{
        "id": company,
        "logo": logo_url
    }])

def show_jobs(data):
    print(json.dumps(data, indent=4))

def translate_city(city):
    cities = {
        # This is general for all scrapers
        "bucharest": "Bucuresti",
        "cluj": "Cluj-Napoca",
        # This is for Arabesque Scraper
        "targul-mures": "Targu Mures",
        "militari": "Bucuresti",
        ############################
    }
    
    if cities.get(city.lower()):
        return cities.get(city.lower())
    else:
        return city
    
def acurate_city_and_county(**kwargs):
    city_and_county = {}
    city_and_county.update(kwargs)

    return city_and_county