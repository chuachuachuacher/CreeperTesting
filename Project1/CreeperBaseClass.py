from utils.tool import regUrl, getUrlWithoutParams  # 后期需要修正
from utils.reqBase import reqBase
from utils.seleBase import seleBase


class OldCreeper(reqBase):
    def __init__(self, url):
        super().__init__(url)
        self.movies = {} # 时间选择
    def getOnlineMovies(self, Presale=False): # 获取正在热映的电影 dd 返回一个字典 {movieTitle:[movieUrl, movieImageUrl, movieType]}
        # Presale 是否预售
        if not self.soup:
            print("——————————爬虫请求失败!")
            return None
        else:
            # print("开始爬取预售电影") #测试
            moviedds = self.soup.find_all('dd') # dd标签即电影简介框
            TagClass1 = r'movie-item film-channel' # 第一个div框
            TagClass11 = r"channel-action channel-action-sale" # 预售标识
            TagClass2 = r"channel-detail movie-item-title" # 电影信息标识
            TagClass12 = r"movie-item-hover" # 
            TagClass121 = r'movie-hover-info'
            TagClass1211 = r'movie-hover-title'
            for moviedd in moviedds:
                moviediv1 = moviedd.find('div', attrs={'class': TagClass1})
                moviediv2 = moviedd.find('div', attrs={'class': TagClass2})
                moviediv13 = moviediv1.find('div', attrs={'class': TagClass12})
                moviediv131 = moviediv13.find('a').find('div', attrs={'class': TagClass121}).find_all('div', attrs={'class': TagClass1211})[1]
                
                movieTitle = moviediv2['title'] # 电影名字 
                movieType = moviediv131.text.strip().replace(" ", "")[4:] # 电影类型 爱情／奇幻／喜剧   爱情／剧情
                # print(f"测试——————————{movieType}")
                movieUrl = regUrl(self.url, getDomain=True, finalg=False) + moviediv2.find('a')['href']
                movieImageUrl = moviediv1.find_all('img')[1]['data-src'] # data-src  0 是水印 这个图片的大小是15k 清晰的是91k
                if moviediv1.find('div', attrs={'class': TagClass11}):
                    self.movies[movieTitle] = [movieUrl, movieImageUrl, movieType]
                if not Presale:
                    self.movies[movieTitle] = [movieUrl, movieImageUrl, movieType]
            return self.movies
    def isPagesDone(self): # 判断是否有下一页, 如果有：返回下一页链接，否则返回None
        TagEnd = self.soup.find('div', attrs={'class': "no-movies"}) # 猫眼网站"没有更多电影"的提示 漏洞点
        if TagEnd:
            return None
        if self.soup.find('ul', attrs={'class':"list-pager"}) is None:
            return None
        pages = self.soup.find('ul', attrs={'class':"list-pager"}).find_all('li')
        if "下一页" == pages[-1].getText().strip():
            params = pages[-1].a['href'].strip()
            return (getUrlWithoutParams(self.url) + params)
        else:
            return None
    def __del__(self):
        super().__del__()       

class YoungCreeper(seleBase):
    def __init__(self, urls):
        super().__init__(urls)
        self.movies = {}
        self.DelayUrls = []
    def getDetailMovies(self): # 获取电影详细信息，清晰的海报图， movies = {moviename:[movieEname, movieInfo, movieImageUrl, movieAbout, movieTicketUrl]}
        DetailMovieDelayUrls = [] 
        for soup, url in zip(self.soups, self.urls):
            if not soup:
                print("——————————某爬虫请求失败!")
                self.DelayUrls.append(url)
                continue
            else:
                banner = soup.body.find('div', attrs={'class': 'banner'})
                movieInfodiv = banner.find('div', attrs={'class': r'wrapper clearfix'})
                movieImagediv = movieInfodiv.find('div', attrs={'class': r'avatar-shadow'})
                movieInfodiv1 = movieInfodiv.find('div', attrs={'class': r'movie-brief-container'})                
                movieBuydiv = movieInfodiv.find('div', attrs={'class': r'celeInfo-right clearfix'}).find('div', attrs={'class': r'action-buyBtn'})
                movieTicket = movieBuydiv.find('a', attrs={'class': r'btn buy'})
                app = soup.body.find('div', attrs={'class': 'container'}).find('div', attrs={'class': r'tab-desc tab-content active'})
                
                movieAbout = app.find_all('div', attrs={'class': r'module'})[0].find('div', attrs={'class':r'mod-content'}).find('span', attrs={'class': 'dra'}).getText()
                movieName = movieInfodiv1.find('h1', attrs={'class': r'name'})
                movieEname = movieInfodiv1.find('div', attrs={'class': r'ename ellipsis'})
                movieInfo = movieInfodiv1.find('ul').getText().strip().replace("\n", "").replace(" ", "")
                movieImageUrl = movieImagediv.find('img')['src']
                if movieTicket is None:
                    self.movies[movieName.text.strip()] = [movieEname.text.strip(), movieInfo, movieImageUrl, movieAbout, None]
                else:
                    movieTicket = movieTicket.get('href').strip()
                    TicketUrl = regUrl(url, getDomain=True, finalg=False) + movieTicket
                    # print("测试，买票链接：", TicketUrl)
                    self.movies[movieName.text.strip()] = [movieEname.text.strip(), movieInfo, movieImageUrl, movieAbout, movieTicket]
        return self.movies

class TicketCreeper(OldCreeper):
    def __init__(self, url):
        super().__init__(url)
        self.cinema = {}
    def getTicketInfo(self): # 获取电影购票页面信息， cinema = {cinemaName:[cinemaAddress, cinemaDistance]}
        if not self.soup:
            print("——————————爬虫请求失败!")
            return None
        else:
            app = self.soup.find('div', attrs={'id':'app'})
            cinemadiv = app.find('div', attrs={'class': 'cinemas-list'})
            cinemacells = cinemadiv.find_all('div', attrs={'class':'cinema-cell'})
            for cinemacell in cinemacells:
                cinemaInfo = cinemacell.find('div', attrs={'class': 'cinema-info'})
                # cinemaPrice = 
                cinemaName = cinemaInfo.find('a', attrs={'class': 'cinema-name'}).getText().replace("\n", "").replace(" ", "").strip()
                cinemaAddress = cinemaInfo.find('p', attrs={'class': 'cinema-address'}).getText()
                cinemaDistance = cinemacell.find('div', attrs={'class':'price'}).find('span', attrs={'class': 'cinema-distance'}).getText()
                self.cinema[cinemaName] = [cinemaAddress, cinemaDistance]
            return self.cinema

   
