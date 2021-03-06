# USING PYTHON 3.7

import requests
import json
from bs4 import BeautifulSoup
from flask import Flask, render_template
import re

home = 'https://fr.openfoodfacts.org/'

numpage = 1
page_number = 1
app = Flask(__name__)
produits = []
details = []


def webcrawler(page):
    r = requests.get(page)
    c = r.content
    soup = BeautifulSoup(c, 'html.parser')
    nutri_number = 0
    nova_number = 0
    lien_image = ""
    nova = ""
    nutriscoreText = ""
    global numpage
    global produits
    global details
    global page_number
    bio = soup.find('a', {"href": "/label/bio"})
    # Liste des produits
    product_list = soup.find('ul', class_="products")
    # Création de l'objet contenant les informations du produit.

    if bio is None:
        bio_number = 0
    else:
        bio_number = 1

    for product in product_list.findAll("li"):
        name = product.find("span").text
        lien_product = product.find("a").get("href")
        lien = home + lien_product
        getProductInfos(lien)
        for data in details:
            lien_image = data["imgProduct"]
            nutriscoreText = data["nutriscoreText"]
            nova = data["novaText"]
        if ("4" in str(nova)):
            nova_number = 1 / 4
        elif ("3" in str(nova)):
            nova_number = 2 / 4
        elif ("2" in str(nova)):
            nova_number = 3 / 4
        elif ("1" in str(nova)):
            nova_number = 4 / 4
        if ("A" in str(nutriscoreText)):
            nutri_number = 5 / 5
        elif ("B" in str(nutriscoreText)):
            nutri_number = 4 / 5
        elif ("C" in str(nutriscoreText)):
            nutri_number = 3 / 5
        elif ("D" in str(nutriscoreText)):
            nutri_number = 2 / 5
        elif ("E" in str(nutriscoreText)):
            nutri_number = 1 / 5

        score = int(float(getScore(nova_number, nutri_number, bio_number)))
        if water(lien):
            score = 100
        elif alcool(lien):
            score = 0

        if score < 26:
            color = 'red'
        elif score >= 26 and score < 51:
            color = 'orange'
        elif score >= 51 and score < 76:
            color = 'yellow'
        elif score > 75:
            color = '#b6e945'
        produits.append({
            "name": name,
            "url_product": lien_product,
            "lien_image": lien_image,
            "nova": nova,
            "score": score,
            "color": color,
            "nutriscoreText": nutriscoreText,
        })
        print(name)
        jsonResult = open("result.json","w")

        produitsParse = str(produits)
        # print(produitsParse)
        # parsed = json.loads(produitsParse)


        # Pas de virgule delimitant les produits dans le json

        # jsonResult.write(json.dumps(parsed, indent=4, sort_keys=True))
        jsonResult.write(produitsParse)
    numpage = numpage + 1
    page_number = page_number +1



def getProductInfos(url):
    r = requests.get(url)
    c = r.content
    global details;
    soup = BeautifulSoup(c, 'html.parser')
    nova = soup.findAll('a', {"href": "/nova"})
    nutriscore = soup.findAll('a', {"href": "/nutriscore"})
    imgProduct = soup.find('img', {"id": "og_image"})["data-src"] or "http://www.friendlyfoodqatar.com/mt-content/uploads/2017/04/no-image.jpg"
    for img in nova:
        imgNova = img.find('img')
        if imgNova is not None:
            finalNova = imgNova['alt'];

    for img in nutriscore:
        imgNutriscore = img.find('img')
        if imgNutriscore is not None:
            final_nutriscore_alt = imgNutriscore["alt"];
        else:
            final_nutriscore_alt = "4"

        details.append({
            "novaText": finalNova,
            "imgProduct": imgProduct,
            "nutriscoreText": final_nutriscore_alt
        })


def getScore(novascore, nutriscore, bioscore):
    score = ((0.6 * nutriscore) + (0.3 * novascore) + (0.1 * bioscore)) * 100
    return score


def water(url):  # retourne True si l'élément est de l'eau, False sinon
    eau = False
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c, 'html.parser')
    caracteristiques = soup.find('div', class_="medium-12 large-8 xlarge-8 xxlarge-8 columns")
    for caracteristique in caracteristiques.findAll("a"):
        categorie = caracteristique.get("href")
        if categorie == '/categorie/eaux':
            eau = True
    return eau


def alcool(url):
    alc = False
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c, 'html.parser')
    caracteristiques = soup.find('div', class_="medium-12 large-8 xlarge-8 xxlarge-8 columns")
    for caracteristique in caracteristiques.findAll("a"):
        categorie = caracteristique.get("href")
        if categorie == '/categorie/boissons-alcoolisees':
            alc = True
    return alc


def run(runPage):
    print(runPage)
    webcrawler(home + runPage)


@app.route("/")
def main():
    run(str(1))
    return render_template('produits.html', produits=produits,page_number = page_number)


@app.route("/<runpage>")
def pagination(runpage):
    run(str(runpage))
    return render_template('produits.html', produits=produits, page_number=page_number)


if __name__ == '__main__':
    app.run(host='localhost', port=4000)
