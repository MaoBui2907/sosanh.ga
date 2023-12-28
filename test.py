
import json
from crawler import Crawler

crawler = Crawler()

with open('test_01_2023.json', 'w+') as f:
    json.dump(crawler.search_thegioididong('iphone'), f)

# print(search_thegioididong("tai nghe nhét tai"))
# oput2 = search_fptshop("iphone")
# oput3 = search_vienthonga("iphone")
# data = merge_data([oput, oput2, oput3])
# print(oput2)
# print(get_product_fptshop("https://fptshop.com.vn/dien-thoai/vsmart-joy-1-plus-2gb-16gb"))
# print(get_product_theogioididong("https://thegioididong.com/dtdd/vsmart-active-1"))
# print(get_product_vienthonga("https://vienthonga.vn/samsung-galaxy-s10plus.html?cn=VINPRO+"))