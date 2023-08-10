import subprocess
import json
import re 

process = subprocess.run(['git', 'remote', 'add','upstream', 'https://github.com/peviitor-ro/based_scraper_py.git'], capture_output=True)
process = subprocess.run(['git', 'fetch', 'upstream'], capture_output=True)
process = subprocess.run(['git', 'diff', '--name-only', 'upstream/main'], capture_output=True)
files = process.stdout.decode('utf-8').split('\n')
files = list(filter(None, files))

for file in files:
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
    else:
        print(f'{file} is not a scraper file!')

