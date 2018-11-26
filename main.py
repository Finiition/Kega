# USING PYTHON 3.7

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

home = 'https://fr.openfoodfacts.org/'

numpage = 1
app = Flask(__name__)
produits = []
details = []


def webcrawler(page):
    r = requests.get(page)
    c = r.content
    soup = BeautifulSoup(c, 'html.parser')
    nutri_number = 0
    nova_number = 0
    global numpage
    global produits
    global details
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
    numpage = numpage + 1




def getProductInfos(url):
    r = requests.get(url)
    c = r.content
    global details;
    soup = BeautifulSoup(c, 'html.parser')
    nova = soup.findAll('a', {"href": "/nova"})
    nutriscore = soup.findAll('a', {"href": "/nutriscore"})
    imgProduct = soup.find('img', {"id": "og_image"})["data-src"]
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
    caractéristiques = soup.find('div', class_="medium-12 large-8 xlarge-8 xxlarge-8 columns")
    for caractéristique in caractéristiques.findAll("a"):
        categorie = caractéristique.text.lower()
        if 'eaux' in categorie:
            eau = True
    return eau


while numpage < 10:
    print(home + str(numpage))
    webcrawler(home + str(numpage))
#print("produits",produits)
#print("details", details)

@app.route("/")
def main():
    return render_template('produits.html', produits=produits)


if __name__ == '__main__':
    app.run(host='localhost', port=4000)
