#!/usr/bin/env python 
# coding: utf-8
# author: bechueng92
# data : 2015-12-28

import requests 
import urllib2
import urllib 
import time
import re
from datetime import date,time,datetime,timedelta

class usersign(object):
	"""docstring for usergin"""
	def __init__(self,name,password):
		self.name = name
		self.password = password
		loginmessage='loginning on the website, username: %s password: %s '
		userdata = (self.name,self.password)
		print loginmessage % userdata

	def _postheader(self):
		header = {}
		header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' 
		header['Host'] = 'www.zimuzu.tv'
		header['Connection'] = 'keep-alive'
		#header['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
		header['Accept-Language'] = 'zh-CN,zh;q=0.8'
		header['Accept-Encoding'] = 'gzip,deflate'
		header['Origin'] = 'http://www.zimuzu.tv'
		header['Referer'] = 'http://www.zimuzu.tv/user/login'
		header['Accept'] = 'application/json, text/javascript, */*; q=0.01'
		header['X-Requested-With'] = 'XMLHttpRequest'
		#print header
		return header 

	def sign(self):
		headers = self._postheader()
		#get the header
		resHeader = requests.get(r'http://www.zimuzu.tv/usr/login',headers).headers
		session = resHeader['set-cookie'][10:36]
		#add the cookies
		headers['Cookie'] ='PHPSESSID='+session+ r'; CNZZDATA1254180690=1872246458-1448330530-%7C1451300613; mykeywords=a%3A1%3A%7Bi%3A0%3Bs%3A9%3A%22%E5%86%B0%E8%A1%80%E6%9A%B4%22%3B%7D'
		loginparam = {'account':self.name,
		'password':self.password,
		'remember':'1',
		'url_back':'http://www.zimuzu.tv/user/sign'}
		#login the website
		res = requests.post(r'http://www.zimuzu.tv/User/Login/ajaxLogin',data=loginparam,headers=headers)
		cookie = res.headers['set-cookie']
		#remove the pattern items
		cookie = cookie.replace('GINFO=deleted;','').replace('GKEY=deleted;','')
		GINFO = re.search('GINFO=uid[^;]+',cookie).group(0)+';'
		GKEY = re.search('GKEY=[^;]+',cookie).group(0)+';'
		CT = 'yhd%2F'+str(int(time.time()))+";"
		headers['Cookie'] = 'PHPSESSID='+session + ';' + CT+(GINFO+GKEY)*3
		requests.get(r'http://www.zimuzu.tv/user/sign',headers=headers).content
		print 'wait for 20 seconds'
		time.sleep(20)
		content=requests.get(r'http://www.zimuzu.tv/user/sign/dosign',headers=headers).json()
		if content['data']!=False:
			print "sign success!"
		if content['data']== False:
			print "sign failed"+ str(content['status'])

def runtask(func,day=0,hour=0,min=0,second=0):
	#Init time 
	now = datetime.now()
	strnow=now.strftime('%Y-%m-%d %H:%M:%S')
	print "the time now",strnow
	#First next run time
	period = timedelta(days=day,hours=hour,minutes=min,seconds=second)
	next_time = now +period
	strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
	print "next run:",strnext_time
	while True:
		#Get system current time
		iter_now = datetime.now()
		iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
		if str(iter_now_time) == str(strnext_time):
			print "---------------start work: %s-----------------" %iter_now_time
			##doing the task
			func()
			print "---------------task done!!------------------"
			##Get the next iteration time 
			iter_time = iter_now+period
			strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
			print "next_iter: %s" %strnext_time
		continue

if __name__ == '__main__':
	signzimuzu = usersign('your account','your password')
	#print 'hello'
	runtask(signzimuzu.sign(),day=1,hour=0,min=0)