
# coding=utf-8
from flask import Flask
from flask import render_template
app = Flask(__name__)


# Cài đặt với đường dẫn /
@app.route("/")
def homepage():
    return render_template('home.html', title="SoSanh.ga")

# Cài đặt với đường dẫn /search/?keyword='từ khóa'
@app.route("/compare")
def search():
    return render_template('search.html', title='So sánh giá')

# Cài đặt với đường dẫn /ten-san-pham
@app.route("/dssanpham")
def listproduct():
    return render_template('listproduct.html', title='Danh sách sản phẩm')

if __name__ == "__main__":
    # Only for debugging while developing
    #app.run(host='0.0.0.0', debug=True, port=80)
	app.run()
