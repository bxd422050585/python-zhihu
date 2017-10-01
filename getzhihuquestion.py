#!/bin/bash
#coding:utf8
import re;
import urllib;
import datetime;
import MySQLdb;

reg=r'<a.*href="(/question/\d{8})/answer.*">'; #正则
quesre=re.compile(reg);

def getHtml(url):
	page=urllib.urlopen(url);
	#urllib.urlretrieve('https://www.zhihu.com/','a.html');
	html=page.read();
	return html;

def getImg(html):
	quesList=re.findall(quesre,html);
	li=[];
	for ques in quesList:
		update_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
		li.append(('https://www.zhihu.com'+ques,update_time));
	return li;


conn=MySQLdb.Connect(host='localhost',port=3306,user='root',passwd='123456',db='test',charset='utf8')
html=getHtml('https://www.zhihu.com/');
#print html;
li=getImg(html);
#print li;
sql = "insert into question (url,update_time) values(%s,%s)";
cur=conn.cursor();
cur.executemany(sql,li);
conn.commit();
cur.execute("drop table if exists `tmp`");
cur.execute("create table tmp as select min(id) as id from question group by url");
cur.execute("delete from question where id not in (select id from tmp)");
conn.commit();
conn.cursor().close();
conn.close();
