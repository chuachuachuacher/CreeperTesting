import asyncio
import aiohttp
from fake_useragent import UserAgent


def printH():
    print("Hello, world!")


async def download_image(session, url, name="1Name", type=0):
    ua = UserAgent()
    typelist = ["classics", "classicb","hots","hotb"]
    headers = {'User-Agent': ua.random}
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            print("图片请求成功")
            file_path = "E:\\Project\\python\\python3\\creeper\\image\\{0}\\{1}.jpg".format(typelist[type], name)
            with open(file_path, mode='wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            print(f"图片已保存到 {file_path}")
        else:
            print("图片请求失败")
            
# import requests
# from fake_useragent import UserAgent

# def download_image(url, name="1Name", type=0):
#     ua = UserAgent()
#     typelist = ["classic", "hot"]
#     headers = {'User-Agent': ua.random}
#     response = requests.get(url, headers=headers)
    
#     if response.status_code == 200:
#         print("图片请求成功")
#         file_path = f"E:\\Project\\python\\python3\\creeper\\image\\{typelist[type]}\\{name}.jpg"
#         with open(file_path, mode='wb') as f:
#             for chunk in response.iter_content(1024):
#                 f.write(chunk)
#         print(f"图片已保存到 {file_path}")
#     else:
#         print("图片请求失败")

# 使用示例
# download_image('http://example.com/image.jpg', 'image_name', 0)

async def main():
    urls = [
    [
        'https://p0.pipi.cn/basicdata/54ecdedd7a3b127a357a35176a77b037fd81a.jpg?imageView2/1/w/160/h/220', 
        'https://p0.pipi.cn/mediaplus/friday_image_fe/cdf05c5c15d4a19a138d3e278b5bcdce77921.jpg?imageView2/1/w/160/h/220', 
        'https://p0.pipi.cn/mmdb/54ecde92339923b12d807750dae3398ce9cce.jpg?imageView2/1/w/160/h/220', ],
    [
        'https://p0.pipi.cn/basicdata/54ecde517e1ddd3139e19bf8f069b9b675e8a.jpg?imageView2/1/w/160/h/220', 
        'https://p0.pipi.cn/mediaplus/friday_image_fe/cdf05c5c15d77e82bf3cbc5628dd9c676167b.jpg?imageView2/1/w/160/h/220', 
        'https://p0.pipi.cn/mediaplus/friday_image_fe/cdf05c5cf876e3e327160d58e6c15bb72a6c8.jpg?imageView2/1/w/160/h/220',], 
    [    
        'https://p0.pipi.cn/basicdata/54ecde518d3923cf3ecbae50a02a19140f317.jpg?imageView2/1/w/160/h/220', 
        'https://p0.pipi.cn/basicdata/54ecde51c69b1221f0b86030daa4572c09b77.jpg?imageView2/1/w/160/h/220', 
        'https://p0.pipi.cn/mmdb/54ecde9a2c9f2a8ea350c8fc07896e036921c.jpg?imageView2/1/w/160/h/220',], 
    [
        'https://p0.pipi.cn/mediaplus/friday_image_fe/cdf05c5c8d3ea482bf8dd476a6ac2fef0f350.jpg?imageView2/1/w/160/h/220', 
        'https://p0.pipi.cn/basicdata/54ecdedd7a3b127a3521f0f987c60653d884d.jpg?imageView2/1/w/160/h/220'
    ]
    ]
    names = [[
        '好东西', 
        '出走的决心', 
        '蜡笔小新：我们的恐龙日记', 
        ],
        [
        '美人鱼的夏天', 
        '不想和你有遗憾', 
        '戴假发的人', 
        ],
        [
        '今年二十二', 
        '毒液：最后一舞', 
        '风流一代', 
        ],
        [
        '哈利·波特与死亡圣器（上)', 
        '金钱堡垒'
    ]]
    printH()
    
    for i in range(4):
        printH()
        async with aiohttp.ClientSession() as session:
            tasks = [download_image(session, url, name) for url, name in zip(urls[i], names[i])]
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.run_until_complete(asyncio.sleep(1))
        loop.close()
    except RuntimeError as e:
        if str(e) != "Event loop is closed":
            raise