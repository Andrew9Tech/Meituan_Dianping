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


P = ['183.223.137.20:8123', '218.204.140.104:8118', '116.231.100.46:8090', '101.4.136.66:84',
     '39.177.107.36:8123', '117.165.43.62:8123', '39.178.92.148:8123', '49.1.245.236:3128',
     '117.173.23.88:8123', '39.166.16.104:8123', '39.177.151.116:8123', '223.85.83.36:8123',
     '117.187.10.140:80', '39.188.190.13:8123', '39.167.206.49:8123', '39.168.93.50:8123',
     '39.169.229.46:8123', '104.238.140.63:3128', '117.174.198.63:8123', '101.4.136.66:80',
     '117.174.206.100:8123', '222.61.18.60:80', '116.228.80.186:8080', '39.167.58.67:8123',
     '183.223.137.119:8123', '117.176.246.235:8123', '39.177.116.51:8123', '39.177.90.233:8123',
     '101.4.136.65:86', '39.178.61.85:8123', '39.167.200.33:8123', '39.166.28.95:8123',
     '223.86.213.143:8123', '39.166.162.162:8123', '101.4.136.65:83', '101.4.136.67:82',
     '223.85.17.212:8123', '39.177.17.51:8123', '112.19.7.23:8123', '117.185.13.85:8080',
     '39.178.41.126:8123', '39.178.151.202:8123', '117.170.93.38:8123', '108.165.33.13:3128',
     '183.227.145.18:8123', '39.184.5.120:8123', '39.177.165.190:8123', '39.184.76.37:8123', 
     '183.220.194.244:8123', '219.239.146.211:8088', '117.174.206.100:8123', '117.164.140.49:8123', 
     '218.78.210.54:8080', '222.61.18.60:80', '39.168.187.64:8123', '117.177.243.42:8082', 
     '39.177.146.83:8123', '101.4.136.67:82', '101.4.136.65:86', '101.4.136.65:83', 
     '117.173.23.88:8123', '101.4.136.66:84', '117.173.20.29:8123', '39.171.135.106:8123', 
     '111.40.196.70:80', '117.185.13.86:8000', '116.228.80.186:8080', '101.4.136.66:80', 
     '39.167.40.145:8123', '202.70.52.66:9595', '59.78.160.248:8080', '183.216.189.6:8123', 
     '112.19.5.49:8123', '39.189.65.210:8123', '117.177.243.26:8080', '101.226.249.237:80', 
     '110.73.10.33:8123', '140.75.252.163:8090',
     '117.177.243.71:85', '39.178.37.162:8123', '117.162.159.127:8123', '223.94.136.31:8123', 
     '183.223.242.141:8123', '39.176.72.156:8123', '223.95.107.214:8123', '183.216.135.219:8123', 
     '112.44.206.19:8123', '211.141.121.27:8123', '39.176.165.131:8123', '223.86.219.115:8123', 
     '39.176.7.89:8123', '112.15.122.144:8123', '117.147.250.198:8123', '223.85.111.17:8123', 
     '117.175.111.150:8123', '39.171.130.70:8123', '117.164.50.208:8123', '117.170.29.99:8123', 
     '117.178.66.211:8123', '117.164.108.2:8123', '183.223.215.118:8123', '117.149.243.76:8123', 
     '117.167.93.21:8123', '223.85.107.158:8123', '112.15.115.125:8123', '108.165.33.5:3128', 
     '120.206.166.94:8123', '39.176.130.165:8123', '223.93.86.193:8123', '117.185.13.87:8080', 
     '39.177.107.167:8123', '39.158.155.205:8123', '39.179.182.126:8123', '117.177.144.44:8123', 
     '117.168.231.232:8123', '117.175.109.6:8123', '183.245.52.145:8123', '101.226.249.237:80', 
     '117.162.169.62:8123', '117.177.243.29:8083', '117.185.13.85:8080', '117.173.20.225:8123', 
     '223.84.22.179:8123', '117.163.196.213:8123', '183.217.208.192:8123', '39.179.28.54:8123',
     '39.189.68.114:8123','124.202.221.26:8118','115.44.102.139:8118','111.199.149.85:8118',
     '39.79.8.172:80','123.234.8.36:8089','117.24.88.246:8118','110.200.182.153:8118','202.108.50.75:80',
     '202.100.166.132:80','218.76.37.44:18186','183.230.119.3:8123','218.56.165.118:8080',
     '218.206.83.89:80','183.203.208.162:8118','114.246.50.186:8118','106.120.62.174:8118','39.190.104.201:8123','124.88.67.24:80','211.141.130.106:8118','1.192.222.39:8118',
     '183.221.55.242:8123','111.164.222.189:8118','222.45.196.17:8118','119.4.21.176:80','124.88.67.20:80','59.67.93.173:18186','175.1.230.115:80','183.221.217.217:8123',
     '124.88.67.13:80','124.88.67.10:80','221.219.63.96:8118','111.13.109.52:80','183.221.217.95:8123','121.40.92.72:8088','122.94.30.65:8118','1.192.239.70:8118',
     '111.164.72.57:8118','182.18.58.2:9080','114.252.108.207:8118','111.164.58.229:8118','222.39.145.180:8118','124.88.67.40:80','183.36.183.76:18186','123.121.132.47:8118',
     '114.252.128.213:8118','183.221.209.145:8123','1.202.81.11:8118','111.164.59.198:8118','222.161.248.122:80','61.163.169.188:18186','222.45.16.204:8118','180.160.97.7:18186',
     '111.199.149.85:8118','118.193.11.38:80','222.45.196.19:8118','119.136.34.135:80','125.39.66.67:80','117.24.88.246:8118','222.186.57.22:443','223.146.39.185:80','218.28.96.39:3128',
     '182.200.101.90:80','183.203.208.162:8118','123.233.145.70:8118','60.26.78.25:8118','49.76.235.111:8080','183.203.208.167:8118','112.231.28.145:8118','211.141.130.106:8118',
     '39.79.8.172:80','123.118.154.98:8118','182.118.23.7:8081','122.94.207.117:8118','202.100.166.132:80','58.48.0.238:9080','39.189.68.114:8123','218.206.83.89:80','183.203.208.169:8118',
     '106.120.62.174:8118','183.221.184.194:8123','124.88.67.10:80','218.76.37.44:18186','123.0.245.164:80','114.255.183.174:8080','1.192.222.39:8118','124.202.221.26:8118',
     '111.164.222.189:8118','183.230.119.3:8123','115.44.102.139:8118','122.94.30.65:8118','123.234.8.36:8089','114.246.50.186:8118','39.190.104.201:8123','110.200.182.153:8118',
     '175.1.230.115:80','202.108.50.75:80','218.56.165.118:8080','222.39.145.180:8118','183.221.55.242:8123','222.45.196.17:8118','111.13.109.52:80','124.88.67.24:80',
     '1.202.81.11:8118','59.67.93.173:18186','183.221.217.217:8123','111.164.72.57:8118','182.18.58.2:9080','124.88.67.20:80','222.45.16.204:8118','114.252.108.207:8118',
     '221.219.63.96:8118','183.221.217.95:8123','124.88.67.13:80','223.146.39.185:80','123.121.132.47:8118','1.192.239.70:8118','111.164.58.229:8118','121.40.92.72:8088',
     '49.76.235.111:8080','61.163.169.188:18186','183.36.183.76:18186','114.252.128.213:8118','112.231.28.145:8118','111.199.149.85:8118','222.161.248.122:80','117.24.88.246:8118',
     '124.88.67.40:80','111.164.59.198:8118','122.94.207.117:8118','125.39.66.67:80','183.203.208.162:8118','222.186.57.22:443','183.221.209.145:8123','222.45.196.19:8118',
     '183.221.184.194:8123','123.0.245.164:80','211.141.130.106:8118','60.26.78.25:8118','124.202.221.26:8118','180.160.97.7:18186','218.28.96.39:3128','183.230.119.3:8123',
     '118.193.11.38:80','114.246.50.186:8118','119.136.34.135:80','123.118.154.98:8118','183.203.208.167:8118','119.4.21.176:80','183.221.55.242:8123','182.200.101.90:80',
     '58.48.0.238:9080','123.233.145.70:8118','183.203.208.169:8118','182.118.23.7:8081','124.88.67.10:80','39.189.68.114:8123','59.67.93.173:18186','39.79.8.172:80',
     '114.255.183.174:8080','122.94.30.65:8118','218.76.37.44:18186','221.219.63.96:8118','202.100.166.132:80','218.206.83.89:80','115.44.102.139:8118','106.120.62.174:8118',
     '123.234.8.36:8089','222.39.145.180:8118','39.190.104.201:8123','110.200.182.153:8118','1.192.239.70:8118','202.108.50.75:80','218.56.165.118:8080','1.192.222.39:8118',
     '1.202.81.11:8118','111.164.222.189:8118','222.45.196.17:8118','183.36.183.76:18186','124.88.67.24:80','222.45.16.204:8118','175.1.230.115:80','183.221.217.217:8123',
     '111.164.59.198:8118','124.88.67.20:80','223.146.39.185:80','111.13.109.52:80','183.221.217.95:8123','222.45.196.19:8118','124.88.67.13:80','49.76.235.111:8080',
     '111.164.72.57:8118','111.164.58.229:8118','112.231.28.145:8118','218.28.96.39:3128','182.18.58.2:9080','114.252.108.207:8118','121.40.92.72:8088','114.252.128.213:8118',
     '122.94.207.117:8118','183.203.208.167:8118','222.161.248.122:80','123.121.132.47:8118','124.88.67.40:80','183.221.184.194:8123','182.118.23.7:8081','123.0.245.164:80',
     '125.39.66.67:80','61.163.169.188:18186','222.186.57.22:443','183.221.209.145:8123','60.26.78.25:8118','180.160.97.7:18186','118.193.11.38:80','119.136.34.135:80',
     '123.118.154.98:8118','182.200.101.90:80','123.233.145.70:8118','58.48.0.238:9080','183.203.208.169:8118','114.255.183.174:8080']

for n in range(8912, len(Num)):

    num = Num[n]
    #num = '11943615'
    #自定义一个请求
    #http://t.dianping.com/deal/12343594
    url1 = 'http://t.dianping.com/deal/' + str(num)
    url2 = 'http://t.dianping.com/ajax/dealGroupShopDetail?dealGroupId=' + str(num) + '&cityId=1&action=shops&page=1&regionId=0'
    #http://t.dianping.com/ajax/dealGroupShopDetail?dealGroupId=11943615&cityId=1&action=shops&page=1&regionId=0
    print "url1: ", url1
    #print num
    headers = {
        'Accept-Encoding':'gzip,deflate',
    #    'Content-Type':'application/x-www-form-urlencoded',
    #    'Origin':'http://rd2.zhaopin.com',
    #    'Referer':'http://rd2.zhaopin.com/portal/myrd/regnew.asp?za=2',
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
        
        #P = re.findall(r'<h1 class="title">(.*?)</h1>.*?<h2 class="sub-title">(.*?)</h2>.*?<span class="price-display"><em>&#165;</em>(.*?)</span>', shopcontent, re.S)
        #print "Stores_Name:", Stores_Name[0]

        
        #Customers_species = re.findall(r'<h1 class="title">(.*?)</h1>', shopcontent, re.S)
        #print "Customers_species:", Customers_species[0]
        #print type(Customers_species[0])

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
    
