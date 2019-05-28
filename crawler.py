
import requests as req
from bs4 import BeautifulSoup

# test set


def get_only_digit(text):
    """Return digit from string"""
    return ''.join(i for i in text if i.isdigit())


def check_same_product(product1, product2):
    """Return true if same product"""
    return True if product1 == product2 else False


def check_duplicate_product(datas, item):
    """Return true if has same product"""
    for i in datas:
        if check_same_product(i['name'], item['name']):
            return True

    return False


def sort_data_list(data, reverse=False):
    """Sắp xếp giá theo thứ tự tang dan"""
    return sorted(data, key=lambda k: k['price'], reverse=reverse)


def get_product(site, link):
    """"Lấy thông tin sản phẩm với các site khác nhau"""
    if (site == "thegioididong"):
        return get_product_theogioididong(link)
    elif (site == "fptshop"):
        return get_product_fptshop(link)
    elif (site == "vienthonga"):
        return get_product_vienthonga(link)
    return(0)

def get_product_theogioididong(link):
    """Lấy thông tin từ trang thế giới di động"""
    url = link.rstrip()
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    code = req.get(url, headers=header)
    plain_text = code.text
    html_text = BeautifulSoup(plain_text)

    product_name = html_text.body.find('h1').text.strip()
    product_first_price = get_only_digit(
        html_text.body.find('span', 'hisprice').text)
    product_real_price = get_only_digit(html_text.body.find(
        'div', 'area_price').find('strong').text.strip())
    product_discount = product_real_price * 100 / product_first_price
    product_short_description = html_text.body.find(
        'ul', 'parameter').text.strip()
    product_rate = html_text.body.find('div', 'lcrt').get('data-gpa')
    output = {
        "Tên sản phẩm": product_name,
        "Giá gốc": product_first_price,
        "Giá bán": product_real_price,
        "Giảm giá": product_discount,
        "Mô tả ngắn": product_short_description,
        "Đánh giá": product_rate
    }
    return(output)


def get_product_fptshop(link):
    """Lấy thông tin từ trang thế giới di động"""
    url = link.rstrip()
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    code = req.get(url, headers=header)
    plain_text = code.text
    html_text = BeautifulSoup(plain_text)

    product_name = html_text.body.find('h1', 'fs-dttname').find(text=True)
    product_first_price = get_only_digit(html_text.body.find(
        'p', 'fs-dtprice').find('del').text if html_text.body.find(
        'p', 'fs-dtprice').find('del') else "")
    product_real_price = get_only_digit(html_text.body.find(
        'p', 'fs-dtprice').find(text=True))
    product_discount = product_real_price * 100 / product_first_price
    product_short_description = html_text.body.find(
        'div', 'fs-tsright').text.strip()
    product_rate = html_text.body.find('div', 'fs-dtrt-c1').find('h5').text
    output = {
        "Tên sản phẩm": product_name,
        "Giá gốc": product_first_price,
        "Giá bán": product_real_price,
        "Giảm giá": product_discount,
        "Mô tả ngắn": product_short_description,
        "Đánh giá": product_rate
    }
    return(output)


def get_product_vienthonga(link):
    """thông tin sản phẩm viễn thông A"""
    url = link.rstrip()
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    code = req.get(url, headers=header)
    plain_text = code.text
    html_text = BeautifulSoup(plain_text)

    product_name = html_text.body.find('h1', 'name').find(text=True)
    product_first_price = get_only_digit(html_text.body.find(
        'p', 'fs-dtprice').find('del').text if html_text.body.find(
        'p', 'fs-dtprice').find('del') else "")
    product_real_price = get_only_digit(html_text.body.find(
        'div', 'detail-price').find(text=True))
    product_discount = product_real_price * 100 / product_first_price
    product_short_description = html_text.body.find(
        'table', 'tablet').text.strip()
    product_rate = '0/5'
    output = {
        "Tên sản phẩm": product_name,
        "Giá gốc": product_first_price,
        "Giá bán": product_real_price,
        "Giảm giá": product_discount,
        "Mô tả ngắn": product_short_description,
        "Đánh giá": product_rate
    }
    return(output)


def get_product_info(link):
    """return"""
    pass


def merge_compare(datas, product, site):
    """return list with update"""
    output_list = datas
    for i in datas:
        if check_same_product(i['name'], product['name']):
            i['compare'].append({
                'site': site,
                'price': product['price'],
                'delprice': product['delprice'],
                'link': product['link']
            })


def merge_data(datas):
    """Return merge data"""
    ouput_list = []
    for i in datas:
        store = i['site']
        for product in i['products']:
            if not check_duplicate_product(ouput_list, product):
                ouput_list.append({
                    'name': product['name'],
                    'image': product['image'],
                    'compare': [{
                        'site': store,
                        'price': product['price'],
                        'delprice': product['delprice'],
                        'link': product['link']
                    }]
                })
            else:
                merge_compare(ouput_list, product, store)

    for i in ouput_list:
        i['compare'] = sort_data_list(i['compare'])

    return ouput_list


def search_thegioididong(keyword):
    """Search with thegioididong"""
    url = "https://www.thegioididong.com/tim-kiem?key=" + keyword

    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    code = req.get(url, headers=header)
    plain_text = code.text
    html_text = BeautifulSoup(plain_text)
    products = []
    page = 1

    if (html_text.body.find('ul', 'listsearch') is not None):
        products_blocks = html_text.body.find(
            'ul', 'listsearch').findAll('li')
        while (html_text.body.find('a', 'viewmore') is not None):
            page += 1
            if page == 5:
                break
            viewmore = req.post('https://www.thegioididong.com/aj/SearchV2/LoadMoreProductResult',
                                data={'keyword': keyword, 'pageIndex': page, 'orderby': 0})
            more = BeautifulSoup(viewmore.text)
            more_product = more.find('ul', 'listsearch').findAll('li')
            products_blocks.extend(more_product)

        products = [{'name': i.find('h3').text, 'image': i.find('img')['src'],
                     'price': get_only_digit(i.find('strong').find(text=True)),
                     'delprice': (get_only_digit(i.find('a').find('span').find(text=True)) if i.find('a').find('span') is not None else '') if i.find('a') is not None else '',
                     'link': 'https://thegiodidong.com' + i.find('a')['href']} for i in products_blocks if i.find('strong') is not None and i.find('strong').find(text=True) is not None]

    ouput_data = {
        "site": "thegiodidong",
        "products": products
    }

    return ouput_data


def search_fptshop(keyword):
    """Search with fptshop"""

    url = "https://fptshop.com.vn/tim-kiem/" + keyword

    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    code = req.get(url, headers=header)
    plain_text = code.text
    html_text = BeautifulSoup(plain_text)

    products = []

    if (html_text.body.find('div', 'category-products') is not None):
        products_blocks = html_text.body.find(
            'div', attrs={'id',  'category-products'}).findAll('div', attrs={'class', 'fs-lpitem'})

        products = [{'name': i.find('h3', 'fs-icname').text, 'image': i.find('img')['src'],
                     'price': get_only_digit(i.find('p',
                                                    'fs-icpri').find(text=True)) if i.find('p',
                                                                                           'fs-icpri') is not None else '', 'delprice': (get_only_digit(i.find('p',
                                                                                                                                                               'fs-icpri').find('del').find(text=True)) if i.find('p',
                                                                                                                                                                                                                  'fs-icpri').find('del') is not None else '') if i.find('p',
                                                                                                                                                                                                                                                                         'fs-icpri') is not None else '', 'link': 'https://fptshop.com' + i.find('a')['href']} for i in products_blocks]
    ouput_data = {
        "site": "fptshop",
        "products": products
    }

    return ouput_data

# not working


def search_viettelstore(keyword):
    """Search with viettelstore"""
    url = "https://viettelstore.vn/ket-qua-tim-kiem.html?keyword=" + keyword

    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36', 'Cookie': '__utma=12798129.281598210.1556814566.1556814566.1557070725.2; __utmz=12798129.1557070725.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=12798129; __utmb=12798129.1.10.1557070725; __utmt=1'}
    code = req.get(url, headers=header)
    plain_text = code.text
    html_text = BeautifulSoup(plain_text)
    products = []

    if (html_text.body.find('div', 'div_Danh_Sach_San_Pham') is not None):
        products_blocks = html_text.body.find(
            'div', attrs={'id',  'div_Danh_Sach_San_Pham'}).findAll('div', 'ProductList3Col_item')
        products = [{'name': i.find('div', 'name').text, 'image': i.find('img')['src'],
                     'price': get_only_digit(i.find('div', 'price-1').find(text=True)) if i.find('div',
                                                                                                 'price-1') is not None else '', 'delprice': get_only_digit(i.find('span',
                                                                                                                                                                   'price-old').find(text=True)) if i.find('span',
                                                                                                                                                                                                           'price-old') is not None else ''} for i in products_blocks]

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
                     'delprice': '', 'link': 'https://vienthonga.vn'+i.find('div', 'product-image').find('a')['href']} for i in products_blocks]

    ouput_data = {
        "site": "vienthonga",
        "products": products
    }

    return ouput_data
