from flask import Flask
from flask import render_template
app = Flask(__name__)

# Cài đặt với đường dẫn /
@app.route("/")
def homepage():
    return render_template('homepage.html', title="So sánh giá")

# Cài đặt với đường dẫn /search/?keyword='từ khóa'
@app.route("/search/?")
def search():
    return render_template('search.html', title='Tìm kiếm')

# Cài đặt với đường dẫn /ten-san-pham
@app.route("/?ten-san-pham")
def product():
    return render_template('product.html', title='Sản phẩm')

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
