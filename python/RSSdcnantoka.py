import urllib
from bs4 import BeautifulSoup
from datetime import datetime

html = urllib.urlopen('http://f.hatena.ne.jp/yohei-a/rss')
soup = BeautifulSoup(html, "html.parser")
ts_list = []

for item in soup.find_all("dc:date"):
	ts_str = item.contents[0]
	ts_date = datetime.strptime(ts_str[0:18], '%Y-%m-%dT%H:%M:%S')
	ts_list.append(ts_date)

print(ts_list)