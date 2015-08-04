#coding=utf-8
#   程序：美团商家数据抓取
#   版本：2.0
#   作者：andrew9tech
#   日期：2015-2-29
#   语言：Python 2.7
#   操作：改写！
#        启用requests模块，弃用urllib\urllib2\cookielib
#        以后优选requests模块
#        添加随机代理，并剔除链接性不好的代理，单次请求设置timeout避免长时间等待
#        记录excl的row
#
#   功能：
#---------------------------------------
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
f = open(u"H:\\meituan\\shlogo_test.txt", "r+")
for line in f.readlines():
    Row.append(line.strip('\n'))
f.close()
row = int(Row[0])


Num = []
f = open(u"H:\\meituan\\shanghai2.txt", "r+")
for line in f.readlines():
    Num.append(line.strip('\n'))
print len(Num)
f.close()

Proxy = []
f = open(u"G:\\爬虫\\代理\\proxy_list.txt", "r+")
for line in f.readlines():
    Proxy.append(line.strip('\n'))
f.close()
ProxyNum = len(Proxy)

for n in range(1280,len(Num)):

    num = Num[n]
    #自定义一个请求
    url = 'http://www.meituan.com/deal/' + str(num) + '.html'
    print num
    headers = {
        'Accept-Encoding':'gzip,deflate',
    #    'Content-Type':'application/x-www-form-urlencoded',
    #    'Origin':'http://rd2.zhaopin.com',
    #    'Referer':'http://rd2.zhaopin.com/portal/myrd/regnew.asp?za=2',
        'User-Agent':'Mozilla/3.1.0'
        }

    randomNum = random.randint(0, len(Proxy))
    proxies = {
                "http" : 'http://' + str(Proxy[randomNum]),
                "https": "http://10.10.1.10:1080",}
    print "proxy"


    try:
        #访问该链接#
        response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
        #判断头文件信息，包含数据是否用gzip传输,
        print response.headers
        shopcontent = response.content
        #print shopcontent
    except Exception as e:
        #删除改低速代理
        del Proxy[randomNum]
        try:
            proxies = {"http" : 'http://' + str(Proxy[random.randint(0, len(Proxy))]),"https": "http://10.10.1.10:1080",}
            response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
            shopcontent = response.content
        except Exception as e:
            #删除改低速代理
            del Proxy[randomNum]
            print e
            continue
            

    try:
        Customers_species = re.findall(r'<a class="link--black__green" gaevent="crumb/category/1".*?>(.*?)</a><span>', shopcontent, re.S)
        #print "Customers_species:", Customers_species[0]
        #print type(Customers_species[0])

        Stores_Name = re.findall(r'<h1 class="deal-component-title">(.*?)</h1>', shopcontent, re.S)
        #print "Stores_Name:", Stores_Name[0]

        Discount_Price = re.findall(r'<div class="deal-component-description">.*?仅售(.*?)元.*?</div>', shopcontent, re.S)
        #print "Discount_Price:", Discount_Price

        Product_Evaluate = re.findall(r'<span class="deal-component-rating-stars orange hidden">(.*?)</span>分.*?<span class="deal-component-rating-comment-count orange hidden">(.*?)</span>人评价</a>', shopcontent, re.S)
        #print "Product_Evaluate:", Product_Evaluate

        Product_Info = re.findall(r'<li>门店价.*?</span>(.*?)</del></li>.*?<li>折扣<br /><span class="num">(.*?)折</span></li>.*?<li>已售<br /><span class="num">(.*?)</span></li>', shopcontent, re.S)
        #print "Product_Info:", Product_Info

        temp = re.findall(r'<div id="J-bizinfo-list" data-poi="(.*?)" data-reservationPhoneNumber=', shopcontent, re.S)
        Business_Locations = re.findall(r'"shopid":(.*?),"name":"(.*?)","address":"(.*?)".*?"disname":"(.*?)",.*?,"phone":"(.*?)","latlng":"(.*?)",.*?,"poiid":(.*?),.*?"avgscore":"(.*?)","fbcount":(.*?)},"cityname":"(.*?)",.*?,"subwayname":"(.*?)",.*?}', temp[0].replace('&quot;', '"').decode('unicode-escape'), re.S)
        #print Business_Locations

        Shop_Num = len(Business_Locations)
        print Shop_Num
        #print len(Business_Locations[0])



        #数据保存于excl
        rb = open_workbook(u'h:\\meituan\\shanghai_test.xls')
        print "rb"
        rs = rb.sheet_by_index(0)
        print "rs"
        wb = copy(rb)
        print "wb"
        #wb = copy(open_workbook(u'h:\\meituan\\shanghai.xls').sheet_by_index(0))
        ws = wb.get_sheet(0)
        print "ws"

        #商品ID
        ws.write(row,0,str(num))
        print "ID"
        #商品种类
        if len(Customers_species[0])>0:
            ws.write(row,1,Customers_species[0].decode('utf-8'))
        #连锁店名称
        if len(Stores_Name[0])>0:
            ws.write(row,2,Stores_Name[0].decode('utf-8'))

        #商品评价(评分、评价数量)
        if len(Product_Evaluate)>0:
            ws.write(row,3,Product_Evaluate[0][0].decode('utf-8'))
            ws.write(row,4,Product_Evaluate[0][1].decode('utf-8'))
        #折后价
        if len(Discount_Price)>0:
            ws.write(row,5,Discount_Price[0].decode('utf-8'))
        #折后价
        if len(Product_Info)>0:
            ws.write(row,6,Product_Info[0][0].decode('utf-8'))
            ws.write(row,7,Product_Info[0][1].decode('utf-8'))
            ws.write(row,8,Product_Info[0][2].decode('utf-8'))

        for i in xrange(Shop_Num):
            for j in xrange(11):
                #if len(Business_Locations[i][j])>0:
                ws.write(row,9+j,Business_Locations[i][j].decode('utf-8'))
            row += 1

        #for j in range(7):
        #    sheet1.write(0,j,info[j].encode('utf-8'))

        wb.save(u"h:\\meituan\\shanghai_test.xls")

        print row, "Done!"
        #代理持久化，写入txt
        f = open(u"H:\\meituan\\shlogo_test.txt",'w+')
        f.write("%d\n"%row)
        f.close()



    except Exception as e1:
      print e1
                
