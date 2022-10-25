# Amazon Spider Scraper using Selectorlib 

A simple amazon scraper to extract product details and prices from Amazon.com using Python Requests and **[Selectorlib](https://selectorlib.readthedocs.io/en/latest/)**. 

Full article at [ScrapeHero Tutorials](https://www.scrapehero.com/tutorial-how-to-scrape-amazon-product-details-using-python-and-selectorlib/)

There are three simple scrapers in this project. 
* Product Detail Page Scraper: `bin/product_detail.py`
* Product Detail Page Spider Scraper: `bin/product_detail_spider.py`
* Product Reviews Page Scraper: `bin/product_reviews.py`
* Product Reviews Page Spider Scraper: `bin/product_reviews_spider.py`
* Search Results Page Scraper: `bin/product_search_results.py`

## Requisites

* [anaconda](https://www.anaconda.com/products/individual) / [miniconda](https://docs.conda.io/en/latest/miniconda.html)

## Setup

**Step 1**: Clone repo.

```bash
$ git clone https://github.com/adrianmarino/amazon-scraper.git
$ cd amazon-scraper
```

**Step 2**: Create environment.

```bash
$ cd amazon-scraper
$ conda env create -f environment.yml
```

## Usage

**Step 1**: Enable project environment.

```bash
$ conda activate amazon-scraper
```

**Step 2:** Configure fields to scrap into config files:

* `config/product_detail_selectors.yml`: Map ccs/xpath selectors to json fields for product details scrapping.
* `config/product_detail_urls`: Urls used by `bin/product_detail.py` scrapper.
* `config/product_reviews_selectors.yml`: Map ccs/xpath selectors to json fields for product reviews scrapping.
* `config/product_reviews_urls`: Urls used by `bin/product_reviews.py` scrapper.
* `config/product_search_results_selectors.yml`: Map ccs/xpath selectors to json fields for product search result scrapping.
* `config/product_search_results_urls`: Urls used by `bin/product_detail.py` and `bin/product_detail_spider.py` scrapper.

**Notes**
* `bin/product_detail_spider.py` get urls specified into `config/product_search_results_urls` and use both `config/product_search_results_selectors.yml` and 
`config/product_detail_selectors.yml` to scrap product details. The result is a file by product in `output` path.
* `bin/product_reviews_spider.py` get urls specified into `output/[PRODUCT_ID | PRODUCT_ID_varaint_PRODUCT_ID.json]` files and use `config/product_reviews_selectors.yml` to scrap product reviews. The result is a file by product in `output` path.

**Step 3:** From terminal execute any of next commands:

```bash
$ bin/product_detail.py
```

```bash
$ bin/product_reviews.py
```

```bash
$ bin/product_search_results.py
```

```bash
$ bin/product_detail_spider.py
```

```bash
$ bin/product_reviews_spider.py
```
**Notes**
* `bin/product_reviews_spider.py` required run `bin/product_detail_spider.py` first.
* `bin/product_reviews_spider.py` generate product review files from `bin/product_detail_spider.py` result files.  

**Step 4:** Scrapped data is downloaded into `output` directory. One file by product details and one file by search results. 


## Proxies

* Proxies lists:
  * [free-proxy-list](https://free-proxy-list.net/)
  * [hidemy.name](https://hidemy.name/es/proxy-list/)
* Setup proxies under `src/scrapper/scrapper_factory.py`
