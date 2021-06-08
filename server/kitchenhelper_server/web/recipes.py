import os
import re
from urllib.parse import urlparse

from recipe_scrapers import SCRAPERS, scrape_me

from kitchenhelper_server.api.schemas import Recipe
from .google_scraper import search

os.environ["RECIPE_SCRAPERS_SETTINGS"] = "recipe_scrapers.settings.v12_settings"

camel_case_regex = re.compile(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)')


def find_recipe(keywords: str):
    for url in search(keywords + " recipe"):
        if any(urlparse(url).netloc.endswith(k) for k in SCRAPERS.keys()):
            scraper = scrape_me(url)
            nutrients = {}

            for nutr, value in scraper.nutrients().items():
                name = ' '.join(camel_case_regex.findall(nutr))
                nutrients[name[0].upper() + name[1:].lower()] = value

            return Recipe(
                url=url,
                title=scraper.title(),
                total_time=scraper.total_time(),
                yields=scraper.yields(),
                ingredients=scraper.ingredients(),
                instructions=scraper.instructions(),
                nutrients=nutrients,
                image=scraper.image()
            )
    
    return None
