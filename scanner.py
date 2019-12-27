import os
import random
import threading
import urllib
import pymysql.cursors
import requests
from bs4 import BeautifulSoup

#伪装头
my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]

header={"user-Agent":random.choice(my_headers)}

TARGET_URL="http://www.mzitu.com/page/{}"

#获取每一页所有人的信息
def getGirlInfo(html):
    soup=BeautifulSoup(html);
    girl={}
    girlPage=[]  #记录每一页的信息

    liGroup=soup.find('div','postlist').find_all("li")
    for item in liGroup:
        girl['title']=item.find('span').find('a').get_text().strip()
        girl['url']=item.find('span').find('a').get('href').strip()
        girlPage.append(girl)
    return girlPage

#获取网页内容
def getHtml(url):
    try:
        request=urllib.request.Request(url,headers=header)
        page=urllib.request.urlopen(request)
        html=page.read()
        return html
    except Exception as e:
        print(e.args)

#获取每个人的所有照片链接
def getEachGirlInfo(url):
    eachGirl=[]
    html=getHtml(url)
    soup=BeautifulSoup(html);
    totalPageNum = soup.find('div','pagenavi').find_all('a')[-2].find('span').get_text().strip() #记录每个妹子的总页数
    picUrl=soup.find('div','main-image').find('a').find('img').get('src').strip()
    for i in range(1,int(totalPageNum)):
        detailUrl=url+"/{}".format(i)
        eachGirl.append(getPicUrl(detailUrl))
    return eachGirl

#获取每个详细页面的照片链接
def getPicUrl(detailPageUrl):
    html=getHtml(detailPageUrl)
    soup=BeautifulSoup(html);
    picUrl=soup.find('div','main-image').find('a').find('img').get('src').strip()
    return picUrl

def makeDir(path):
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print (path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')
        return False

def download_Pic(title, image_list):    # 新建文件夹
    downloadPath="D:/PyBugs/"+title
    makeDir(downloadPath)
    # 下载图片
    num=1
    for item in image_list:
        try:
            header['Referer']=item
            filename=os.path.join(downloadPath, str(num)+".jpg")
            print(filename)
            # filename = '{}_{}.jpg'.format(downloadPath,num)
            print('downloading....{} : NO.{}'.format(title,num))
            with open(filename, 'wb') as f:
                img = requests.get(item,headers=header).content
                f.write(img)
                num+=1
        except Exception as e:
            print(e)
            pass




for i in range(2,238):
    try:
        html=getHtml(TARGET_URL.format(i))
        girlPage=getGirlInfo(html)
        print(">>>>第{}页:".format(i)+str(girlPage))
        for itemGirl in girlPage:
            image_list=getEachGirlInfo(itemGirl['url'])
            print(str(image_list))
            download_Pic(itemGirl['title'],image_list)
    except Exception as e:
        print(e.args)
        pass


