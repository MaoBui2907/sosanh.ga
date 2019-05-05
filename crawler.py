
import requests as req
from bs4 import BeautifulSoup


def get_only_digit(text):
    """Return digit from string"""
    return ''.join(i for i in text if i.isdigit())


def search_fptshop(keyword):
    """Search with fptshop"""

    url = "https://fptshop.com.vn/tim-kiem/" + keyword

    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    code = req.get(url, headers=header)
    plain_text = code.text
    html_text = BeautifulSoup(plain_text)

    products = []

    if (html_text.body.find('div', 'fs-senull') is None):
        products_blocks = html_text.body.find(
            'div', attrs={'id',  'category-products'}).findAll('div', attrs={'class', 'fs-lpitem'})

        products = [{'name': i.find('h3', 'fs-icname').text, 'image': i.find('img')['src'],
                     'price': get_only_digit(i.find('p', 'fs-icpri').find(text=True)) if i.find('p',
                     'fs-icpri') is not None else '', 'delprice': ( get_only_digit(i.find('p', 
                     'fs-icpri').find('del').find(text=True)) if i.find('p',
                     'fs-icpri').find('del') is not None else '' ) if i.find('p',
                     'fs-icpri') is not None  else '','link': 'https://thegioididong.com' + i.find('a')['href']} for i in products_blocks]

    ouput_data = {
        "site": "fptshop",
        "products": products
    }

    return ouput_data


def search_viettelstore(keyword):
    """Search with viettelstore"""
    url = "https://viettelstore.vn/ket-qua-tim-kiem.html?keyword=" + keyword

    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36', 'Cookie':'__utma=12798129.281598210.1556814566.1556814566.1557070725.2; __utmz=12798129.1557070725.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=12798129; __utmb=12798129.1.10.1557070725; __utmt=1'}
    code = req.get(url, headers=header)
    plain_text = code.text
    html_text = BeautifulSoup(plain_text)
    print(html_text)
    products = []

    if (html_text.body.find('div', 'div_Danh_Sach_San_Pham') is not None):
        products_blocks = html_text.body.find(
            'div', attrs={'id',  'div_Danh_Sach_San_Pham'}).findAll('div', 'ProductList3Col_item')

        # print(products_blocks)

        products = [{'name': i.find('div', 'name').text, 'image': i.find('img')['src'],
                     'price': get_only_digit(i.find('div', 'price-1').find(text=True)) if i.find('div', 
                     'price-1') is not None else '', 'delprice': get_only_digit(i.find('span', 
                     'price-old').find(text=True)) if i.find('span',
                     'price-old') is not None  else ''} for i in products_blocks]

    ouput_data = {
        "site": "viettelshop",
        "products": products
    }

    return ouput_data

def search_vienthonga(keyword):
    """Search with vienthonga"""
    url = "https://vienthonga.vn/tim-kiem?q=" + keyword

    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    code = req.get(url, headers=header)
    plain_text = code.text
    html_text = BeautifulSoup(plain_text)
    products = []

    if (html_text.body.find('div', 'shop-masonry') is not None):
        products_blocks = html_text.body.find(
            'div', 'shop-masonry').findAll('div', 'masonry-item')

        products = [{'name': i.find('h3', 'name').text, 'image': i.find('img')['data-original'],
                     'price': get_only_digit(i.find('div', 'price-1').find(text=True)) if i.find('div', 'price-1') is not None else '',
                     'delprice': '', 'link': 'https://vienthonga.vn'+i.find('div','product-image').find('a')['href']} for i in products_blocks]

    ouput_data = {
        "site": "vienthonga",
        "products": products
    }

    return ouput_data

print(search_vienthonga("dasfdf afdsafs"))