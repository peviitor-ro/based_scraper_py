import subprocess
import json
import re 

commit =  subprocess.run(["git", "log", "--name-status", "HEAD^..HEAD"], capture_output=True).stdout.decode('utf-8').split('M\t')[1].strip()

if commit.startswith('sites/'):
    run_file = subprocess.run(["python3", commit], capture_output=True).stdout.decode('utf-8')

    pattern = re.compile(r"(\[.*?\])", re.DOTALL)
    matches = pattern.findall(run_file)

    scraper_obj = json.loads(matches[0])

    keys = ['id', 'job_title', 'job_link', 'city', 'country', 'company']

    for job in scraper_obj:
        for key, value in job.items():
            if key not in keys:
                raise Exception(f"Key {key} is not allowed!")
            
            if value == None:
                raise Exception(f"Key {key} has no value! \n {job}")
