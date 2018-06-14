#-*- conding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import os
import json
import shutil
import re

if os.path.exists('qq_music'):
	shutil.rmtree('qq_music')
os.makedirs('qq_music')
s = 0
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',
}
sin = 0
ein = 29
page = 1
while True:
	# 分类歌单页面js文件“fcg_get_diss_by_tag.fcg?”，获取dissid
	headers['referer'] = 'https://y.qq.com/portal/playlist.html'
	url = 'https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg?' \
	      'picmid=1&rnd=0.5680886142129784&g_tk=5381&jsonpCallback=getPlaylist&' \
	      'loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&' \
	      'notice=0&platform=yqq&needNewCode=0&categoryId=10000000&sortId=5&' \
	      'sin={0}&ein={1}'
	try:
		print(sin, ein)
		get_dissid = requests.get(url.format(sin, ein), headers=headers).text
		print(get_dissid)
	except requests.exceptions.Timeout:
		print('请求超时')
	dissid_dic = json.loads(get_dissid.strip('getPlaylist()'))
	sum_music = dissid_dic['data']['sum']
	y = 0
	for i in dissid_dic['data']['list']:
		y += 1
		dissid = i['dissid']
		dissname = i['dissname']
		filename = dissname
		filename = re.sub(r'[?|/*()<>#":]', '', filename).strip()
		os.mkdir('qq_music/'+filename)
		path = 'qq_music/'+filename
		print(path)
		# 歌单页面js文件“fcg_ucc_getcdinfo_byids_cp.fcg?”，获取songmid、strMediaMid
		url_1 = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?' \
		      'type=1&json=1&utf8=1&onlysong=0&disstid={0}&format=jsonp&' \
		      'g_tk=5381&jsonpCallback=playlistinfoCallback&loginUin=0&hostUin=0&' \
		      'format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&' \
		      'needNewCode=0'.format(dissid)
		headers['referer'] = 'https://y.qq.com/n/yqq/playsquare/{0}.html'.format(dissid)
		try:
			get_songmid = requests.get(url_1, headers=headers).text.strip('playlistinfoCallback()')
		except requests.exceptions.Timeout:
			print('请求超时')
		songmid_list = json.loads(get_songmid)
		z = 0
		time.sleep(0.0003)
		for j in songmid_list['cdlist'][0]['songlist']:
			z += 1
			songmid = j['songmid']
			songname = j['songname']
			strMediaMid = j['strMediaMid']

			# 播放页面js文件“fcg_music_express_mobile?”，获取vkey
			url_2 = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?' \
			        'g_tk=5381&jsonpCallback=MusicJsonCallback&' \
			        'loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&' \
			        'notice=0&platform=yqq&needNewCode=0&cid=205361747&' \
			        'callback=MusicJsonCallback&uin=0&' \
			        'songmid={0}&filename=C400{1}.m4a&' \
			        'guid=1716426600'.format(songmid, strMediaMid)
			headers['referer'] = 'https://y.qq.com/portal/player.html'
			try:
				get_vkey = requests.get(url_2, headers=headers).text.strip('MusicJsonCallback()')
			except requests.exceptions.Timeout:
				print('请求超时')
			vkey_list = json.loads(get_vkey)
			#  歌曲下载
			k = vkey_list['data']['items'][0]['vkey']
			url_3 = 'http://dl.stream.qqmusic.qq.com/C400{0}.m4a?' \
			        'vkey={1}&guid=1716426600&uin=0&fromtag=66'.format(strMediaMid, k)
			del headers['referer']
			headers['Host'] = 'dl.stream.qqmusic.qq.com'
			get_music = requests.get(url_3, headers=headers, stream=True).raw.read()
			print(re.sub(r'[?|/*()<>#:"]', '', songname), songname)
			songname = re.sub(r'[?|/*()<>#":]', '', songname)
			with open("{0}/{1}.mp3".format(path, songname), 'wb') as file:
				file.write(get_music)
			print('第{0}页第{1}歌单第{2}首歌爬取完成~！'.format(page, y, z))
			time.sleep(0.001)

	if page < sum_music/30+1:
		sin += 30
		ein += 30
		page += 1
	else:
		break