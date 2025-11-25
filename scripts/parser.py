from bs4 import BeautifulSoup
import json

from utils import *
from functools import partial

BASE_URL = 'https://www.crunchbase.com'

def parse_page(html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')

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
        'email':                'label-with-info:contains("Email") + field-formatter',
        'company_type':         'span[title~="Profit"]',
        'operative_status':     'div tile-field div:has(label-with-info:contains("Operating Status")) field-formatter span',
        'company_categories':   'chips-container',
        'headquarter_location': 'markup-block:contains("headquarters") field-formatter identifier-multi-formatter span',
        'products':             'section[class="body"]:has(div[class~="product-container"])',
        'num_investors':        'markup-block:contains("investors") field-formatter a[href*="num_investors"]',
        'similar_companies':    'signal-similar-companies-upsell',
        'num_funding_rounds':   'label-with-info:contains("Number of Funding Rounds") + field-formatter a',
        'last_funding_type':    'a[href*="last_funding_type"]',
    }

    # Functions to use on selected elements to extract data
    data_extractors = {
        'email': lambda x: x.text.strip(),
        'company_type': lambda x: x['title'].lower().replace(' ', '_'),
        'operative_status': lambda x: x['title'],
        'company_categories': lambda x: extract_categories(x, base_url=BASE_URL),
        'headquarter_location': lambda x: extract_location(x, base_url=BASE_URL),
        'products': lambda x: extract_products(x),
        'num_investors': lambda x: int(x.text.strip()),
        'similar_companies': lambda x: extract_competitors(x, base_url=BASE_URL),
        'num_funding_rounds': lambda x: int(x.text.strip()),
        'last_funding_type': lambda x: x.text.lower().replace(' ', '_'),
    }
    # Making funcs return default None if error occur
    data_extractors = {k: partial(errorCatcher,
                                  v, 
                                  lambda _: None if k not in ['company_categories', 'headquarter_location', 'products', 'investors', 'similar_companies'] else []) 
                       for k, v in data_extractors.items()}

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
        'num_investors': parsed_data.get('num_investors'),
        'investors': json_data.get('funder'),
        'similar_companies': parsed_data.get('similar_companies'),
        'num_funding_rounds': parsed_data.get('num_funding_rounds'),
        'last_funding_type': parsed_data.get('last_funding_type'),
        'employees': json_data.get('employee')
    }

if __name__ == '__main__':
    writer = TableWriter(output_dir='../output')

    for filename in os.listdir('../html_examples'):
        with open(f'../html_examples/{filename}', 'r', encoding='utf-8') as f:
            html = f.read()
        result = parse_page(html)
        writer.write_nested(result, 'companies', primary_fields=['company_name'])
        writer.write_json(result, 'companies.json')
