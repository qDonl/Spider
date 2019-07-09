import requests
import re

def getHTMLText(url):
	try:
		r = requests.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return ""

def parsePage(ilt, html):
	try:
		plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
		tlt = re.findall(r'\"raw_title"\:\".*?\"', html)
		for i in range(len(plt)):
			price = eval(plt[i].split(':')[1])
			title = eval(tlt[i].split(':')[1])
			ilt.append([price, title])
	except:
		print ("")

def printGoodsList(ilt):
	tplt = "{:4}\t{:8}\t{:16}"
	print (tplt.format("序号", "价格", "商品名称"))
	count = 0
	for g in ilt:
		count += 1
		print (tplt.format(count, g[0], g[1]))

def main():
	goods = '书包'# 搜索栏搜索内容
	depth = 2 #爬取几页
	start_url = 'https://s.taobao.com/search?q=' + goods# 爬取起始页
	infoList = []
	for i in range(depth):
		try:
			url = start_url + '&s=' + str(44*i)
			html = getHTMLText(url)
			parsePage(infoList, html)
		except:
			continue
	printGoodsList(infoList)

main()