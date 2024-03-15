import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

domain = os.environ.get("DOMAIN")

def get_token():
    """
    Returnează token-ul necesar pentru a face request-uri către API.
    :return: token-ul necesar pentru a face request-uri către API
    """
    endpoint = os.environ.get("TOKEN_ROUTE")
    email = os.environ.get("EMAIL")
    url = f'{domain}{endpoint}'
    response = requests.post(url, json={"email": email})
    return response.json()["access"]


def create_job(**kwargs):
    job = {}
    job.update(kwargs)
    return job


def clean(version, company, apikey):
    apikey = os.environ.get(apikey)
    content_type = "application/x-www-form-urlencoded"
    requests.post(
        "https://api.peviitor.ro/v" + str(version) + "/clean/",
        headers={"apikey": apikey, "Content-Type": content_type},
        data={"company": company},
    )


def update(version, apikey, data):
    apikey = os.environ.get(apikey)
    content_type = "application/json"
    requests.post(
        "https://api.peviitor.ro/v" + str(version) + "/update/",
        headers={"apikey": apikey, "Content-Type": content_type},
        json=data,
    )

    # VALIDATOR
    route = os.environ.get("ADD_JOBS_ROUTE")
    url = f"{domain}{route}"
    token = os.environ.get("TOKEN") if os.environ.get("TOKEN") else get_token()

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    requests.post(url, headers=headers, json=data)


def dataset(company, data):
    content_type = "application/json"
    requests.post(
        f"https://dev.laurentiumarian.ro/dataset/based_scraper_py/{company.lower()}.py/",
        headers={"Content-Type": content_type},
        json={"data": len(data)},
    )


def publish(version, company, data, apikey):
    clean(version, company, apikey)
    update(version, apikey, data)
    dataset(company, data)


def publish_logo(company, logo_url):
    content_type = "application/json"
    requests.post(
        "https://api.peviitor.ro/v1/logo/add/",
        headers={"Content-Type": content_type},
        json=[{"id": company, "logo": logo_url}],
    )


def show_jobs(data):
    print(json.dumps(data, indent=4))


def translate_city(city):
    city = city.replace(" ", "_")
    cities = {
        # This is general for all scrapers
        "bucharest": "Bucuresti",
        "cluj": "Cluj-Napoca",
        # This is for Arabesque Scraper
        "targul-mures": "Targu-Mures",
        "militari": "Bucuresti",
        ############################
        # This is for Vodafone Scraper
        "cluj_napoca": "Cluj-Napoca",
        "targu_mures": "Targu-Mures",
        "pipera": "Bucuresti",
        ############################
        # This is for ppt
        "campulung_muscel": "Campulung",
        # This is for Strabag
        "petrobrazi": "Ploiesti",
        # This is for CARTOFISSERIE
        "Satu-Mare": "Satu Mare",
        "Piatra_Neamt": "Piatra Neamt",
    }

    if cities.get(city.lower()):
        return cities.get(city.lower())
    else:
        return city.replace("_", " ")


def acurate_city_and_county(**kwargs):
    """
    Returns a dictionary containing accurate city and county information.

    Keyword Arguments:
    **kwargs -- key-value pairs representing city and county information

    Returns:
    A dictionary containing accurate city and county information.
    """
    city_and_county = {}
    if kwargs:
        city_and_county.update(kwargs)
    else:
        city_and_county = {
            "Satu_Mare": {"city": "Satu Mare", "county": "Satu Mare"},
            "Iasi": {"city": "Iasi", "county": "Iasi"},
            "Piatra_Neamt": {"city": "Piatra-Neamt", "county": "Neamt"},
            "Ramnicu_Valcea":{"city": "Ramnicu Valcea", "county": "Valcea"}
        }

    return city_and_county

def get_jobtype(sentence, **kwargs):
    """
    Get the job types mentioned in a sentence.

    Args:
        sentence (str): The sentence to analyze.
        **kwargs: Additional keyword arguments.
            jobs_typse (list): Additional job types to consider.

    Returns:
        list: A list of job types mentioned in the sentence.
    """
    jobs_typse = ["on-site", "remote", "hybrid"]
    jobs_typse.extend(kwargs.get("jobs_typse", []))
    types = [
        jobtype for jobtype in jobs_typse if jobtype in sentence.lower()
    ]

    return list(set(types))
