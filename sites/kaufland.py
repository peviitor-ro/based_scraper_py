from scraper_peviitor import Scraper, Rules
import time
import urllib.parse
import json

scraper = Scraper('https://jobs.kaufland.com/Romania/search/?q=&locationsearch=&locale=ro_RO')
rules = Rules(scraper)

pages = rules.getTags("a", {'rel': 'nofollow'})
pagesLink = "https://jobs.kaufland.com/Romania/search/"

j = []
jobsLink = "https://jobs.kaufland.com"

step = 15
queryStringNumbers = [*range(0, int(rules.getXpath('//*[@id="content"]/div/div[3]/div/div/div/span[1]/b[2]')[0].text), step)]

lst = list(pages)[0]['href'].split('=')
links = []
for i in queryStringNumbers:
    lst[-1] = str(i)
    links.append(pagesLink + '='.join(lst))

for page in links:
    scraper.url = page
    rules = Rules(scraper)
    jobs = rules.getTags('a', {'class': 'jobTitle-link'})
    a = rules.getTags("a", {'rel': 'nofollow'})
    pages.update(a)
    j.extend(map(lambda x: jobsLink + urllib.parse.unquote(x['href']), jobs))
    time.sleep(3)

finalJobs = dict()
idx = 0

for job in j:
    print(job)
    scraper.url = job
    rules = Rules(scraper)
    title = rules.getTag('title').text
    location = "Romania"
    finalJobs[idx] = {'title': title, 'location': location, 'link': job}
    idx += 1
    time.sleep(3)

with open('kaufland.json', 'w') as f:
    json.dump(finalJobs, f)

