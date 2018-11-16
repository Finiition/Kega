# USING PYTHON 3.7

import requests
from bs4 import BeautifulSoup

home = 'https://fr.openfoodfacts.org/'


def webcrawler(page):
    r = requests.get(page)
    c = r.content

    soup = BeautifulSoup(c, 'html.parser')

    product_list = soup.find('ul', class_="products")
    for product in product_list.findAll("li"):
        name = product.find("span").text
        print('Nom prodtuit : ' + name)

        lien_product = product.find("a").get("href")
        print('Lien produits : ' + home + lien_product)

        lien_image = product.find("img")
        print('Lien image : ',  lien_image['data-src'])

        print('####################')


webcrawler(home)
