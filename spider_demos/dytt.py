import requests
from lxml import etree

BASE_DOMAIN = "http://www.dytt8.net"
HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",
}

def get_detail_url(url):
    response = requests.get(url, headers=HEADERS)
    text = response.content

    html = etree.HTML(text)
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
    # 将列表 detail_urls中的每一项都执行 BASE_DOMAIN+url
    detail_urls = map(lambda url:BASE_DOMAIN+url, detail_urls)
    return detail_urls

# 解析资源链接页面
def parse_detail_page(url):
    movie = {}
    try:
        respose = requests.get(url, headers=HEADERS)
        text = respose.content.decode('gbk')
        html = etree.HTML(text)
        title = html.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")[0]
        movie['title'] = title

        def parse_info(info, rule):
            # 去除  ◎ 标识 以及 取值左右空格
            return info.replace(rule, '').strip()

        zoomE = html.xpath("//div[@id='Zoom']")[0]
        infos = zoomE.xpath(".//p/text()")
        for index, info in enumerate(infos):
            if info.startswith("◎年　　代"):
                info = parse_info(info, "◎年　　代")
                movie["year"] = info
            elif info.startswith("◎产　　地"):
                info = parse_info(info, "◎产　　地")
                movie['country'] = info
            elif info.startswith("◎类　　别"):
                info = parse_info(info, "◎类　　别")
                movie['category'] = info
            elif info.startswith("◎豆瓣评分"):
                info = parse_info(info, "◎豆瓣评分")
                movie["douban_rating"] = info
            elif info.startswith("◎片　　长"):
                info = parse_info(info, "◎片　　长")
                movie["duratiion"] = info
            elif info.startswith("◎导　　演"):
                info = parse_info(info, "◎导　　演")
                movie["director"] = info
            elif info.startswith("◎主　　演"):
                info = parse_info(info, "◎主　　演")
                actors = [info]
                for x in range(index+1, len(infos)):
                    actor = infos[x].strip()
                    if actor.startswith("◎简　　介"):
                        break
                    actors.append(actor)
                movie['actors'] = actors
            elif info.startswith("◎简　　介"):
                info = parse_info(info, "◎简　　介")
                for x in range(index+1, len(infos)):
                    profile = infos[x].strip()
                    if profile.startswith('◎获奖情况'):
                        break
                    movie['profile'] = profile
        download_url = html.xpath("//td[@bgcolor='#fdfddf']/a/@href")[0]
        movie['download_url'] = download_url
    except:
        pass
    return  movie


# 爬取资源页面
def spider():
    base_url = "http://www.dytt8.net/html/gndy/dyzz/list_23_{}.html"
    for x in range(1, 8):
        movies = []
        #第一个for循环用于遍历整个主页
        url = base_url.format(x)
        detail_urls = get_detail_url(url)

        for detail_url in detail_urls:
            #第二个for循环用于遍历所获取的电影url
            movie = parse_detail_page(detail_url)
            movies.append(movie)
            print(movie)
        print("——————"*20)



if __name__ == "__main__":
    spider()
