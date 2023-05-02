import os 
import subprocess

exclude = ['__init__.py','main.py' , 'kaufland.py', "tesla.py"]
path = os.path.dirname(os.path.abspath(__file__))

for site in os.listdir(path):
    if site.endswith('.py') and site not in exclude:
        # action = subprocess.run(['python', os.path.join(path, site)], capture_output=True)   
        action = subprocess.run(['python', os.path.join(path, "auchan.py")])
        if action.returncode != 0:
            errors = action.stderr.decode('utf-8')
            print("Error in " + site)
            print(errors)
        else:
            print("Success scraping " + site)
            print(action.stdout.decode('utf-8'))
    break


        
