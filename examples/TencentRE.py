import re, requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
    "Referer": "https://hr.tencent.com/position.php?lid=&tid=&keywords=python"
}
BASE_DOMAIN = "https://hr.tencent.com/"

def get_detail_url(url):
    response = requests.get(url, headers=HEADERS)
    text = response.content.decode("utf-8")

    urls = re.findall(r'<td class="l square">.*?<a target="_blank" href="(.*?)">', text, re.DOTALL)
    detail_urls = list(map(lambda url:BASE_DOMAIN+url, urls))
    return detail_urls

def parse_page(url):
    job = {}
    response = requests.get(url, headers=HEADERS)
    text = response.content.decode("utf-8")

    position = re.findall(r'<tr class="h">.*?<td.*?>(.*?)</td>', text, re.DOTALL)[0]
    job['position'] = position

    base_info = re.findall(r'<td>.*?<span.*?>.*?</span>(.*?)</td>', text, re.DOTALL)
    job['address'] = base_info[0]
    job['category'] = base_info[1]
    job['num'] = base_info[2]

    duty_info = re.findall(r'<ul class="squareli">(.*?)</ul>', text, re.DOTALL)
    duty = re.sub(r'<.*?>', '', duty_info[0]).strip()
    job['duty'] = duty
    requirement = re.sub(r'<.*?>', '', duty_info[1]).strip()
    job['requirement'] = requirement

    return job


def main():
    base_url = "https://hr.tencent.com/position.php?lid=&tid=&keywords=python&start={}0#a"
    for page in range(0, 10):
        jobs = []
        url = base_url.format(page)
        detail_urls = get_detail_url(url)
        for detail_url in detail_urls:
            job = parse_page(detail_url)
            jobs.append(job)
        print(jobs)

if __name__ == '__main__':
    main()
