from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs
import json
import html
import re

url = "https://www.synevo.ro/cariere/"
scraper = Scraper()
scraper.get_from_url(url)

company = {"company": "Synevo"}
finaljobs = list()

content = scraper.markup.text if hasattr(scraper.markup, 'text') else str(scraper.markup)

idx = content.find('careers:')
if idx >= 0:
    start = content.find('[', idx)
    depth = 0
    for i, ch in enumerate(content[start:], start):
        if ch == '[':
            depth += 1
        elif ch == ']':
            depth -= 1
            if depth == 0:
                end = i
                break
    else:
        end = -1
    if end >= start:
        data = html.unescape(content[start:end + 1])
        try:
            jobs_data = json.loads(data)
            for cat in jobs_data:
                sub = cat.get("sub_jobs")
                if isinstance(sub, dict):
                    for k, v in sub.items():
                        job_title = v.get("job_name", "").strip()
                        slug = v.get("slug", "")
                        if job_title and slug:
                            finaljobs.append(
                                {
                                    "job_title": job_title,
                                    "job_link": "https://www.synevo.ro/cariere/" + slug + "/",
                                    "company": company.get("company"),
                                    "country": "Romania",
                                }
                            )
                elif isinstance(sub, list):
                    for v in sub:
                        job_title = v.get("job_name", "").strip()
                        slug = v.get("slug", "")
                        if job_title and slug:
                            finaljobs.append(
                                {
                                    "job_title": job_title,
                                    "job_link": "https://www.synevo.ro/cariere/" + slug + "/",
                                    "company": company.get("company"),
                                    "country": "Romania",
                                }
                            )
        except Exception as e:
            pass

publish_or_update(finaljobs)

logourl = "https://www.synevo.ro/wp-content/themes/synevo-sage/dist/images/synevo-logo_6edc429f.svg"
publish_logo(company.get("company"), logourl)

show_jobs(finaljobs)
