import unicodedata
import requests

abreviate_counties = {
    "ab": {"city": "Alba Iulia", "county": "Alba"},
    "ar": {"city": "Arad", "county": "Arad"},
    "ag": {"city": "Pitesti", "county": "Arges"},
    "bc": {"city": "Bacau", "county": "Bacau"},
    "bh": {"city": "Oradea", "county": "Bihor"},
    "bn": {"city": "Bistrita", "county": "Bistrita-Nasaud"},
    "bt": {"city": "Botosani", "county": "Botosani"},
    "br": {"city": "Braila", "county": "Braila"},
    "bv": {"city": "Brasov", "county": "Brasov"},
    "b": {"city": "Bucuresti", "county": "Bucuresti"},
    "bz": {"city": "Buzau", "county": "Buzau"},
    "cl": {"city": "Calarasi", "county": "Calarasi"},
    "cs": {"city": "Resita", "county": "Caras-Severin"},
    "cj": {"city": "Cluj-Napoca", "county": "Cluj"},
    "ct": {"city": "Constanta", "county": "Constanta"},
    "cv": {"city": "Sfantu Gheorghe", "county": "Covasna"},
    "db": {"city": "Targoviste", "county": "Dambovita"},
    "dj": {"city": "Craiova", "county": "Dolj"},
    "gl": {"city": "Galati", "county": "Galati"},
    "gr": {"city": "Giurgiu", "county": "Giurgiu"},
    "gj": {"city": "Targu Jiu", "county": "Gorj"},
    "hg": {"city": "Miercurea Ciuc", "county": "Harghita"},
    "hr": {"city": "Hunedoara", "county": "Hunedoara"},
    "hd": {"city": "Deva", "county": "Hunedoara"},
    "il": {"city": "Slobozia", "county": "Ialomita"},
    "is": {"city": "Iasi", "county": "Iasi"},
    "if": {"city": "Buftea", "county": "Ilfov"},
    "mm": {"city": "Baia Mare", "county": "Maramures"},
    "mh": {"city": "Drobeta-Turnu Severin", "county": "Mehedinti"},
    "ms": {"city": "Targu-Mures", "county": "Mures"},
    "nt": {"city": "Piatra-Neamt", "county": "Neamt"},
    "ot": {"city": "Slatina", "county": "Olt"},
    "ph": {"city": "Ploiesti", "county": "Prahova"},
    "sj": {"city": "Zalau", "county": "Salaj"},
    "sm": {"city": "Satu Mare", "county": "Satu Mare"},
    "sb": {"city": "Sibiu", "county": "Sibiu"},
    "sv": {"city": "Suceava", "county": "Suceava"},
    "tr": {"city": "Alexandria", "county": "Teleorman"},
    "tm": {"city": "Timisoara", "county": "Timis"},
    "tl": {"city": "Tulcea", "county": "Tulcea"},
    "vl": {"city": "Ramnicu Valcea", "county": "Valcea"},
    "vs": {"city": "Vaslui", "county": "Vaslui"},
    "vn": {"city": "Focsani", "county": "Vrancea"},
}


def has_diacritics(char):
    return any(unicodedata.combining(c) for c in char)


def remove_diacritics(input_string):
    normalized_string = unicodedata.normalize("NFD", input_string)
    return "".join(char for char in normalized_string if not has_diacritics(char))


def get_county(city):
    api_endpoint = f"https://api.laurentiumarian.ro/orase/?search={remove_diacritics(city)}&page_size=50"
    cities = []
    
    response = requests.get(api_endpoint).json()

    while response.get("next") is not None:
        cities.extend(response.get("results"))
        response = requests.get(response.get("next")).json()
    else:
        cities.extend(response.get("results"))

    county = [
        item.get("county") for item in cities if item.get("name") == remove_diacritics(city.title())
    ]

    return county if county else None
