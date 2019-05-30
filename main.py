
# coding=utf-8
import math
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from crawler import search_fptshop, search_thegioididong, search_vienthonga, merge_data, get_product
app = Flask(__name__)


# Cài đặt với đường dẫn /
@app.route("/")
def homepage():
    return render_template('home.html', title="SoSanh.ga")

# Cài đặt với đường dẫn /timkiem?keyword=""
@app.route("/timkiem", methods=['GET'])
def search():
    if request.method == 'GET':
        keyword = request.args.get('keyword', default='', type=str)
        page = request.args.get('page', default=1, type=int)
        fptshop = search_fptshop(keyword)
        tgdd = search_thegioididong(keyword)
        vienthonga = search_vienthonga(keyword)
        data = merge_data([fptshop, tgdd, vienthonga])
        num_per_page = 16

        max_page = math.ceil(len(data) / num_per_page)
        # print(max_page)
        if (page > max_page):
            page = max_page
        return render_template('dssp.html', title='Danh sách sản phẩm', keyword=keyword, data=data[(page-1)*num_per_page:page*num_per_page if page*num_per_page < len(data) else len(data)], max_page=max_page, page=page, max_data=len(data))

# Cài đặt với đường dẫn /ten-san-pham
@app.route("/sanpham", methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        data = eval(request.get_json()['data'])
        print("data", data)
        name = data['name']
        image = data['image']
        products = [{'site': i['site'], 'data': get_product(
            i['site'], i['link'])} for i in data['compare']]
        print("products", products)
        return render_template('product.html', title='Sản phẩm', shops=products, image=image, name=name)
    elif request.method == 'GET':
        return render_template('product.html', title='Sản phẩm')


if __name__ == "__main__":
    # Only for debugging while developing
    # app.run(host='0.0.0.0', debug=True, port=5000)
    app.run()
