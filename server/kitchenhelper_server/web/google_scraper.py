from lxml import etree
import requests

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'


def search(term: str, results: int = 10, lang: str = 'en'):
    """
    Search Google for the given term and return a list of resulting URLs.

    :param str term: Term to search
    :param int results: How many results to return
    :param str lang: Language in which to search
    :return: List of resulting URLs
    :rtype: list
    """

    response = requests.get(
        f"https://www.google.com/search?q={term.replace(' ', '+')}&num={results}&hl={lang}",
        headers={'User-Agent': user_agent},
        stream=True
    )
    response.raise_for_status()
    response.raw.decode_content = True

    parser = etree.HTMLParser()
    doc = etree.parse(response.raw, parser)
    urls = []

    for div in doc.getroot().xpath("//div[@class='g']"):
        urls.append(div.xpath('.//a')[0].get('href'))
    
    return urls
