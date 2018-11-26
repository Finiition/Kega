# USING PYTHON 3.7

import requests
from bs4 import BeautifulSoup
from flask import Flask,render_template

home = 'https://fr.openfoodfacts.org/'

app = Flask(__name__)
produits = []
details = []


def webcrawler(page):
    r = requests.get(page)
    c = r.content
    soup = BeautifulSoup(c, 'html.parser')
    global produits;
    bio = soup.find('a', {"href": "/label/bio"})
    #Liste des produits
    product_list = soup.find('ul', class_="products")
    i = 0
    #Création de l'objet contenant les informations du produit.

    if bio is None:
        bio_number = 0
    else:
        bio_number = 1

    for product in product_list.findAll("li"):
        name = product.find("span").text
        lien_product = product.find("a").get("href")
        lien = home + lien_product
        getProductInfos(lien)
        lien_image = details[i]["imgProduct"]
        nutriscoreText =details[i]["nutriscoreText"]
        nova = details[i]["novaText"]
        if("4" in str(nova)):
            nova_number = 1
        elif("3" in str(nova)):
            nova_number = 2
        elif("2" in str(nova)):
            nova_number = 3
        elif("1" in str(nova)):
            nova_number = 4
        if("A" in str(nutriscoreText)):
            nutri_number = 5
        elif("B" in str(nutriscoreText)):
            nutri_number = 4
        elif("C" in str(nutriscoreText)):
            nutri_number = 3
        elif("D" in str(nutriscoreText)):
            nutri_number = 2
        elif("E" in str(nutriscoreText)):
            nutri_number = 1

        score = getScore(nova_number, nutri_number, bio_number)

        if score < 26:
            color = 'red'
        elif score >= 26 & score < 51:
            color = 'orange'
        elif score >= 51 & score <76:
            color = 'yellow'
        elif score > 75:
            color = 'green'
        produits.append({
            "name":name,
            "url_product":lien_product,
            "lien_image":lien_image,
            "nova": nova,
            "score": score,
            "color": color,
        })
        i = i+1

def getProductInfos(url):
    r = requests.get(url)
    c = r.content
    global details;
    soup = BeautifulSoup(c, 'html.parser')
    nova = soup.findAll('a', {"href": "/nova"})
    nutriscore = soup.findAll('a', {"href": "/nutriscore"})
    imgProduct = soup.find('img',{"id":"og_image"})["data-src"]

    for img in nova:
        imgNova = img.find('img')
        if imgNova is not None:
            finalNova = imgNova['alt'];

    for img in nutriscore:
        imgNutriscore = img.find('img')
        if imgNutriscore is not None:
            final_nutriscore_alt = imgNutriscore["alt"];

            details.append({
                "novaText": finalNova,
                "imgProduct": imgProduct,
                "nutriscoreText": final_nutriscore_alt
            })

def getScore(novascore, nutriscore, bioscore):
    score = ((0.6 * nutriscore) + (0.3 * novascore) + (0.1 * bioscore))
    return score


webcrawler(home)


@app.route("/")
def main():
    return render_template('produits.html', produits=produits)


if __name__ == '__main__':
    app.run(host='localhost', port=4000)
