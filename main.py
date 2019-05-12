
# coding=utf-8
from flask import Flask
from flask import request
from flask import render_template
from crawler import search_fptshop, search_thegioididong, search_vienthonga, merge_data
app = Flask(__name__)


# Cài đặt với đường dẫn /
@app.route("/")
def homepage():
    return render_template('home.html', title="SoSanh.ga")

# Cài đặt với đường dẫn /timkiem?keyword=""
@app.route("/timkiem")
def search():
    keyword = request.args.get('keyword', default='', type=str)

    fptshop = search_fptshop(keyword)
    tgdd = search_thegioididong(keyword)
    vienthonga = search_vienthonga(keyword)

    data = merge_data([fptshop, tgdd, vienthonga])
    return render_template('dssp.html', title='Danh sách sản phẩm', data=data[:20])

# Cài đặt với đường dẫn /ten-san-pham
@app.route("/sanpham")
def product():
    return render_template('product.html', title='Sản phẩm')


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)
    # app.run()
