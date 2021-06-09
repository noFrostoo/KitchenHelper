import os
import re
from urllib.parse import urlparse

from recipe_scrapers import SCRAPERS, scrape_me

from kitchenhelper_server.api.schemas import Recipe
from .google_scraper import search

os.environ["RECIPE_SCRAPERS_SETTINGS"] = "recipe_scrapers.settings.v12_settings"

camel_case_regex = re.compile(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)')


def find_recipe(keywords: str):
    """
    Tries to find a recipe given the keywords (a space-separated string of words).
    Only URLs supported by the `recipe-scrapers` library are considered.

    :param keywords: Keywords describing the dish to search
    :return: a :py:class:Recipe object describing a found recipe or `None` if nothing was found
    """

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
