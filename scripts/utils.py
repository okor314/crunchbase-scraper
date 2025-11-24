from bs4 import BeautifulSoup

import csv
import json
import os
from typing import Dict, List, Any

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

def extract_competitors(soup: BeautifulSoup, base_url='') -> list[dict]:
    result = []
    for company in soup.select('div[class="row"]:has(a)'):
        result.append(
            {
                'competitor': company.find('a').text.strip(),
                'image': company.find('img').get('src'),
                'link': base_url + company.find('a').get('href'),
            }
        )
    return result


class TableWriter:
    """
    Writes JSON-like dictionaries into multiple CSV files,
    handling nested fields by splitting into separate tables.
    """
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        self.tables: Dict[str, Dict] = {}
        self.json_files: Dict[str, str] = {}

    def _ensure_table(self, table_name: str, fields: List[str]):
        """
        Create table entry if not exists.
        Initialize mode = 'w' and store fields.
        """
        if table_name not in self.tables:
            self.tables[table_name] = {
                "fields": fields,
                "filename": os.path.join(self.output_dir, f"{table_name}.csv"),
                "mode": "w",
            }

    def write_row(self, table_name: str, row: Dict[str, Any], parent_identifiers: Dict = dict()):
        """
        Write a single row into a table CSV.
        If first write → write header.
        If next writes → append without header.
        """
        # Connect with parent table if such provided
        row.update(parent_identifiers)

        # Ensure table definitions exist
        fields = list(row.keys())
        self._ensure_table(table_name, fields)

        meta = self.tables[table_name]

        with open(meta["filename"], meta["mode"], newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=meta["fields"])

            if meta["mode"] == "w":
                writer.writeheader()
                meta["mode"] = "a"  # switch to append mode

            writer.writerow(row)

    def write_nested(self, 
                    json_obj: Dict | List[Dict], 
                    table_name: str,
                    has_parent: bool = False,
                    primary_fields: List[str] = [],
                    parent_identifiers: Dict[str, Any] = dict()):
        """
        Splits nested dictionaries in separate CSV tables.
        """
        if isinstance(json_obj, dict):
            if not parent_identifiers: parent_identifiers = {key: json_obj.get(key) for key in primary_fields}
            row = {}
            for key, val in json_obj.items():
                if isinstance(val, list):
                    self.write_nested(val, table_name=key, has_parent=True, parent_identifiers=parent_identifiers)
                else:
                    row[key] = val
            if has_parent:
                self.write_row(table_name, row, parent_identifiers)
            else:
                self.write_row(table_name, row)
        elif isinstance(json_obj, list): 
            if not json_obj: 
                return # pass if epmty 
            for row in json_obj: 
                self.write_nested(row, table_name, has_parent, primary_fields, parent_identifiers)

    def write_json(self, json_obj: Dict, filename):
        file_mode = self.json_files.get(filename)
        file_path = os.path.join(self.output_dir, filename)
        if not file_mode:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4)
        
        self.json_files[filename] = 'a'
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        with open(file_path, 'w', encoding='utf-8') as f:
            data.append(json_obj)
            json.dump(data, f, indent=4)
        