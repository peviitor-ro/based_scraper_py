import os 
import subprocess

exclude = [
    "__init__.py",
    "main.py",
    "cat.py",
    "cososys.py",
    "nshift.py",
    "stratpharma.py",
    "uipath.py",
    "uplift.py",
]
path = os.path.dirname(os.path.abspath(__file__))

for site in os.listdir(path):
    if site.endswith('.py') and site not in exclude:
        action = subprocess.run(['python', os.path.join(path, site)], capture_output=True)   
        if action.returncode != 0:
            print("Error scraping " + site)
            print(action.stderr.decode("utf-8"))
        else:
            print("Success scraping " + site)
