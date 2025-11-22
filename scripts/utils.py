from bs4 import BeautifulSoup

def errorCatcher(func, heandler, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return heandler(e)
    
def extract_categories(soup: BeautifulSoup, base_url='') -> list[dict]:
    return [
        {
            'category': a.find('chip').text.strip(),
            'category_link': base_url + a.get('href')
        }
        for a in soup.find_all('a')
    ]

def extract_location(soup: BeautifulSoup, base_url='') -> list[dict]:
    result = []
    for a, location_type in zip(soup.find_all('a'), ['city', 'region', 'country']):
        result.append({
            'location_name': a.get('title'),
            'location_link': base_url + a.get('href'),
            'location_type': location_type
        })

    return result

def extract_products(soup: BeautifulSoup) -> list[dict]:
    return [
        {
            'name': prod.select_one('div[class="product-name"]').text.strip(),
            'description': prod.select_one('div[class="product-description"]').text.strip()
        }
        for prod in soup.select('div[class~="product-container"]')
    ]
    