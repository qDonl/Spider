import re, requests
from pyecharts import Bar

DATAS = []# 将总数据设置为全局变量

def parse_page(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    content = response.content.decode("utf-8")
    cities = re.findall(r'<td width="83" height="23">.*?<a.*?>(.*?)</a>', content, re.DOTALL)
    len_ = int(len(cities)/7)
    cities = cities[0:len_]
    temps = re.findall(r'<td width="86">(\d+?)</td>', content, re.DOTALL)
    temps = temps[0:len_]

    for value in zip(cities, temps):
        city, temp = value
        DATAS.append({'city': city, 'temp': int(temp)})

def main():
    urls = [
        "http://www.weather.com.cn/textFC/hb.shtml",
        "http://www.weather.com.cn/textFC/db.shtml",
        "http://www.weather.com.cn/textFC/hd.shtml",
        "http://www.weather.com.cn/textFC/hz.shtml",
        "http://www.weather.com.cn/textFC/hn.shtml",
        "http://www.weather.com.cn/textFC/xb.shtml",
        "http://www.weather.com.cn/textFC/xn.shtml",
        "http://www.weather.com.cn/textFC/gat.shtml"
    ]
    for url in urls:
        parse_page(url)
    DATAS.sort(key=lambda data: data['temp'])
    data = DATAS[0:10]

    cities = list(map(lambda city: city['city'], data))
    temps = list(map(lambda temp: temp['temp'], data))

    chart = Bar("中国最低气温排行榜")
    chart.add('', cities, temps)
    chart.render("temperature.html")


if __name__ == '__main__':
    main()
