import requests
from bs4 import BeautifulSoup, NavigableString
import re


class NovelCrawler:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0"
        }
        self.novel_url = ""
        self.chapter_list = []

    def run(self):
        self.novel_url = self.set_novel()
        if self.novel_url:
            self.chapter_list = self.get_novel_info(self.novel_url)
            if self.chapter_list:
                self.get_chapter_content(self.chapter_list)

    def set_novel(self):
        print("大学了，想看什么类型小说？")
        type_list = {
            "经典小说": "jingdian",
            "双语小说": "shuangyu",
            "名人传记": "mingren"
        }
        
        # 展示可选类型
        for key, value in type_list.items():
            print(f"{key} : {value}")

        # 输入小说类型并进行简单验证
        novel_type = input("请输入小说类型：【Key】")
        if novel_type not in type_list.values():
            print("无效的小说类型，请重试。")
            return None

        novel_rank_url = f"http://novel.tingroom.com/{novel_type}/"
        response = self.get_response(novel_rank_url)

        if response:
            return self.select_novel(response)
        else:
            print("————————get 失败！！！！！！")
            return None

    def select_novel(self, response):
        print("\n仅列出前五小说")
        type_novels = response.find_all("h6", attrs={"class": "yuyu"})
        link_list = []

        if not type_novels:
            print("未找到任何小说，请检查类型。")
            return None

        for num, novel in enumerate(type_novels[:5], start=1):
            print(f"小说名：【编号{num}】", novel.find("a").getText())
            link_list.append(novel.find("a").get("href"))

        # 输入小说编号并进行验证
        try:
            novel_num = int(input("输入你想要的小说编号：【1、2、3、4、5】："))
            if 1 <= novel_num <= len(link_list):
                return link_list[novel_num - 1]
            else:
                print("小说编号超出范围，请重试。")
                return None
        except ValueError:
            print("无效的输入，请输入一个数字。")
            return None

    def get_novel_info(self, sub_url):
        list_url = f"http://novel.tingroom.com/{sub_url}/list.html"
        response = self.get_response(list_url)

        if response:
            self.display_novel_info(response)
            return self.extract_chapter_links(response)
        else:
            print("————————get 失败！！！！！！")
            return None

    def get_response(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.encoding = "utf-8"
            if response.ok:
                return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            print(f"请求错误: {e}")
        return None

    def display_novel_info(self, soup):
        novel_name = soup.find("div", attrs={"class": "title"})
        if novel_name:
            print("书名：", novel_name.getText())
        else:
            print("未找到小说名。")
            return

        chapters = soup.find("ol", attrs={"class": "clearfix"})
        if chapters:
            chapter_list = chapters.find_all("li")
            print("章节数：", len(chapter_list))
        else:
            print("未找到章节信息。")

    def extract_chapter_links(self, soup):
        link_list = []
        chapters = soup.find("ol", attrs={"class": "clearfix"}).find_all("li")

        for chapter in chapters:
            link_list.append(chapter.find("a").get("href"))
        if chapters:
            last = chapters[-1].find("a")["href"].rsplit("list.html", 1)
            link_list.append(last[0])  # 定位文章
        return link_list

    def get_chapter_content(self, clist):
        if clist is None:
            print("————————get 失败！！！！！！")
            return
        try:
            chapter_num = int(input("输入你想要阅读的章节编号："))
            if 1 <= chapter_num <= len(clist):
                chapter_url = clist[-1] + clist[chapter_num - 1]
                print("章节链接：", chapter_url)
                response = self.get_response(chapter_url)

                if response:
                    self.parse_chapter_content(response)
            else:
                print("章节编号超出范围！")
        except ValueError:
            print("无效的输入，请输入一个数字。")

    def parse_chapter_content(self, soup):
        content_body = soup.body.find("div", attrs={"class": "text"})
        if content_body:
            contents = content_body.contents
            print("\n章节topic：{}".format(contents[2].getText().strip()))

            for content in contents:
                if isinstance(content, NavigableString):
                    continue
                
                if content.name == "div":
                    self.process_div_content(content)
                else:
                    print(content.getText().strip())
        else:
            print("未找到章节内容。")

    def process_div_content(self, content):
        if content.find("img", src="../../../skin/default/image/4.jpg"):
            return

        if content.getText().strip() == "\u00A0" * len(content.getText().strip()):  # '\u00A0' 是 &nbsp;
            return
        
        final_text = content.getText().strip()
        diff_list = [diff.getText().strip() for diff in content.find_all("sup")]
        for diff in diff_list:
            final_text = final_text.replace(diff, "")
        
        print(final_text)


if __name__ == "__main__":
    crawler = NovelCrawler()
    crawler.run()
