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
    for product in product_list.findAll("li"):
        name = product.find("span").text
        lien_product = product.find("a").get("href")
        lien = home + lien_product
        lien_image = getProductInfos(lien)
        nova = getDetailProduit(lien)
        if("4" in str(nova)):
            color = "red"
        if("3" in str(nova)):
            color = "orange"
        if("2" in str(nova)):
            color = "yellow"
        if("1" in str(nova)):
            color = "green"
        i = 0
        produits.append({
            "name":name,
            "url_product":lien_product,
            "lien_image":lien_image,
            "nova": nova,
            "color": color,
            #"nutri_img": details[i].imgNutriscore,
            #"nutriscoreText": details[i].nutriscoreText,
        })
        i=i+1

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
                'imgNutriscore': final_nutriscore_img,
                "nutriscoreText": final_nutriscore_alt
            })


def getDetailProduit(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c, 'html.parser')
    nova = soup.findAll('a', {"href": "/nova"})
    img = soup.findAll('img')

    for img in nova:
        imgNova = img.find('img')
        if imgNova is not None:
            return imgNova['alt'];



webcrawler(home)


@app.route("/")
def main():
    return render_template('produits.html', produits=produits)


if __name__ == '__main__':
    app.run(host='localhost', port=4000)
