import os 
import subprocess

exclude = ['__init__.py','main.py' , 'enel.py', 'kaufland.py', 'decathlon.py']
print(os.environ.get("apikey"))
path = os.path.dirname(os.path.abspath(__file__))

for site in os.listdir(path):
    if site.endswith('.py') and site not in exclude:
        print(f'Executing {site}...')
        print("=====================================")
        subprocess.run(['python', os.path.join(path, site)])
        print("=====================================")
        print(f'Finished executing {site}.')
        
