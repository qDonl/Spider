"""
    使用 selenium 爬取拉勾网动态网页，mongodb
    mongodb: zhihu.position
"""
from selenium import webdriver
from lxml import etree
import re
import time
import pymongo


class LagouSpider(object):

    def __init__(self):
        self.url = 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
        self.driver = webdriver.Chrome(executable_path='E:\chromedriver\chromedriver.exe')

    def run(self):
        self.driver.get(self.url)  # 进入主页面
        while True:
            source = self.driver.page_source
            self.parse_url_page(source)
            self.driver.get(self.url)
            time.sleep(3)
            next_btn = self.driver.find_element_by_class_name('pager_next ')
            if 'pager_next pager_next_disabled' in next_btn.get_attribute('class'):
                break
            else:
                next_btn.click()

    def parse_url_page(self, source):
        """获取主页面所有详情页面的url"""
        html = etree.HTML(source)
        links = html.xpath("//a[@class='position_link']/@href")
        for link in links:
            self.request_detail_page(link)
            time.sleep(1)

    def request_detail_page(self, link):
        """进入详情页面 source"""
        self.driver.get(link)
        source = self.driver.page_source
        self.spider_info(source)

    def spider_info(self, source):
        """爬取详细页面, 详细信息"""
        position = re.findall(r'<span class="name">(.*?)</span>', source, re.DOTALL)[0]
        salary_tag = re.findall(r'<span class="salary">(.*?)</span>', source, re.DOTALL)[0]
        salary = re.sub(' ', '', salary_tag)
        company_name = re.findall(r'<h2 class="fl">(.*?)<i .*?></i>', source, re.DOTALL)[0].strip()
        city_tag = re.findall(r'<span class="salary">.*?</span>.*?<span>(.*?)</span>', source, re.DOTALL)[0]
        city = re.sub(r'/| ', '', city_tag)
        work_years_tag = re.findall(r'<span class="salary">.*?</span>.*?<span>.*?</span>.*?<span>(.*?)</span>', source, re.DOTALL)[0]
        work_years = re.sub(' |/', '', work_years_tag)

        advantage = re.findall(r'<span class="advantage">.*?<p>(.*?)</p>', source, re.DOTALL)[0]
        desc = re.findall(r'<h3 class="description">.*?</h3>.*?<div>(.*?)</div>', source, re.DOTALL)[0]
        description = re.sub(r'<.*?>|( |\n)', '', desc)

        job = {
            'position': position,
            'salary':salary,
            'company_name': company_name,
            'city': city,
            'work_years': work_years,
            'advantage': advantage,
            'description': description,
        }
        write_mongodb(job)
        print('成功写入一条数据')


def write_mongodb(job):
    client = pymongo.MongoClient('127.0.0.1', port=27017)

    db = client.zhihu
    collection = db.position
    collection.insert(job)


if __name__ == '__main__':
    spider = LagouSpider()
    spider.run()













