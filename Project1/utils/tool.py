import re
from urllib.parse import urlparse, urlunparse
from fake_useragent import UserAgent
import os



'''
    我的范式URL处理器
'''
def regUrl(url, getDomain=False, finalg=False):  # 开启getDomain 返回主域名 开启finalg Url末尾添加"/"
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
        TUrl = Protocol + Domain
        FinalUrl = TUrl if not finalg else (TUrl + "/")
        return FinalUrl
    Path = "/"
    if Domain:
        AtPathStart = url.rfind(Domain) + len(Domain) # 最后开始找
        Paths = list(filter(None, url[AtPathStart:].split("/"))) # 规范///////情况
        Path += '/'.join(Paths)
    FinalUrl = Protocol + Domain + Path
    return FinalUrl

'''
    去除url参数
'''
def getUrlWithoutParams(url):  # 去除url参数
    purl = urlparse(url)
    return urlunparse((purl.scheme, purl.netloc, purl.path, '', '', ''))

'''
    本地获取图片路径
'''
def getLocalImagePath(name, type):
    path = 'E:\\Project\\python\\python3\\creeper\\image\\{1}\\{0}.jpg'.format(name, type)
    if not os.path.exists(path):  # 检查文件是否存在
        return None
    return path

if __name__ == "__main__":
    url = "https://www.baidu.com/index.html"
    imageurl = "https://p0.pipi.cn/mediaplus/friday_image_fe/cdf05c5c25c4a1ea40e3278b62ed4c81cd1e9.jpg?imageView2/1/w/160/h/220"
    url1 = "https://p0.pipi.cn/mediaplus/friday_image_fe/cdf05c5c25c4a1ea40e3278b62ed4c81cd1e9.jpg?imageView2/1/w/464/h/644"
    print(getLocalImagePath("只此青绿", ""))
    # print(regUrl(imageurl))
    # getImage(imageurl)
    # url2 = "https://www.example.com/path/to/resource?param1=value1&param2=value2"
    # print(getUrlWithoutParams(url2))