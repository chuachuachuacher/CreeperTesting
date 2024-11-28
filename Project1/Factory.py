from CreeperBaseClass import OldCreeper, YoungCreeper, TicketCreeper
from utils.download_image import download_image
# from utils.DataBase import Database
from utils.ezdb import Database
from utils.tool import getLocalImagePath


import aiohttp
import asyncio

import time


config = {
        'host': '192.168.150.20',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'db': 'Creepers',
        'charset': 'utf8mb4',
        'autocommit': True,
        'maxsize': 10,
        'minsize': 1,
    }



class CreeperFactory:
    def __init__(self, urls):
        self.urls = urls # 0热映影片、1经典影片
        self.ClassicMovies = {} # {"movieTitle": [movieUrl, movieImageUrl, movieType]} 点击进去 {"movieName": [movieEname, movieInfo, movieImageUrl, movieAbout]} 
        self.ClassicMoviesDetails = {} # 
        self.HotMovies = {} # {movieTitle: [movieUrl, movieImageUrl, movieType]} 点进去 {"movieName": [movieEname, movieInfo, movieImageUrl, movieAbout]} 
        self.HotMoviesDetails = {} # 
        # 临时表（点击才生成）{movieTitle: [cinemaName, cinemaAddress, cinemaDistance]}
    # 并发操作
    async def crawlClassicMovies(self):
    # def crawClassicMovies(self): 
        # 爬取经典电影的所有页数
        Classic = OldCreeper(self.urls[1])
        while True:
            TMovies = Classic.getOnlineMovies()
            self.ClassicMovies.update(TMovies)
            if not Classic.isPagesDone():
                break
            Classic = OldCreeper(Classic.isPagesDone())# 启用一次爬虫

        ClassicMoviesNames = list(self.ClassicMovies.keys())
        ClassicMoviesUrls = [self.ClassicMovies[name][0] for name in ClassicMoviesNames]
        ClassicMoviesImageUrls = [self.ClassicMovies[name][1] for name in ClassicMoviesNames]
        ClassicMoviesTypes = [self.ClassicMovies[name][2] for name in ClassicMoviesNames]
        
        
        # '''
        # 并发下载图片
        async with aiohttp.ClientSession() as session:
            tasks = [download_image(session, url, name, type=0) for url, name in zip(ClassicMoviesImageUrls, ClassicMoviesNames)]
            await asyncio.gather(*tasks)
        # '''
        
        sql0 = "create table if not exists ClassicMovies (id int primary key auto_increment, name varchar(255), type varchar(255), simage BLOB)"
        sql1 = "insert into ClassicMovies (name, type, simage) values(%s, %s, %s)"
        # id info about image
        sql2 = "create table if not exists ClassicMoviesDetails (id int primary key auto_increment, ename varchar(255), info varchar(255), about varchar(255), bimage LONGBLOB)"
        sql3 = "insert into ClassicMoviesDetails (info, ename, about, bimage) values(%s, %s, %s, %s)"
        
        db = Database(config)
        db.execute(sql0)
        for name, type_ in zip(ClassicMoviesNames, ClassicMoviesTypes):
            imgPath = getLocalImagePath(name=name, type='classics')
            if imgPath is None:
                print(f"未能获取到图片路径: {name}")
            else:
                try:
                    with open(imgPath, 'rb') as f:
                        img = f.read()
                        db.execute(sql1, (name, type_, img))
                except IOError as e:
                    print(f"无法读取图片文件 {imgPath}: {e}")
        print("存入成功")
        
        # 单线程 将本地数据存储到数据库
        # ClassicMovies 表 id name type simage ClassicMoviesDetails 表 id name info about bimage
        # HotMovies 表 id name type simage HotMoviesDetails 表 id name info about bimage
        # id name type simage
 
        # 爬取经典电影的所有详情页 mod 30
        # Urls15 = ClassicMoviesUrls[:15]
        # ClassicDetail = YoungCreeper(Urls15)
        ClassicDetail = YoungCreeper(ClassicMoviesUrls)
        self.ClassicMoviesDetails = ClassicDetail.getDetailMovies()
        ClassicMoviesDNames = list(self.ClassicMoviesDetails.keys())
        ClassicMoviesDEnames = [self.ClassicMoviesDetails[name][0] for name in ClassicMoviesDNames]
        ClassicMoviesDInfos = [self.ClassicMoviesDetails[name][1] for name in ClassicMoviesDNames]      
        ClassicMoviesDImageUrls = [self.ClassicMoviesDetails[name][2] for name in ClassicMoviesDNames]
        ClassicMoviesDAbouts = [self.ClassicMoviesDetails[name][3] for name in ClassicMoviesDNames]
        ClassicMoviesDTiketUrls = [self.ClassicMoviesDetails[name][4] for name in ClassicMoviesDNames]
        # print("测试，英文电影名：", ClassicMoviesDEnames)
        # print(len(ClassicDetail.DelayUrls),"这么多访问失败")
        # 并发下载高清图片
        async with aiohttp.ClientSession() as session:
            tasks = [download_image(session, url, name, type=1) for url, name in zip(ClassicMoviesDImageUrls, ClassicMoviesDNames)]
            await asyncio.gather(*tasks)
        
        db = Database(config)
        db.execute(sql2)
        for name , ename, info, about in zip(ClassicMoviesDNames, ClassicMoviesDEnames, ClassicMoviesDInfos, ClassicMoviesDAbouts):
            imgPath = getLocalImagePath(name=name, type='classicb')
            if imgPath is None:
                print(f"未能获取到图片路径: {name}")
            else:
                try:
                    with open(imgPath, 'rb') as f:
                        img = f.read()
                        db.execute(sql3, (ename, info, about, img))
                except IOError as e:
                    print(f"无法读取图片文件 {imgPath}: {e}")
        
        time.sleep(10)
        
        '''
        Hot = OldCreeper(self.urls[0])
        while True:
            TMovies = Hot.getOnlineMovies()
            self.HotMovies.update(TMovies)
            if not Hot.isPagesDone():
                break
            Hot = OldCreeper(Hot.isPagesDone())# 启用一次爬虫

        HotMoviesNames = list(self.HotMovies.keys())
        HotMoviesUrls = [self.HotMovies[name][0] for name in HotMoviesNames]
        HotMoviesImageUrls = [self.HotMovies[name][1] for name in HotMoviesNames]
        HotMoviesTypes = [self.HotMovies[name][2] for name in HotMoviesNames]
        
        
        
        # 并发下载图片
        async with aiohttp.ClientSession() as session:
            tasks = [download_image(session, url, name, type=0) for url, name in zip(HotMoviesImageUrls, HotMoviesNames)]
            await asyncio.gather(*tasks)
        
        sql4 = "create table if not exists HotMovies (id int primary key auto_increment, name varchar(255), type varchar(255), simage BLOB)"
        sql5 = "insert into HotMovies (name, type, simage) values(%s, %s, %s)"
        # id info about image
        sql6 = "create table if not exists HotMoviesDetails (id int primary key auto_increment, ename varchar(255), info varchar(255), about varchar(255), bimage LONGBLOB, ticketUrl varchar(255))"
        sql7 = "insert into HotMoviesDetails (info, ename, about, bimage, ticketUrl) values(%s, %s, %s, %s, %s)"
        
        db = Database(config)
        db.execute(sql4)
        for name, type_ in zip(HotMoviesNames, HotMoviesTypes):
            imgPath = getLocalImagePath(name=name, type='hots')
            if imgPath is None:
                print(f"未能获取到图片路径: {name}")
            else:
                try:
                    with open(imgPath, 'rb') as f:
                        img = f.read()
                        db.execute(sql5, (name, type_, img))
                except IOError as e:
                    print(f"无法读取图片文件 {imgPath}: {e}")
        print("存入成功")
        
        HotDetail = YoungCreeper(HotMoviesUrls)
        self.HotMoviesDetails = HotDetail.getDetailMovies()
        HotMoviesDNames = list(self.HotMoviesDetails.keys())
        HotMoviesDEnames = [self.HotMoviesDetails[name][0] for name in HotMoviesDNames]
        HotMoviesDInfos = [self.HotMoviesDetails[name][1] for name in HotMoviesDNames]      
        HotMoviesDImageUrls = [self.HotMoviesDetails[name][2] for name in HotMoviesDNames]
        HotMoviesDAbouts = [self.HotMoviesDetails[name][3] for name in HotMoviesDNames]
        HotMoviesDTiketUrls = [self.HotMoviesDetails[name][4] for name in HotMoviesDNames]
        # 并发下载高清图片
        async with aiohttp.ClientSession() as session:
            tasks = [download_image(session, url, name, type=3) for url, name in zip(HotMoviesDImageUrls, HotMoviesDNames)]
            await asyncio.gather(*tasks)
        
        db = Database(config)
        db.execute(sql6)
        for name , ename, info, about, turl in zip(HotMoviesDNames, HotMoviesDEnames, HotMoviesDInfos, HotMoviesDAbouts, HotMoviesDTiketUrls):
            imgPath = getLocalImagePath(name=name, type='classicb')
            if imgPath is None:
                print(f"未能获取到图片路径: {name}")
            else:
                try:
                    with open(imgPath, 'rb') as f:
                        img = f.read()
                        db.execute(sql7, (ename, info, about, img, turl))
                except IOError as e:
                    print(f"无法读取图片文件 {imgPath}: {e}")
        '''
        
        
        
def main():
    F = CreeperFactory(['https://maoyan.com/films?type=1', 'https://maoyan.com/films?showType=3'])
    starttime = time.time()
    # '''
    async def run():
        await F.crawlClassicMovies()
        
    asyncio.run(run())
    
    endtime = time.time()
    print("爬取经典电影详情页共耗时：", endtime - starttime, "秒")
    # '''
    # F.crawClassicMovies()
if __name__ == '__main__':
    # asyncio.run(main())
    main()