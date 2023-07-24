# Based Scraper Python

![Pe Viitor logo](https://peviitor.ro/static/media/peviitor_logo.df4cd2d4b04f25a93757bb59b397e656.svg)

## Descriere 

**scraper_peviitor** este o bibliotecă de scraping bazată pe Python, care se bazează pe bibliotecile de parsing HTML, Beautiful Soup și Requests. Acesta vă permite să extrageți datele necesare din paginile web și să le salvați într-un format ușor de utilizat, cum ar fi CSV sau JSON. Cu , **scraper_peviitor** puteți selecta elementele HTML specifice de pe o pagină web și puteți extrage informațiile necesare, cum ar fi textul, link-urile, imagini etc.

Caracteristicile cheie ale **scraper_peviitor** includ:
- Utilizează bibliotecile Python populare, BeautifulSoup și Requests, pentru a facilita scraping-ul web.
- Extrage datele necesare de pe o pagină web folosind selecții HTML specifice.
- Oferă o varietate de opțiuni de stocare pentru datele scrapate, inclusiv JSON.
- Este ușor de utilizat și integrat în proiectele Python existente.

**scraper_peviitor** este o opțiune excelentă pentru dezvoltatorii Python care caută o bibliotecă puternică și flexibilă de scraping. Cu **scraper_peviitor**, puteți automatiza procesul de extragere a datelor din paginile web, economisind timp și efort.

## Instalare

Pentru a instala biblioteca **scraper_peviitor**, urmați următorii pași:

- Clonați fișierul `git clone https://github.com/peviitor-ro/based_scraper_py.git`
- Navigați la directorul **based_scraper_py**. Rulați comanda `cd based_scraper_py` pentru a naviga la acest director.
- Creați mediu virtual de lucru.`python3 -m venv env`
- Activează mediu virtual de lucru. Rulați comanda `source env/bin/activate` pentru al activa.
- Rulați comanda `pip install -e .` pentru a instala **scraper_peviitor**.

## Exemple de utilizare 
1. Descărcarea conținutului de la un anumit URL:
    ```py
    scraper = Scraper('https://www.example.com')
    soup = scraper.getSoup()
    ```
    Aceste două linii de cod creează un obiect Scraper care are ca URL https://www.example.com, și apoi descarcă codul HTML de la acel URL folosind metoda  `getSoup()` și returnează un obiect BeautifulSoup care poate fi ulterior folosit pentru a căuta anumite elemente în cadrul paginii web.
    
    Pentru a extrage toate tag-urile "a" care conțin un atribut "href" care începe cu "https://":
    ```py
    rules = Rules(scraper)
    anchors = rules.getTags("a", {"href": lambda x: x and x.startswith("https://")})
    ```
    
    Pentru a extrage primul tag "h1" de pe pagină:
    ```py
    h1 = rules.getTag("h1")
    ```

2. Descărcarea conținutului JSON de la un anumit URL:
    ```py
    scraper = Scraper('https://api.example.com/data')
    data = scraper.getJson()
    ```
    Aceste două linii de cod creează un obiect Scraper care are ca URL https://api.example.com/data, și apoi descarcă conținutul de la acel URL folosind metoda `getJson()` și returnează un dicționar Python care conține datele JSON.
    
    Pentru a face un request POST către un API și a extrage răspunsul în format JSON:
    ```py
    scraper = Scraper()
    data = {"key1": "value1", "key2": "value2"}
    response_json = scraper.post("https://api.example.com", data=data)
    ```
3. Schimbarea URL-ului folosit de un obiect Scraper:
     ```py
    scraper = Scraper('https://www.example.com')
    scraper.url = 'https://www.example.com/about'
    soup = scraper.getSoup()
    ```

Pentru a vedea mai multe exemple, puteți verifica fișierele din folderul "sites". Acesta conține diverse pagini web pe care le puteți utiliza pentru a testa funcționalitatea clasei Scraper și a altor clase legate de web scraping. În aceste fișiere puteți găsi diverse exemple de atribute și taguri pe care le puteți utiliza în metodele din clasa Rules. De asemenea, puteți crea propriile exemple în aceste fișiere și să le utilizați pentru a experimenta și a îmbunătăți codul dvs.

## Contribuie
Dacă dorești să contribui la dezvoltarea scraperului, există mai multe modalități prin care poți face acest lucru. În primul rând, poți ajuta la dezvoltarea codului sursă prin adăugarea de noi funcționalități sau prin remedierea de probleme existente. În al doilea rând, poți contribui la îmbunătățirea documentației sau a traducerilor în alte limbi. În plus, dacă dorești să ajuți și nu ești sigur cum să începi, poți verifica lista noastră de probleme deschise și să ne întrebi cum poți ajuta. Pentru a obține mai multe informații, te rugăm să consulți secțiunea "Contribuie" din documentația noastră.

## Autori
 Echipa noastră este formată dintr-un grup de specialiști și entuziaști ai educației, care își doresc să aducă o contribuție semnificativă în acest domeniu. 

- [peviitor team](https://github.com/peviitor-ro)

Suntem dedicați îmbunătățirii și dezvoltării continue a acestui proiect, astfel încât să putem oferi cele mai bune resurse pentru toți cei interesați.
