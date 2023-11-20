import os 
import subprocess
import requests

exclude = ['__init__.py','main.py' , 'kaufland.py', "tesla.py", "kellanova.py"]
path = os.path.dirname(os.path.abspath(__file__))
resolveApi = "https://dev.laurentiumarian.ro/scraper/based_scraper_py/"

for site in os.listdir(path):
    if site.endswith('.py') and site not in exclude:
        action = subprocess.run(['python', os.path.join(path, site)], capture_output=True)   
        if action.returncode != 0:
            errors = action.stderr.decode('utf-8')
            print("Error in " + site)
            print("Sending trigger to API ...")
            try:
                r = requests.post(resolveApi, data = {"file": site})
                response = r.json()
                if response.get("succes"):
                    print("Success Scraping " + site + " after trigger")
                else:
                    print("Both scraping and trigger failed")
                    print("Error:")
                    for error in response.get("error"):
                        print(error)
            except Exception as e:
                print("Error sending trigger to API")
                print("Error:")
                print(e)
                print("Error in " + site)
        else:
            print("Success scraping " + site)



        
