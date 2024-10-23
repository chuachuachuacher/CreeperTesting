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

# tablename'规范'操作
def doName(Sdata):
    if '-' in Sdata:
        index = Sdata.index('-')
        return Sdata[:index].strip()
    if '_' in Sdata:
        index = Sdata.index('_')
        return Sdata[:index].strip()
    return Sdata[:5].strip()
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
        f"CREATE TABLE IF NOT    EXISTS {tableName} ("
        "id INT AUTO_INCREMENT PRIMARY KEY,"
        "info VARCHAR(255),"
        "link VARCHAR(255));"
        )
    sql2 = f"insert into {tableName}(info, link) values "
    for info, url in zip(data.keys(), data.values()):
        sql2 += f"('{info}', '{url}'), "
    sql2 = sql2[:-2] + ";"
    try:
        cursor.execute(sql1)
        db.commit()
        print("————————————建表成功") #
        cursor.execute(sql2)
        db.commit()
        print("————————————插入数据成功")
    except Exception as e:
        db.rollback()
        print(f"————————————建表出错：{e}")
    finally:
        db.close()    

class CreeperBase:
    def __init__(self, url):
        # self.byCreeper = False
        self.url = url
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
        self.response = requests.get(url, headers=self.headers)
        if self.response.ok:
            # time.sleep(10)
            self.soup = BeautifulSoup(self.response.content.decode('utf-8'), 'html.parser')
            self.title = doName(self.soup.find('title').getText().strip().replace(' ', ''))
            self.response.close()
        else:
            print("——————————爬虫请求失败!")
            self.response.close()
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
                if 'http' in linkvalue:
                    del Links[linkkey]
                    continue
                if  linkvalue in self.url:# 子链接肯定不包括自己——self.url
                    del Links[linkkey]
                else:
                    Links[linkkey] = self.url + linkvalue
            return Links
        else:
            return None


if __name__ == '__main__':
    url = "url"
    movie = CreeperBase(url)
    operateDb(movie.getAllSubLinks(), movie.title)
