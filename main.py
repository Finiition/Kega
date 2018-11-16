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
    return data


req = 'https://fr.openfoodfacts.org/produit/3045320104172/100-pur-jus-clementines-pressees-andros'


def getDetailProduit(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c, 'html.parser')
    # div = soup.find('div', {"class": "medium-12 large-8 xlarge-8 xxlarge-8 columns"})
    nova = soup.findAll('a', {"href": "/nova"})
    novaScore = 0

    for img in nova:
        imgNova = img.find('img')
        if imgNova is not None:
            if imgNova['alt'] == '1 - Aliments non transformés ou transformés minimalement':
                novaScore = 4
            if imgNova['alt'] == '2 - Ingrédients culinaires transformés':
                novaScore = 3
            if imgNova['alt'] == '3 - Aliments transformés':
                novaScore = 2
            if imgNova['alt'] == '4 -  Produits alimentaires et boissons  ultra-tran':
                novaScore = 1

    print(novaScore)


getDetailProduit(req)
webcrawler(home)
