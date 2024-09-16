import requests
from bs4 import BeautifulSoup

# 构造请求头、get网页源码
MyHeaders={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0"
}
num = 0
for i in range(0, 250, 25):
    response = requests.get("https://movie.douban.com/top250?start={}&filter=".format(i), headers=MyHeaders)
    # 处理源码
    if response.ok:
        content = response.text
        soup = BeautifulSoup(content, "html.parser")
        titles = soup.findAll("span", {"class": "title"})
        with open("./test.txt", "a+", encoding="utf-8") as f:        
            for title in titles:
                if '/' not in title.string:
                    num += 1
                    # print("电影号{}: ".format(num),title.string)
                    txt = "电影号{}: ".format(num) + title.string + "\n"
                    f.write(txt)
    else:
        print('the method of get Failed!/n')

response.close()