from bs4 import BeautifulSoup
import json

from utils import *
from functools import partial

BASE_URL = 'https://www.crunchbase.com/'

def parse_page(html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    test = soup.select_one('section[class="body"]:has(div[class~="product-container"])')
    test = test.select('div[class="product-container"]')
    print(len(test))

    # Get json with a lot of info
    json_data = json.loads(soup.select('structured-data script')[2].text)
    json_data = json_data.get('mainEntity')

    # Sorting links in dictionary
    links = {}
    for link in json_data.get('sameAs'):
        typical_domens = ['linkedin', 'facebook', 'twitter', 'x', 'instagram']
        domen = link.split('.')[1]
        if domen in typical_domens:
            links[domen] = link
        else:
            links['website'] = link

    # CSS selectors for parsing page
    seletors = {
        'email': 'blob-formatter span',
        'company_type': 'span[title~="Profit"]',
        'operative_status': 'div tile-field div:has(label-with-info:contains("Operating Status")) field-formatter span',
        'company_categories': 'chips-container',
        'headquarter_location': 'markup-block:contains("headquarters") field-formatter identifier-multi-formatter span',
        'products': 'section[class="body"]:has(div[class~="product-container"])'
    }

    # Functions to use on selected elements to extract data
    data_extractors = {
        'email': lambda x: x.text.strip(),
        'company_type': lambda x: x['title'].lower().replace(' ', '_'),
        'operative_status': lambda x: x['title'],
        'company_categories': lambda x: extract_categories(x, base_url=BASE_URL),
        'headquarter_location': lambda x: extract_location(x, base_url=BASE_URL),
        'products': lambda x: extract_products(x)
    }
    # Making funcs return default None if error occur
    data_extractors = {k: partial(errorCatcher, v, lambda _: None) for k, v in data_extractors.items()}

    # Selecting html-elements with data
    data_containers = {k: soup.select_one(selector) for k, selector in seletors.items()}
    # Extracting data from them
    parsed_data = {k:extr(data_containers[k]) for k, extr in data_extractors.items()}
    return {
        'company_name': json_data.get('name'),
        'company_description': json_data.get('description'),
        'website': links.get('website'),
        'email': parsed_data.get('email'),
        'linkedin': links.get('linkedin'),
        'facebook': links.get('facebook'),
        'twitter': links.get('twitter'),
        'company_type': parsed_data.get('company_type'),
        'operative_status': parsed_data.get('operative_status'),
        'company_categories': parsed_data.get('company_categories'),
        'headquarter_location': parsed_data.get('headquarter_location'),
        'founders': json_data.get('founder'),
        'products': parsed_data.get('products'),
    }

if __name__ == '__main__':
    with open('./html_examples/example1.txt', 'r', encoding='utf-8') as f:
        html = f.read()
    result = parse_page(html)
    print(result)
