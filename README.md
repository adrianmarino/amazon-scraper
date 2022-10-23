# Amazon Scraper using Selectorlib 

A simple amazon scraper to extract product details and prices from Amazon.com using Python Requests and Selectorlib. 

Full article at [ScrapeHero Tutorials](https://www.scrapehero.com/tutorial-how-to-scrape-amazon-product-details-using-python-and-selectorlib/)

There are three simple scrapers in this project. 
1. Amazon Product Detail Page Scraper `bin/product_detail.py`
1. Amazon Search Results Page Scraper `bin/search_result.py`
1. Amazon Product Detail Page spider Scraper `bin/product_search_result_scrapper.py`

Note: A completely web browser based commercial version of these scrapers are available in [ScrapeHero Marketplace](https://www.scrapehero.com/marketplace/)

## Usage

**Step 1:**: Configure fiels to scrap into config files:

* `config/product_detail_selectors.yml`: Map ccs/xpath selectors to json fields for product details scrapping.
* `config/product_detail_urls`: Urls used by `bin/product_detail.py` scrapper.
* `config/search_results_selectors.yml`: Map ccs/xpath selectors to json fields for product search result scrapping.
* `config/search_results_urls`: Urls used by `bin/product_detail.py` and `bin/search_product_detail.py` scrapper.

**Note**: `bin/search_product_detail.py` get urls specified into `config/search_results_urls` and use both `config/search_results_selectors.yml` and 
`config/product_detail_selectors.yml` to scrap product details. The result is a file by product in `output` path.

**Step 2:** From terminal execute any of next commands:

```bash
$ bin/product_detail.py
```

```bash
$ bin/search_result.py
```

```bash
$ bin/product_search_result_scrapper.py
```

**Step 3:**: Scrapped data is downloaded into `output` directory. One file by product details and one file by search results. 
