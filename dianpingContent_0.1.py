#coding=utf-8
#   程序：大众点评商家数据抓取
#   版本：0.1
#   作者：andrew9tech
#   日期：2015-6-13
#   语言：Python 2.7

import urllib
import re
import os
import random
import time
import requests
from tempfile import TemporaryFile
from xlwt import Workbook
from xlutils.copy import copy
from xlrd import open_workbook

import sys 
reload(sys) 
sys.setdefaultencoding('utf-8')


Row = []
f = open(u"h:\\大众点评\\shlogo.txt", "r+")
for line in f.readlines():
    Row.append(line.strip('\n'))
f.close()
row = int(Row[0])

Num = []
f = open(u"h:\\大众点评\\" + u"上海编号.txt", "r+")
for line in f.readlines():
    Num.append(line.strip('\n'))
print len(Num)
f.close()

#代理IP实时抓取
P = ['183.223.137.20:8123', '218.204.140.104:8118', '116.231.100.46:8090', '101.4.136.66:84']

for n in range(8912, len(Num)):

    num = Num[n]
    #自定义一个请求
    url1 = 'http://t.dianping.com/deal/' + str(num)
    url2 = 'http://t.dianping.com/ajax/dealGroupShopDetail?dealGroupId=' + str(num) + '&cityId=1&action=shops&page=1&regionId=0'
    print "url1: ", url1
    #print num
    headers = {
        'Accept-Encoding':'gzip,deflate',
        'User-Agent':'Mozilla/3.1.0'
        }
    
    try:
        print "Length of P:", len(P)
        randomP = random.randint(0, len(P)-1)
        proxies = {"http" : 'http://'+str(P[randomP]),
                   "https" : 'http://'+str(P[randomP]),}
        print proxies
        #访问链接url1
        response1 = requests.get(url1, headers=headers, proxies=proxies, timeout=10)
        #判断头文件信息，包含数据是否用gzip传输,访问是否成功
        #print response1.headers
        shopcontent1 = response1.content
        #print shopcontent1


        #访问链接url2
        response2 = requests.get(url2, headers=headers, proxies=proxies, timeout=10)
        #判断头文件信息，包含数据是否用gzip传输,
        #print response2.headers
        shopcontent2 = response2.content
        #print shopcontent2
    except Exception as e10:
        del P[randomP]
        try:
            randomP = random.randint(0, len(P)-1)
            proxies = {"http" : 'http://'+str(P[randomP]),
                        "https" : 'http://'+str(P[randomP]),}
            print proxies
            #访问链接url1
            response1 = requests.get(url1, headers=headers, proxies=proxies, timeout=10)
            #判断头文件信息，包含数据是否用gzip传输,
            #print response1.headers
            shopcontent1 = response1.content
            #print shopcontent1

            #访问链接url2
            response2 = requests.get(url2, headers=headers, proxies=proxies, timeout=10)
            #判断头文件信息，包含数据是否用gzip传输,
            #print response2.headers
            shopcontent2 = response2.content
            #print shopcontent2
        except Exception as e11:
            del P[randomP]
            shopcontent2 = -1
            shopcontent1 = -1
            print "url error!"
            continue
            

    try:
        try:
            stores_name = re.findall(r'<h1 class="title">(.*?)</h1>', shopcontent1, re.S)[0]
            #print "stores_name:", stores_name
            Stores_Name = stores_name.replace(' ', '').replace('\n', '')
            #print "Stores_Name:", Stores_Name
        except Exception as e1:
            Stores_Name = -1
            print "Stores_Name:", e1

        try:
            subtitle = re.findall(r'<h2 class="sub-title">(.*?)</h2>', shopcontent1, re.S)[0]
            #print "subtitle: ", subtitle
            Sub_Title = re.sub(r'</?[^>]+>', '', subtitle).replace(' ', '').replace('\n', '')
            #print "Sub_Title:", Sub_Title
        except Exception as e2:
            Sub_Title = -1
            print "Sub_Title:", e2

        try:
            Price_Display = re.findall(r'<span class="price-display"><em>&#165;</em>(.*?)</span>', shopcontent1, re.S)[0]
            #print "Price_Display:", Price_Display
        except Exception as e3:
            Price_Display = -1
            print "Price_Display:", e3

        try:
            #<span class="price-discount">5<em>折</em></span>
            Price_Discount = re.findall(r'<span class="price-discount">(.*?)<em>折</em></span>', shopcontent1, re.S)[0]
            #print "Price_Discount:", Price_Discount
        except Exception as e4:
            Price_Discount = -1
            print "Price_Discount:", e4

        try:
            #<span class="price-original">价值&nbsp;<em>&#165;</em>70</span>
            Price_Original = re.findall(r'<span class="price-original">价值&nbsp;<em>&#165;</em>(.*?)</span>', shopcontent1, re.S)[0]
            #print "Price_Original:", Price_Original
        except Exception as e5:
            Price_Original = -1
            print "Price_Original:", e5
        
        try:
            #<span>已售<em class="J_current_join">651</em>份</span>
            J_current_join = re.findall(r'<span>已售<em class="J_current_join">(.*?)</em>份</span>', shopcontent1, re.S)[0]
            #print "J_current_join:", J_current_join
        except Exception as e6:
            J_current_join = -1
            print "J_current_join:", e6
        
        try:
            #<span class="star-rate">4.5</span>
            Star_rate = re.findall(r'<span class="star-rate">(.*?)</span>', shopcontent1, re.S)[0]
            #print "Star_rate:", Star_rate
        except Exception as e7:
            Star_rate = -1
            print "Star_rate:", e7

        try:
            product_evaluate_num_temp = re.findall(r'<span class="star-rate">.*?</span>(.*?)</a>条团购评价', shopcontent1, re.S)[0].replace(' ', '').replace('\n', '')
            #print "product_evaluate_num_temp:", product_evaluate_num_temp
            Product_Evaluate_Num = re.sub(r'</?[^>]+>', '', product_evaluate_num_temp)
            #print "Product_Evaluate_Num:", Product_Evaluate_Num
        except Exception as e8:
            Product_Evaluate_Num = -1
            print "Product_Evaluate_Num:", e8

        try:
            #<span class="star-rate">4.5</span>
            #{"address":"(.*?)","avgPrice":(.*?),"branchName":"(.*?)".*?"contactPhone":"(.*?)","crossRoad":"(.*?)".*?"glat":(.*?),"glng":(.*?).*?"shopId":(.*?),"shopName":"(.*?)".*?"voteTotal":(.*?)}
            Shop_info = re.findall(r'{"address":"(.*?)","avgPrice":(.*?),"branchName":"(.*?)","businessHours".*?"contactPhone":"(.*?)","crossRoad":"(.*?)","dealGroupId".*?"glat":(.*?),"glng":(.*?),"power".*?"shopId":(.*?),"shopName":"(.*?)".*?"voteTotal":(.*?)}', shopcontent2, re.S)
            #print "Shop_info:", Shop_info
            Shop_Num = len(Shop_info)
            #print Shop_Num
        except Exception as e9:
            Shop_info = -1
            print e9

        TGinfo = []
        #print type(TGinfo)
        TGinfo.append(Stores_Name)
        TGinfo.append(Sub_Title)
        TGinfo.append(Price_Display)
        TGinfo.append(Price_Discount)
        TGinfo.append(Price_Original)
        TGinfo.append(J_current_join)
        TGinfo.append(Star_rate)
        TGinfo.append(Product_Evaluate_Num)


        #数据保存于excl
        rb = open_workbook(u'h:\\大众点评\\shanghai.xls')
        #print "rb"
        rs = rb.sheet_by_index(0)
        #print "rs"
        wb = copy(rb)
        #print "wb"
        #wb = copy(open_workbook(u'h:\\meituan\\shanghai.xls').sheet_by_index(0))
        ws = wb.get_sheet(0)
        #print "ws"

        for i in xrange(8):
            ws.write(row,i,str(TGinfo[i]).decode('utf-8'))

        for i in xrange(Shop_Num):
            for j in xrange(10):
                #if len(Business_Locations[i][j])>0:
                ws.write(row,8+j,Shop_info[i][j].decode('utf-8'))
            row += 1

        #for j in range(7):
        #    sheet1.write(0,j,info[j].encode('utf-8'))

        wb.save(u"h:\\大众点评\\shanghai.xls")

        print row, "Done!"
       
    except Exception as e0:
      print e0
