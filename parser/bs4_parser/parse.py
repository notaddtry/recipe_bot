import argparse
import bs4
from datetime import datetime
from functools import reduce
import math
from multiprocessing import Pool
import pandas as pd
from pathlib import Path
import requests
from tqdm import tqdm
import os  


from const import n_workers, json_name, main_url


def get_soup(url):
    req = requests.get(url)
    return bs4.BeautifulSoup(req.text, 'lxml')


def get_recipe_urls_from_page(url):
    soup = get_soup(url)
    content_div = soup.find('div', 'content-md')
    pages_url = [recipe_preview.find('h2').find('a')['href']
                 for recipe_preview in content_div.find_all('article', 'item-bl')]
    return pages_url


def get_pages_range():
    url = f'{main_url}/~1/'
    soup = get_soup(url)

    recipe_count_div = soup.find('div', 'bl-right')
    recipe_count = int(recipe_count_div.find('strong').get_text())
    recipe_per_page_count = 15
    pages_count = math.ceil(recipe_count / recipe_per_page_count)

    pages_range = [f'{main_url}/~{i}/' for i in range(1, pages_count + 1)]
    return pages_range


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parser of recipes from povarenok.ru site')
    parser.add_argument(
        help='path for saving data',
        type=Path,
        required=True
    )
    args = parser.parse_args()
    print(f'Run with arguments: {args}')

    pages_range = get_pages_range()
  
    print("Let's find all recipe urls")
    with Pool(n_workers) as p:
        p = Pool(n_workers)
        maped_recipe_urls = tqdm(p.imap_unordered(get_recipe_urls_from_page, pages_range), total=len(pages_range))
        recipe_urls = reduce(lambda x, y: x + y, maped_recipe_urls)
        recipe_urls = set(recipe_urls)
        recipe_urls_df = pd.DataFrame(recipe_urls)

    outdir = args.save_path
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    fullname = os.path.join(outdir, json_name)
    recipe_urls_df.to_json(fullname, orient='values', index=False)

    print("Well done")