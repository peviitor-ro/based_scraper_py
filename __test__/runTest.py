"""
Scraper Validation Test Script

This script validates scrapers by checking their output against required rules.

Validation Rules:
-----------------
1. Required keys (must be present with non-None values):
   - company: The company name
   - job_title: The job title
   - job_link: URL to the job posting

2. Optional keys (may be present):
   - city: City location(s) 
   - county: County location(s)
   - remote: Work arrangement options (must be a list)

3. Remote field validation (when present):
   - Must be a list (even if empty)
   - All values must be lowercase
   - Only allowed values: 'remote', 'on-site', 'hybrid'
   - Examples:
     * {"remote": ["remote"]}
     * {"remote": ["on-site", "hybrid"]}
     * {"remote": []}

4. All other keys are rejected.

The script runs all changed scraper files (in sites/ directory) and validates
their JSON output against these rules.
"""

import subprocess
import json
import re 
import os

process = subprocess.run(['git', 'remote', 'add','upstream', 'https://github.com/peviitor-ro/based_scraper_py.git'], capture_output=True)
process = subprocess.run(['git', 'fetch', 'upstream'], capture_output=True)
process = subprocess.run(['git', 'diff', '--name-only', 'upstream/main'], capture_output=True)
files = process.stdout.decode('utf-8').split('\n')
files = list(filter(None, files))

for file in files:
    print(f'Running {file} ...')
    if file.startswith('sites/'):
        directory = os.path.abspath(file).rsplit('/', 1)[0].replace('__test__/', '')
        file_name = file.rsplit('/', 1)[1]

        run_file = subprocess.run(["python3", directory + "/" + file_name], capture_output=True).stdout.decode('utf-8')

        pattern = re.compile(r"(\[.*\])", re.DOTALL)
        matches = pattern.findall(run_file)

        scraper_obj = json.loads(matches[0])

        # Define required and optional keys
        required_keys = ['company', 'job_title', 'job_link']
        optional_keys = ['city', 'county', 'remote', 'country']
        allowed_keys = required_keys + optional_keys
        
        # Define allowed remote values
        allowed_remote_values = ['remote', 'on-site', 'hybrid']

        for job in scraper_obj:
            # Check that all required keys are present
            for req_key in required_keys:
                if req_key not in job:
                    raise Exception(f"Required key '{req_key}' is missing! \n {job}")
            
            # Check each key in the job
            for key, value in job.items():
                # Reject keys that are not in the allowed list
                if key not in allowed_keys:
                    raise Exception(f"Key '{key}' is not allowed! Allowed keys are: {', '.join(allowed_keys)}")

                # Check that required keys have non-None values
                if key in required_keys and value == None:
                    raise Exception(f"Required key '{key}' has no value! \n {job}")
                
                # Validate remote field format
                if key == 'remote':
                    # Remote must be a list
                    if not isinstance(value, list):
                        raise Exception(f"Key 'remote' must be a list, got {type(value).__name__}! \n {job}")
                    
                    # Check each value in the remote list
                    for remote_val in value:
                        # Must be lowercase
                        if remote_val != remote_val.lower():
                            raise Exception(f"Remote value '{remote_val}' must be lowercase! \n {job}")
                        
                        # Must be in allowed values
                        if remote_val not in allowed_remote_values:
                            raise Exception(f"Remote value '{remote_val}' is not allowed! Allowed values are: {', '.join(allowed_remote_values)} \n {job}")
                
        print(f'✅ {file}')
    else:
        print(f'{file} is not a scraper file!')

