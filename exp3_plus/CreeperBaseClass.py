#exp3
# 为爬取所有内容做准备
'''
编写Python代码，遍历某个特定的包含多个链接的网页中的所有链接，
并获取这些链接的标题或基本信息，并学习如何遍历网页中的链接，
并获取这些链接的标题或基本信息。
'''
# 老爬虫
from bs4 import BeautifulSoup
import requests
import re
import pymysql


def regUrl(url, getDomain=False):
    url = re.sub(r"^(https?:)/", r"\1//", url) # 处理单/
    IsProtocol = re.match(r"(https?://)", url)
    Protocol = IsProtocol.group(1) if IsProtocol else ""
    Domains = re.findall(r"([a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})", url)
    if len(Domains) >= 2:
        if Domains[-1].count('.') == 1: # index.html
            Domain = Domains[-2]
        else:
            Domain = Domains[-1]
    elif len(Domains) == 1:
        Domain = Domains[0]
    else:
        Domain = ""
    if getDomain:
        FinalUrl = Protocol + Domain + "/"
        return FinalUrl
    Path = "/"
    if Domain:
        AtPathStart = url.rfind(Domain) + len(Domain) # 最后开始找
        Paths = list(filter(None, url[AtPathStart:].split("/"))) # 规范///////情况
        Path += '/'.join(Paths)
    FinalUrl = Protocol + Domain + Path
    return FinalUrl
# Url'规范'操作
def doUrl(urllist):
    if isinstance(urllist, list):    
        FinalUrllist = []
        for url in urllist:
            FinalUrl = regUrl(url)
            FinalUrllist.append(FinalUrl)
        return FinalUrllist
    elif isinstance(urllist, str):
        return regUrl(urllist, getDomain=True)
# 生成表名
def tableName(url):
    turl = regUrl(url, getDomain=True)
    pattern = r'https?://www\.(.*?)\.[a-zA-Z]{2,}'
    match = re.search(pattern, url)
    if match:
        subdomain = match.group(1)
        return subdomain
    else:
        return None
# 处理非转义字符、除去无关引号'
def doUnicode(datalist):
    pattern = r'(.*?)\\u[0-9a-fA-F]{4}'
    result = []
    for data in datalist:
        tstring = repr(data)
        if re.search(pattern, tstring):
            result.append(re.search(pattern, tstring).group(1).replace("'",""))
        else:
            result.append(tstring.replace("'",""))
    return result
# mariadb操作
def connectDb():
    try:
        db = pymysql.connect(
            host="192.168.1.129",
            user="root",
            password="root",
            charset="utf8",
            database="py_creeper0",
            port=3306
        )
        print("——————————数据库连接成功")
        return db
    except Exception as e:
        print(f"—————————数据库连接失败：{e}")
    return None
def operateDb(data, tableName): 
    db = connectDb()  
    cursor = db.cursor()
    sql1 = (
        f"CREATE TABLE IF NOT EXISTS {tableName} ("
        "id INT AUTO_INCREMENT PRIMARY KEY,"
        "info VARCHAR(255),"
        "link VARCHAR(255));"
    )    
    try:
        cursor.execute(sql1)
        db.commit()
        print("————————————建表成功")
        oncesize = 1000
        keys = list(data.keys())
        values = list(data.values())
        print("————————————————data is ", data)
        for i in range(0, len(keys), oncesize):
            tkeys = keys[i:i+oncesize]
            tvalues = values[i:i+oncesize]
            sql2 = f"INSERT INTO {tableName} (info, link) VALUES (%s, %s)"
            params = [(info, url) for info, url in zip(tkeys, tvalues)]
            cursor.executemany(sql2, params)
            db.commit()
            print(f"————————————插入数据成功，第{i // oncesize + 1}批")
    except Exception as e:
        db.rollback()
        print(f"————————————建表或插入数据出错：{e}")
    finally:
        db.close()
    

class CreeperBase:
    def __init__(self, url):
        self.url = regUrl(url)
        self.domain = doUrl(self.url)
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0'
        }
        # self.proxies = {
        #     "http": "http://127.0.0.1:7890",
        #     "https": "https://127.0.0.1:7890"
        # }
        self.response = requests.get(url, headers=self.headers)
        if self.response.ok:
            self.soup = BeautifulSoup(self.response.content.decode('utf-8'), 'html.parser')
            self.title = tableName(self.url)
            self.response.close()
        else:
            print("——————————爬虫请求失败!")
            self.response.close()
            raise Exception(">>>>>>>爬虫请求失败!及时止损!<<<<<<<<")
    def matchKeyWordTag(self, keyword):
        contents =self.soup.find_all(string=keyword)
        if (len(contents)>0):
            for content in contents:
                print(content.parent)
            return contents
        else:
            print("——————————没有找到关键字"+keyword)
            return None
    def getAllLinks(self):
        tempLinks = self.soup.find_all("a")
        if (len(tempLinks) == 0):
            print("——————————没有找到任何链接")
            return None
        else:
            Links = {}
            pattern = r'.*[/.].*'
            for tlink in tempLinks:
                if len(tlink.getText()) == 0 or tlink.getText() is None or tlink.get("href") is None:
                    continue
                elif not re.search(pattern, tlink.get("href")):
                    continue # 出现javascript:void 0类似物
                elif 'gov' in tlink.get("href") or 'edu' in tlink.get("href"):
                    continue # gov、edu：你好
                elif '关于我们' in tlink.getText():
                    break
                else:
                    Links[tlink.getText().strip().replace('\n', '')] = tlink.get("href")
            return Links
#‘干净’的 子链接
    def getAllSubLinks(self):
        tLinks = self.getAllLinks()
        reLinks = dict(zip(doUnicode(tLinks.keys()), tLinks.values()))
        if tLinks is not None:
            Links = reLinks.copy() # 之前操作的原字典
            for linkkey, linkvalue in zip(reLinks.keys(), reLinks.values()):
                    Links[linkkey] = self.domain + linkvalue
            Links = dict(zip(Links.keys(), doUrl(list(Links.values()))))
            #反向字典去重 ####必须加分
            FinalLinks = {}
            for linkkey, linkvalue in zip(Links.keys(), Links.values()):
                FinalLinks[linkvalue] = linkkey
            self.info = FinalLinks.pop(self.url, '')
            return FinalLinks
        else:
            return None


if __name__ == '__main__':
    url = "https://www.runoob.com/"
    url1 = "https://www.maoyan.com/"
    url2 = "https://www.runoob.com/w3cnote"
    url3 = "https://www.runoob.com/w3cnote/w3cnote/hadoop-tutorial.html"
    movie = CreeperBase(url)
    print(movie.getAllSubLinks())

