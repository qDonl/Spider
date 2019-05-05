import re, requests
import csv

POEMS = []

def parse_page(url):
	poem = {}
	headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"}
	resp = requests.get(url, headers=headers)
	content = resp.content.decode('utf-8')

	titles = re.findall(r'<b>(.*?)</b>', content, re.DOTALL)
	dynasties = re.findall(r'<p class="source">.*?<a.*?>(.*?)</a>', content, re.DOTALL)
	authors = re.findall(r'<span>：</span><a.*?>(.*?)</a>', content, re.DOTALL)
	verses_tags = re.findall(r'<div class="contson".*?>(.*?)</div>', content, re.DOTALL)

	verses = []
	for verse in verses_tags:
		verse = re.sub(r'(<.*?>|\n)', '', verse)
		verses.append(verse)

	for value in zip(titles, authors, dynasties, verses):
		title, author, dynasty, verse = value
		poem = {'title': title, 'author': author, 'dynasty': dynasty, 'verse': verse}
		POEMS.append(poem)

def main():
	base_url = "https://www.gushiwen.org/default_{}.aspx"
	for page in range(1, 11):
		url = base_url.format(page)
		parse_page(url)

	header = ['title', 'author', 'dynasty', 'verse']

	with open('poems.csv', 'w', encoding='utf-8', newline='') as fp:
		writer = csv.DictWriter(fp, header)
		writer.writeheader()
		writer.writerows(POEMS)

if __name__ == '__main__':
	main()
