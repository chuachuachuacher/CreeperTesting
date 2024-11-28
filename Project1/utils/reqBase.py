import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class reqBase:
    def __init__(self, url):
        ua = UserAgent()
        # ua = UserAgent(path=r'E:\Project\python\python3\creeper\utils\fake_useragent.json')
        # cache=False不缓存数据 verify_ssl=False忽略ssl验证 use_cache_server=False禁用服务器缓存
        self.url = url
        self.headers = {
            'User-Agent':ua.random
        }
        self.response = requests.get(url, headers=self.headers)
        if self.response.ok:
            print("——————————爬虫请求成功!")
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            self.response.close()
        else:
            print("——————————爬虫请求失败!")
            self.soup = None
            self.response.close()
    def __del__(self):
        print("——————————连接关闭，爬回去了————————")
        self.response.close()

if __name__ == '__main__':
    # ua = UserAgent(path=r'E:\Project\python\python3\creeper\utils\fake_useragent.json')
    ua = UserAgent()
    print(ua.random)