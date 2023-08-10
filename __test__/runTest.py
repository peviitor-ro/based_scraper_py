import subprocess
import json
import re 
import os
import requests
from sites.main import exclude, path, resolveApi

# response = requests.get(resolveApi)
# files = [file for file in response.json()[1].values() if file not in exclude]

# new_files = []
# for file in os.listdir(path):
#     if file not in files and file not in exclude:
#         new_files.append(file)

# if len(new_files) > 0:
#     for file in new_files:
#         run_file = subprocess.run(["python3", path + '/' + file], capture_output=True).stdout.decode('utf-8')

#         pattern = re.compile(r"(\[.*?\])", re.DOTALL)
#         matches = pattern.findall(run_file)

#         scraper_obj = json.loads(matches[0])

#         keys = ['id', 'job_title', 'job_link', 'city', 'country', 'company']

#         for job in scraper_obj:
#             for key, value in job.items():
#                 if key not in keys:
#                     raise Exception(f"Key {key} is not allowed!")
                
#                 if value == None:
#                     raise Exception(f"Key {key} has no value! \n {job}")

#         print(f'✅ {file}')
# else:
process = subprocess.run(['git', 'remote', 'upstream', 'https://github.com/peviitor-ro/based_scraper_py.git'], capture_output=True)
process = subprocess.run(['git', 'diff', '--name-only'], capture_output=True)
files = process.stdout.decode('utf-8').split('\n')
files = list(filter(None, files))

print(f'🔴 {files}')
