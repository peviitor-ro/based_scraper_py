from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)
from getCounty import get_county

url=''
company='UnicreditTiriac'
scraper=Scraper()
scraper.get_from_url(url)