from bs4 import BeautifulSoup
import requests
from pyecharts import Bar

ALL_DATA = []

def parse_page(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    text = response.content.decode("utf-8")
    soup = BeautifulSoup(text, "html5lib")

    conMidtab = soup.find('div', class_='conMidtab')
    tables = conMidtab.find_all("table")
    for table in tables:
        trs = table.find_all("tr")[2:]
        for index, tr in enumerate(trs):
            tds = tr.find_all("td")
            if index == 0:
                city_td = tds[1]
            else:
                city_td = tds[0]

            temp_td = tds[-5]

            city = list(city_td.stripped_strings)[0]
            temp = list(temp_td.stripped_strings)[0]
            ALL_DATA.append({"city": city, "temp":int(temp)})


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
    message = input("1.从最高温排序；2.从最低排序:")
    if message == '1':
        ALL_DATA.sort(key=lambda data: data['temp'], reverse=True)
    elif message == '2':
        ALL_DATA.sort(key=lambda data: data['temp'])
    data = ALL_DATA[0:10]

    cities = list(map(lambda x:x['city'], data))
    temps = list(map(lambda x: x['temp'], data))

    chart = Bar("中国气温排行榜")
    chart.add('', cities, temps)
    chart.render("Temperature.html")



if __name__ == '__main__':
    main()
