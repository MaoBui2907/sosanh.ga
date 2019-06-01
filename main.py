
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
    return render_template('home.html', title="Sosanh.ga | So sánh giá sản phẩm công nghệ")

# Cài đặt với đường dẫn /timkiem?keyword=""&page=
@app.route("/timkiem", methods=['GET'])
def search():
    if request.method == 'GET':
        # các tham số truyền vào từ url
        keyword = request.args.get('keyword', default='', type=str)
        page = request.args.get('page', default=1, type=int)

        # Bắt đầu tìm kiếm với từ khóa trên các trang
        fptshop = search_fptshop(keyword)
        tgdd = search_thegioididong(keyword)
        vienthonga = search_vienthonga(keyword)

        # gom dữ liệu
        data = merge_data([fptshop, tgdd, vienthonga])
        # chọn số sản phẩm hiển thị trên 1 trang
        num_per_page = 16
        # lấy tổng số sản phẩm chia cho sản phẩm mỗi trang
        max_page = math.ceil(len(data) / num_per_page)
        if (page > max_page):
            page = max_page
        return render_template('dssp.html', title= keyword + ' | Kết quả tìm kiếm', keyword=keyword, data=data[(page-1)*num_per_page:page*num_per_page if page*num_per_page < len(data) else len(data)], max_page=max_page, page=page, max_data=len(data))

# Cài đặt với đường dẫn /ten-san-pham
@app.route("/sanpham", methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        data = (eval(request.data))
        name = data['name']
        image = data['image']
        compare = data['compare']
        shops = []
        for i in compare:
            shops.append(get_product(i['site'], i['link']))
        return render_template('product.html', title=name + ' | So sánh',best_price=compare[0]['site'], image=image, name=name, compare=compare, shops=shops)

if __name__ == "__main__":
    # Only for debugging while developing
    # app.run(host='0.0.0.0', debug=True, port=5000)
    app.run()
