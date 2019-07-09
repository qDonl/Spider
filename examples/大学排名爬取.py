import requests
from bs4 import BeautifulSoup
import bs4

def getHTMLText(url):
	"""从网络上获取大学排名网页信息"""

	try:
		r = requests.get(url, timeout=30)
		r.raise_for_status()# 检测产生异常信息
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return ""

def fillUnivList(ulist, html):
	"""提取网页内容中信息，o找到合适的数据结构"""

	soup = BeautifulSoup(html, 'html.parser')
	for tr in soup.find('tbody').children:# 获取tbody下的children-tr标签
		if isinstance(tr, bs4.element.Tag):# 过滤掉得标签类型的其他信息
			tds = tr('td')
			# 将所有信息都保存在ulist中
			ulist.append([tds[0].string, tds[1].string, tds[3].string])

def printUnivList(ulist, num):
	"""利用数据结构展示并输出结果"""

	tplt = "{0:^10}\t{1:{3}^10}\t{2:^10}"
	print (tplt.format("排名", "学校名称", "总分", chr(12288)))
	for i in range(num):
		u = ulist[i]
		print (tplt.format(u[0], u[1], u[2], chr(12288)))

def main():
	uinfo = []# 存储大学信息
	url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2016.html'
	html = getHTMLText(url)# 将url转换成html
	fillUnivList(uinfo, html)
	printUnivList(uinfo, 25)# 20所大学信息

main()
