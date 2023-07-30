import subprocess
import json
import re 

hash =  subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True).stdout.decode('utf-8').strip()
commit = subprocess.run(["git", "show", hash], capture_output=True).stdout.decode('utf-8')
pattern = re.compile(r"(\+\+\+ b/sites/.*?\.py)", re.DOTALL)

try:
    file = pattern.findall(commit)[0].split('+++ b/')[1]
except:
    file = ''

if file.startswith('sites/'):
    run_file = subprocess.run(["python3", file], capture_output=True).stdout.decode('utf-8')

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

    print(f'✅ {file}')
else:
    print(f'{file} is not a scraper file!')