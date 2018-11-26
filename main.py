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
    product_list = soup.find('ul', class_="products")
    i = 0
    for product in product_list.findAll("li"):
        name = product.find("span").text
        lien_product = product.find("a").get("href")
        lien = home + lien_product
        getProductInfos(lien)
        lien_image = details[i]["imgProduct"]
        nutriscoreText =details[i]["nutriscoreText"]
        nova = details[i]["novaText"]
        if("4" in str(nova)):
            color = "red"
            nova_number = 4
        if("3" in str(nova)):
            color = "orange"
            nova_number = 3
        if("2" in str(nova)):
            color = "yellow"
            nova_number = 2
        if("1" in str(nova)):
            color = "green"
            nova_number = 1

        if("A" in str(nutriscoreText)):
            nutri_number = 1
        if("B" in str(nutriscoreText)):
            nutri_number = 2
        if("C" in str(nutriscoreText)):
            nutri_number = 3
        if("D" in str(nutriscoreText)):
            nutri_number = 4
        if("E" in str(nutriscoreText)):
            nutri_number = 5


        produits.append({
            "name":name,
            "url_product":lien_product,
            "lien_image":lien_image,
            "nova": nova,
            "color": color,
            "nutriscoreText": nutriscoreText,
        })
        print("nova number" + str(nova_number) + "//nutri number" + str(nutri_number))
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
            final_nutriscore_img = imgNutriscore["src"];
            final_nutriscore_alt = imgNutriscore["alt"];


            #print("Nova ALT : "+str(finalNova)+ "///// nutriscore SRC : " +
             #     str(final_nutriscore_img) + "///// nutriscore ALT :"
              #    + str(final_nutriscore_alt)+ " ///// img product : "
               #   +str(imgProduct));


            details.append({
                "novaText": finalNova,
                "imgProduct": imgProduct,
                "nutriscoreText": final_nutriscore_alt
            })






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


if water("https://fr.openfoodfacts.org/produit/3274080005003/eau-de-source-cristaline"): #exemple utilisation water()
    score = 100
    print("C'est de l'eau !")

webcrawler(home)


@app.route("/")
def main():
    return render_template('produits.html', produits=produits)


if __name__ == '__main__':
    app.run(host='localhost', port=4000)

