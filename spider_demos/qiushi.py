import re, requests

def parse_page(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    text = response.content.decode("utf-8")
    contents = re.findall(r'<div class="content">.*?<span>(.*?)</span>', text, re.DOTALL)
    for content in contents:
        x = re.sub(r'<.*?>|\n', '', content)
        print(x.strip())
        print("===="*20)

def main():
    base_url = "https://www.qiushibaike.com/text/page/{}/"
    for x in range(1, 10):
        url = base_url.format(x)
        parse_page(url)

if __name__ == '__main__':
    main()
