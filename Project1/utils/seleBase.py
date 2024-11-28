from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

class seleBase():
    def __init__(self, urls):
        self.urls = urls
        self.soups = [None] * len(urls)
        service = FirefoxService(executable_path="E:\Project\python\python3\geckodriver-v0.35.0-win64\geckodriver.exe")
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        
        profile = webdriver.FirefoxProfile()
        profile.set_preference("permissions.default.image", 2)
        options.profile = profile

        self.driver = webdriver.Firefox(service=service, options=options)
        wait = WebDriverWait(self.driver, 2)
        for url, num in zip(urls, range(len(urls))):
            self.driver.get(url)
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.banner")))
            except TimeoutException:
                self.soups[num] = None
                print(BeautifulSoup(self.driver.page_source, 'html.parser').title.text)
                print("——————————爬虫请求失败！")
            else:
                self.soups[num] = BeautifulSoup(self.driver.page_source, 'html.parser')
                print("——————————爬虫请求成功！")
    def __del__(self):
        self.driver.quit()
        print("——————————关闭爬虫驱动！！！")
        #### 手动del对象
        


if __name__ == '__main__':
    testCreeper = seleBase("https://www.maoyan.com/films/1518897")
    print(testCreeper.soup)