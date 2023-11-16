from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

#Cream o instanta a clasei Scraper
scraper = Scraper("https://d-career.org/Draexlmaier/go/DRÄXLMAIER-Job-Opportunities-in-Romania-%28Romanian%29/4196801/0/?q=&sortColumn=referencedate&sortDirection=desc")
rules = Rules(scraper)

#Cautam numarul de joburi
jobsnumbers = rules.getTag("span", {"class":"paginationLabel"}).find_all("b")[1].text

#Cream o lista cu numerele de joburi de 25 in 25
jobsPerPage = [i for i in range(0 , int(jobsnumbers), 25) ]

#Cream un dictionar in care vom salva joburile
company = {"company": "Draxlmaier"}
finaljobs = list()

#Pentru fiecare numar din lista, extragem joburile
for jobs in jobsPerPage:
    #Daca numarul de joburi este intre 0 si 25, atunci luam decat pagina 1
    if jobs == 0:
        pageLink = 'https://d-career.org/Draexlmaier/go/DRÄXLMAIER-Job-Opportunities-in-Romania-%28Romanian%29/4196801/?q=&sortColumn=referencedate&sortDirection=desc'
    #Daca numarul de joburi este mai mare decat 25, atunci luam pagina corespunzatoare
    else:
        pageLink = f"https://d-career.org/Draexlmaier/go/DRÄXLMAIER-Job-Opportunities-in-Romania-%28Romanian%29/4196801/{jobs}/?q=&sortColumn=referencedate&sortDirection=desc"

    #Punem link-ul in url-ul scraper-ului
    scraper.url = pageLink

    #Cautam elementele care contin joburile si locatiile
    elements = rules.getTags("tr", {"class":"data-row"})

    #Pentru fiecare job, extragem titlul, link-ul, compania, tara si orasul
    for element in elements:
        id = str(uuid.uuid4())
        job_title = element.find("a", {"class":"jobTitle-link"}).text
        job_link = "https://d-career.org" + element.find("a", {"class":"jobTitle-link"})['href']
        city = element.find("span", {"class":"jobLocation"}).text.split(',')[0].replace('  ', '').replace('\n', '')
        if city == 'Codlea Brasov':
            city='Codlea'

        finaljobs.append({
            'id': id,
            'job_title': job_title,
            'job_link': job_link,
            'company': company.get('company'),
            'country': 'Romania',
            'city': city,
        })

#Afisam numarul de joburi
print(json.dumps(finaljobs, indent=4))

#Incarcam joburile in baza de date
loadingData(finaljobs, company.get("company"))