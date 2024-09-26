#exp2
'''
利用BeautifulSoup解析工具，
解析并提取任一小说网站中某一长篇小说的内容，
并按章节存储
'''

import requests
from bs4 import BeautifulSoup, NavigableString
import re

# 网址
MyHeader = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0"
}

def main():
    NovelUrl = setNovel()
    ChapterList = getNovelInfo(NovelUrl)
    getChapterContent(ChapterList)
    TxtToMarkdown('./creeper/Output.txt', './creeper/output.md')


# 转 markdown
def TxtToMarkdown(input_file, output_file):  
    with open(input_file, 'r', encoding='utf-8') as infile:  
        lines = infile.readlines()  
    markdown_content = []  
    if lines:  
        markdown_content.append('# ' + lines[0].strip())  
        lines = lines[1:]
    in_list = False  
    for line in lines:  
        stripped_line = line.strip()  
        if stripped_line.startswith('- '):  
            markdown_content.append(stripped_line[2:] + '\n')  
            in_list = True  
        elif in_list and not stripped_line.startswith('- '):  
            in_list = False  
        else:  
            markdown_content.append(line)  
    with open(output_file, 'w', encoding='utf-8') as outfile:  
        outfile.writelines(markdown_content) 

# 获取内容
def getChapterContent(clist):
    if clist is None:
        print("————————get 失败！！！！！！")
        return None
    else:
        ChapterNum = int(input("输入你想要阅读的章节编号："))
        if 1 <= ChapterNum <= len(clist):
            ChapterUrl = clist[-1] + clist[ChapterNum-1]
            print("章节链接：", ChapterUrl)
            response = requests.get(ChapterUrl, headers=MyHeader)
            response.encoding = "utf-8"
            if response.ok:
                ChapterSoup = BeautifulSoup(response.text, "html.parser")
                response.close()
                ContentBody = ChapterSoup.body.find("div", attrs={"class": "text"})
                Contents = ContentBody.contents
                print("\n章节topic：{}".format(Contents[2].getText().strip()))
                ln = 0
                for div_ in ContentBody.find_all("div"):
                    if div_.find("img", src="../../../skin/default/image/4.jpg"):
                        break
                    ln+=1
                # print("长度：", ln)
                if ln >= 3:
                    for content in Contents:
                        if content.name == "div" and content.find("img", src="../../../skin/default/image/4.jpg"):
                            break
                        if content.getText().strip() == "\u00A0"*len(content.getText().strip()): #'\u00A0' 是 &nbsp;
                            continue
                        if content.find("sup"):
                            if isinstance(content, NavigableString):# 判断非tag纯文本
                                continue
                            else:
                                DiffText = []
                                DiffList = content.find_all("sup")
                                FinalText = content.getText().strip()
                                for diff in DiffList:
                                    DiffText.append(diff.getText().strip())
                                for diff in DiffText:
                                    FinalText = FinalText.replace(diff, "")
                                # print(FinalText)
                                with open("./creeper/Output.txt", 'a+', encoding='UTF-8') as f:
                                    f.write(FinalText)
                        else:
                            print(content.getText().strip())
                else:
                    for content in Contents:
                        if content == Contents[2]:
                            continue
                        if isinstance(content, NavigableString):
                            # print(content.getText().strip(), end="")
                            text = content.getText().strip()
                            with open("./creeper/Output.txt", 'a+', encoding='UTF-8') as f:
                                f.write(text)
                print("\n章节内容已写入文件：Output.md")
        else:
            print("章节编号超出范围！")

# 确定章节
def getNovelInfo(SubUrl):
    LinkList = [] #LinkList[0] diff章节链接差值   
    ListUrl = "http://novel.tingroom.com/{}/list.html".format(SubUrl)
    response = requests.get(ListUrl, headers=MyHeader)
    response.encoding = "utf-8"
    if response.ok:
        ListSoup = BeautifulSoup(response.text, "html.parser")
        response.close()
        # 小说名
        NovelName = ListSoup.find("div", attrs={"class":"title"}).getText()
        print("书名：", NovelName)

        # 章节列表
        Chapters = ListSoup.find("ol", attrs={"class":"clearfix"}).find_all("li")
        print("章节数：", len(Chapters))
        for chapter, Pnum in zip(Chapters, range(1, len(Chapters)+1)):
            print("章节{}：".format(Pnum), chapter.find("a").getText())
            LinkList.append(chapter.find("a").get("href"))
        last = ListUrl.rsplit("list.html", 1)
        LinkList.append(last[0]) # 定位文章
        return LinkList
    else:
        print("————————get 失败！！！！！！")
        return None

# 指定小说
def setNovel():
    print("大学了，想看什么类型小说？")
    TypeList = {"经典小说":"jingdian", "双语小说":"shuangyu", "名人传记":"mingren"} # going on...
    print("!!!!!!")
    for key, value in TypeList.items():
        print(key, ":", value)
    print("!!!!!!")
    str = input("请输入小说类型：【Key】")
    NovelRankUrl = "http://novel.tingroom.com/{}/".format(str)
    response = requests.get(NovelRankUrl, headers=MyHeader)
    response.encoding = "utf-8"
    LinkList = []
    if response.ok:
        TypeListSoup = BeautifulSoup(response.text, "html.parser")
        response.close()
        print("\n仅列出前五小说")
        TypeNovels = TypeListSoup.find_all("h6", attrs={"class":"yuyu"})
        for novel, num in zip(TypeNovels[:5], range(1, 6)):
            print("小说名：【编号{}】".format(num), novel.find("a").getText())
            LinkList.append(novel.find("a").get("href"))
        # return LinkList
        NovelNum = int(input("输入你想要的小说编号：【1、2、3、4、5】："))
        return LinkList[NovelNum-1]
    else:
        print("————————get 失败！！！！！！")
    return None


# 处理章节链接    1219 04 .html
def reChapterLink(clink):
    match = re.search(r'(\d{2})(?=\.html$)', clink)
    if match:  
        return match.group(1)  
    else:  
        return None


main()

