from urllib.parse import urlparse

from recipe_scrapers import SCRAPERS, scrape_me

from kitchenhelper_server.api.schemas import Recipe
from .google_scraper import search


def find_recipe(keywords: str):
    for url in search(keywords + " recipe"):
        if any(urlparse(url).netloc.endswith(k) for k in SCRAPERS.keys()):
            scraper = scrape_me(url)
            return Recipe(
                keywords=' '.join(sorted(keywords.split(' '))),
                title=scraper.title(),
                total_time=scraper.total_time(),
                yields=scraper.yields(),
                ingredients=scraper.ingredients(),
                instructions=scraper.instructions(),
                nutrients=scraper.nutrients(),
                image=scraper.image()
            )
    
    return None
