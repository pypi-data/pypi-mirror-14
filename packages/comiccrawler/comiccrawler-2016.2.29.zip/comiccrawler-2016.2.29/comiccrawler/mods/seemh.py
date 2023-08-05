#! python3

"""this is seemh module for comiccrawler

Ex:
	http://tw.seemh.com/comic/10924/
	http://www.seemh.com/comic/10924/

"""

import re, execjs

from urllib.parse import urljoin

from ..core import Episode, grabhtml

domain = ["tw.seemh.com", "www.seemh.com"]
name = "看漫畫"

def gettitle(html, url):
	return re.search(r'<h1>([^<]*)', html).group(1)

def get_list(html, cid):
	ep_re = r'href="(/comic/{}/\d+\.html)" title="([^"]+)"'.format(cid)
	arr = []
	try:
		comment_pos = html.index('class="comment-bar"')
	except ValueError:
		comment_pos = len(html)

	for match in re.finditer(ep_re, html):
		if match.start() >= comment_pos:
			break
		ep_url, title = match.groups()
		arr.append((title, ep_url))
	return arr


def getepisodelist(html, url):
	cid = re.search(r"comic/(\d+)", url).group(1)
	episodes = get_list(html, cid)

	if not episodes:
		ep_html = grabhtml(urljoin(url, "/support/chapters.aspx?id=" + cid), referer=url)
		episodes = get_list(ep_html, cid)

	episodes = [Episode(v[0].strip(), urljoin(url, v[1])) for v in episodes]
	return episodes[::-1]

def getimgurls(html, url):
	configjs_url = re.search(
		r'src="(http://[^"]+?/config_\w+?\.js)"',
		html
	).group(1)
	configjs = grabhtml(configjs_url, referer=url)
	crypto = re.search(r"(var CryptoJS.+?)var pVars", configjs, re.S).group(1)

	info_eval = re.search(
		r'<script type="text/javascript">(eval[^<]+)',
		html
	).group(1)

	ctx = execjs.compile(crypto + info_eval)
	files, path = ctx.eval("[cInfo.files, cInfo.path]")

	return ["http://i.seemh.com:88" + path + file for file in files]
