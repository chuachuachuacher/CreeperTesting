# 实验一
'''
利用requests库和正则表达式，
提取百度贴吧某一热门帖(回帖数量不小于200)
的发帖人、发帖时间、发帖内容、楼层数、点赞数等信息，
并将提取的数据保存到本地文件或打印出来。
'''

import requests
from bs4 import BeautifulSoup
import re

MyHeader = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0"
}

#判断l_pager pager_theme_4 pb_list_pager
response = requests.get("https://tieba.baidu.com/p/9109361647", headers=MyHeader)
response.encoding = 'utf-8'

if response.ok:
    Soup = BeautifulSoup(response.text, "html.parser")
    pages = Soup.find("ul", attrs={"class":"l_posts_num"}).find("li", attrs={"class":"l_pager pager_theme_4 pb_list_pager"}).find_all("a")
    pageNum = 0
    for page in pages:
        if page.get_text() != "下一页":
            pageNum = int(page.get_text())
    # print("总页数：", pageNum)


for i in range(pageNum): #手动调 XXXXX 自动调
    MyResponse = requests.get('https://tieba.baidu.com/p/9109361647?pn={}'.format(i+1), headers=MyHeader)
    MyResponse.encoding = 'utf-8'
    if MyResponse.ok:
        print("______请求成功______\n")
        with open("./test_ex{}.html".format(i+1), "w", encoding="utf-8") as f:
            f.write(MyResponse.text)        
        

FloorNum = 1
for i in range(pageNum): # 手动
    with open("./page_{}.html".format(i+1), "r", encoding="utf-8") as f:
        MyContent = f.read()
        Soup = BeautifulSoup(MyContent, "html.parser")
        with open("./Output.txt", "a+", encoding="utf-8") as fo:
            if i == 0:
                TopicTitle = Soup.find("h3", attrs={"class":"core_title_txt pull-left text-overflow"}).getText()
                LzName_Text = Soup.find("a", attrs={"class":"p_author_name j_user_card"}).getText()
                ReleaseTime_Text = Soup.find_all("span", attrs={"class":"tail-info"})[2].getText() #span class都一样
                ReplyNum_Text = Soup.find("span", attrs={"class":"red"}).getText()
                fo.write("帖子主题：{}\n".format(TopicTitle))
                fo.write("发帖人：{}\t回帖数：{}\t发帖时间：{}\n\n".format(LzName_Text, ReplyNum_Text, ReleaseTime_Text))
            # 定位、提取所有楼层的评论框、master框
            SoupFloorMasters = Soup.find_all("div", attrs={"class":"d_author"})

            SoupFloorContents = Soup.find_all("div", attrs={"class":"d_post_content_main"})
            
            for SoupFloorMaster, SoupFloorContent in zip(SoupFloorMasters, SoupFloorContents):

                # 提取该楼层信息：评论、评论人
                FloorMasterInfo = SoupFloorContent.find("div", attrs={"class":"core_reply_tail clearfix"}).getText().strip()
                FloorMasterInfo = re.sub(r'回复\((\d+)\)收起回复|回复收起回复|回复$',"", FloorMasterInfo)
                fo.write("{}\n".format(FloorMasterInfo))

                FloorMaster = SoupFloorMaster.find("li", attrs={"class":"d_name"}).getText().strip()
                fo.write("楼层评论人：{}\t".format(FloorMaster))

                FloorCommit = SoupFloorContent.find("div", attrs={"class":"d_post_content j_d_post_content"}).getText().strip()
                fo.write("\n评论内容：'''{}'''\n\n".format(FloorCommit))

                FloorNum += 1
print("______数据提取成功______\n前往Output.txt查看数据")