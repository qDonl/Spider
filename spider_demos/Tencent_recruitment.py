from lxml import etree
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
}
BASE_DOMAIN = "https://hr.tencent.com/"

def get_detail_url(url):
    # 从主页面抓取招聘信息页面
    response = requests.get(url, headers=HEADERS)
    text = response.content
    html = etree.HTML(text)
    # 抓取发布时间 并且过滤页面以及jsp链接：a[@target='_blank']
    detail_urls = html.xpath("//table[@class='tablelist']//tr//td//a[@target='_blank']/@href")
    detail_urls = map(lambda url:BASE_DOMAIN+url, detail_urls)
    return detail_urls

def parse_detail_page(url):
    # 分析招聘页面
    try:   # 进行错误处理
        recruit = {}
        response = requests.get(url, headers=HEADERS)
        text = response.content.decode("utf-8")
        html = etree.HTML(text)
        position = html.xpath("//td[@id='sharetitle']/text()")[0]
        recruit["position"] = position

        address = html.xpath("//tr[@class='c bottomline']/td[1]/text()")[0]
        recruit["address"] = address

        category = html.xpath("//tr[@class='c bottomline']/td[2]/text()")[0]
        recruit["category"] = category

        nums = html.xpath("//tr[@class='c bottomline']/td[3]/text()")[0]
        recruit["nums"] = nums

        duty = html.xpath("//ul[@class='squareli']")[0]
        operating_duty = duty.xpath(".//li/text()")
        recruit["operating_duty"] = operating_duty

        requ = html.xpath("//ul[@class='squareli']")[1]
        requirement = requ.xpath(".//li/text()")
        recruit["requirement"] = requirement
    except:
        pass

    return recruit

def get_pubtime(url):
    # 获取招聘发布时间
    try:
        response = requests.get(url, headers=HEADERS)
        text = response.content.decode("utf-8")
        html = etree.HTML(text)
        pubtimes = html.xpath("//table[@class='tablelist']//tr[@class != 'h']/td[5]/text()")
    except:
        pass
    return pubtimes


def spider():
    # 爬取页面
    base_url = "https://hr.tencent.com/position.php?lid=&tid=&keywords=python&start={}0"
    for x in range(20):
        # 循环主页
        recruits = []
        url = base_url.format(x)
        detail_urls = get_detail_url(url)
        for index, detail_url in enumerate(detail_urls):
            # 循环从主页得到的详细页面
            recruit = parse_detail_page(detail_url)
            pubtimes = get_pubtime(url)
            recruit["pubtime"] = pubtimes[index]
            recruits.append(recruit)
        print(recruits)


if __name__ == "__main__":
    spider()
