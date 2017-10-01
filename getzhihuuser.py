#!/bin/bash
#coding:utf8
import re;
import urllib;
import datetime;
import MySQLdb;

reg=r'<a class="author-link".*>(.*)</a>'; #正则
namere=re.compile(reg);

def getHtml(url):
	page=urllib.urlopen(url);
	html=page.read();
	return html;

def getName(html):
	nameList=re.findall(namere,html);
	#print nameList;
	li=[];
	for name in nameList:
		update_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
		li.append((name,update_time));
	print len(li);
	return li;


if(__name__=='__main__'):
	conn=MySQLdb.Connect(host='localhost',port=3306,user='root',passwd='123456',db='test',charset='utf8');
	cur=conn.cursor();
	#sql="select url from question order by id desc limit 50";
	sql="select id,url from question where status='0' order by id desc";
	cur.execute(sql);
	urlList=cur.fetchall();
	#print urlList;
	
	li=[];
	delLi=[];
	sql = "insert into user (name,update_time) values(%s,%s)";
	for val in urlList:
		url=val[1];
		id=val[0];
		html=getHtml(url);
		tmpLi=getName(html);
		if(len(tmpLi)>=15):
			#print 'delete';
			delLi.append("'"+str(id)+"'");
		li.extend(tmpLi);
		if(len(li)>50):
			cur.executemany(sql,li);
			conn.commit();
			li=[];
		if(len(delLi)>50):
			delstr=",".join(delLi);
			cur.execute("update question set status='1' where id in ("+delstr+")");
			conn.commit();
			delLi=[];
	
	if(len(li)>0):
		cur.executemany(sql,li);
		conn.commit();
	#print delLi;
	if(len(delLi)>0):
		delstr=",".join(delLi);
		cur.execute("update question set status='1' where id in ("+delstr+")");
		conn.commit();

	cur.execute("drop table if exists `tmpuser`");
	cur.execute("create table tmpuser as select min(id) as id from user group by name");
	cur.execute("delete from user where id not in (select id from tmpuser)");
	conn.commit();
	cur.close();
	conn.close();
	
