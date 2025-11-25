# Crunchbase Scraper

A lightweight, modular, pure-Python web scraping tool designed for parsing Crunchbase organization pages.

All data extraction is performed with:
- **aiohttp** for HTTP client logic  
- **BeautifulSoup** for HTML parsing  
- **Incremental CSV writer** that flattens nested JSON into separate tables  

⚠️ **Important:**  
Due to Cloudflare protection on the live website, `scraper.py` **cannot fetch real Crunchbase pages** through normal HTTP requests.  
However, the **parser and data extraction pipeline are fully functional** and tested using manually downloaded HTML examples stored in `html_examples/`.

---

## Installation

```bash
git clone https://github.com/okor314/crunchbase-scraper
cd crunchbase-scraper
pip install -r requirements.txt
```

## Testing the Parser (Recommended)
Since Cloudflare blocks automated requests, you can test the parser on local examples:

```bash
cd scripts
python parser.py
```
## What Data Does It Collect?

| Field Name                                          | Data Structure               | Description                                                                                                                   |
| --------------------------------------------------- | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Company Name**                                    | String                       | Company's primary name (extracted from other fields)                                                                          |
| **Company Description**                             | String                       | Brief description of the company and what it does                                                                             |
| **Website**                                         | String (URL)                 | Company's primary website address                                                                                             |
| **Contact Email**                                   | String                       | Company's publicly listed contact email address                                                                               |
| **LinkedIn URL**                                    | String (URL)                 | Link to the company's LinkedIn profile                                                                                        |
| **Twitter URL**                                     | String (URL)                 | Link to the company's Twitter profile                                                                                         |
| **Facebook URL**                                    | String (URL)                 | Link to the company's Facebook page                                                                                           |
| **Company Type**                                    | String                       | Legal structure of the company (e.g., "for_profit", "non_profit")                                                             |
| **Operating Status**                                | String                       | Current operational status of the company (e.g., "active", "acquired")                                                        |
| **Company Categories**                              | List of Objects              | Industry categories associated with the company. Each object contains:                                                        |
| &nbsp;&nbsp;&nbsp;&nbsp;Category Name               | String                       | Name of the category (e.g., "Artificial Intelligence (AI)", "Software")                                                       |
| &nbsp;&nbsp;&nbsp;&nbsp;Category Link               | String (URL)                 | Link to a Crunchbase search for that category                                                                                 |
| **Headquarter Location**                            | List of Objects              | More specific details about the company's headquarters location. Each object contains:                                        |
| &nbsp;&nbsp;&nbsp;&nbsp;Location Name               | String                       | Name of the city, region, country, or continent                                                                               |
| &nbsp;&nbsp;&nbsp;&nbsp;Location Link               | String (URL)                 | Link to a Crunchbase search for companies in that location                                                                    |
| &nbsp;&nbsp;&nbsp;&nbsp;Location Type               | String                       | Type of location (e.g., "city", "country")                                                                                    |
| **Founders**                                        | List of Objects              | Information about the company's founders. Each object contains:                                                               |
| &nbsp;&nbsp;&nbsp;&nbsp;Founder Name                | String                       | Name of the founder                                                                                                           |
| &nbsp;&nbsp;&nbsp;&nbsp;Founder Link                | String (URL)                 | Link to the founder's Crunchbase profile                                                                                      |
| &nbsp;&nbsp;&nbsp;&nbsp;Founder Image               | String (URL)                 | Link to the founder's image                                                                                                   |
| **Products**                                        | List of Objects              | Products or services offered by the company. Each object contains:                                                            |
| &nbsp;&nbsp;&nbsp;&nbsp;Product Name                | String                       | Name of the product or service                                                                                                |
| &nbsp;&nbsp;&nbsp;&nbsp;Product Description         | String                       | Brief description of the product or service                                                                                   |
| **Number of Investors**                             | Number                       | Total number of investors who have funded the company                                                                         |
| **Investors**                                       | List of Objects              | Details about each investor. Each object contains:                                                                            |
| &nbsp;&nbsp;&nbsp;&nbsp;Lead Investor?              | Boolean (true/false or null) | Indicates if the investor led a particular funding round                                                                      |
| &nbsp;&nbsp;&nbsp;&nbsp;Investment Title            | String                       | Short description of the investment (e.g., "[Investor Name] investment in [Funding Round]")                                   |
| &nbsp;&nbsp;&nbsp;&nbsp;Investment Link             | String (URL)                 | Link to the Crunchbase page with investment details                                                                           |
| &nbsp;&nbsp;&nbsp;&nbsp;Partners Involved           | List of Objects              | Names and links to Crunchbase profiles of individuals from the investment firm involved in the deal                           |
| &nbsp;&nbsp;&nbsp;&nbsp;Funding Round Title         | String                       | Title of the funding round in which the investment was made                                                                   |
| &nbsp;&nbsp;&nbsp;&nbsp;Funding Round Link          | String (URL)                 | Link to the Crunchbase page for that funding round                                                                            |
| &nbsp;&nbsp;&nbsp;&nbsp;Investor Name               | String                       | Name of the investing organization or individual                                                                              |
| &nbsp;&nbsp;&nbsp;&nbsp;Investor Image              | String (URL)                 | Link to the investor's logo or image                                                                                          |
| &nbsp;&nbsp;&nbsp;&nbsp;Investor Link               | String (URL)                 | Link to the Crunchbase profile of the investor                                                                                |
| **Similar Companies**                               | List of Objects              | List of companies deemed similar by Crunchbase. Each object contains:                                                         |
| &nbsp;&nbsp;&nbsp;&nbsp;Company Name                | String                       | Name of the similar organization                                                                                              |
| &nbsp;&nbsp;&nbsp;&nbsp;Company Image               | String (URL)                 | Link to the company's logo                                                                                                    |
| &nbsp;&nbsp;&nbsp;&nbsp;Company Link                | String (URL)                 | Link to the company's Crunchbase profile                                                                                      |
| **Number of Funding Rounds**                        | Number                       | Total number of funding rounds the company has gone through                                                                   |
| **Last Funding Type**                               | String                       | Type of the most recent funding round (e.g., "seed", "series_a")                                                              |
| **Current Employees (Featured)**                    | List of Objects              | Information about key employees. Each object contains:                                                                        |
| &nbsp;&nbsp;&nbsp;&nbsp;Employee Name               | String                       | Name of the employee                                                                                                          |
| &nbsp;&nbsp;&nbsp;&nbsp;Employee Link               | String (URL)                 | Link to the employee's Crunchbase profile                                                                                     |
| &nbsp;&nbsp;&nbsp;&nbsp;Employee Image              | String (URL)                 | Link to the employee's image                                                                                                  |
| &nbsp;&nbsp;&nbsp;&nbsp;Job Title                   | String                       | Employee's job title at the company                                                                                           |
| &nbsp;&nbsp;&nbsp;&nbsp;Job Link                    | String (URL)                 | Link to the employee's job on Crunchbase                                                                                      |
| &nbsp;&nbsp;&nbsp;&nbsp;Start Date                  | Date                         | Approximate date the employee started in this role                                                                            |
| &nbsp;&nbsp;&nbsp;&nbsp;Start Date Precision        | String                       | Level of precision for the start date                                                                                         |
