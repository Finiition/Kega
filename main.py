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
        lien = home + lien_product
        print('Lien produits : ' + lien)

        lien_image = product.find("img")
        print('Lien image : ',  lien_image['data-src'])

        getDetailProduit(lien)

        print('####################')


def getDetailProduit(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c, 'html.parser')
    #div = soup.find('div', {"class": "medium-12 large-8 xlarge-8 xxlarge-8 columns"})
    nova = soup.findAll('a', {"href": "/nova"})

    for img in nova:
        imgNova = img.find('img')
        if imgNova is not None:
            print('Nova score : ' + imgNova['alt'])


webcrawler(home)
