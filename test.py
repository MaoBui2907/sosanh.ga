from crawler import search_fptshop, search_thegioididong, search_vienthonga, merge_data


oput = search_thegioididong("iphone")
oput2 = search_fptshop("iphone")
oput3 = search_vienthonga("iphone")
print(len(merge_data([oput, oput2, oput3])))