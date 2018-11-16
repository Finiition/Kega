# USING PYTHON 3.7

import requests
from bs4 import BeautifulSoup

home = 'https://fr.openfoodfacts.org/'


def webcrawler(page):
    r = requests.get(page)
    c = r.content
    data = []
    soup = BeautifulSoup(c, 'html.parser')

    product_list = soup.find('ul', class_="products")
    for product in product_list.findAll("li"):
        name = product.find("span").text
        lien_product = product.find("a").get("href")
        lien_image = product.find("img")
        data.append({
            "name": name,
            "url_product": lien_product,
            "url_image": lien_image['data-src']
        })
    print(data)
    print(len(data))


webcrawler(home)
