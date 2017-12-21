#-*-coding:utf-8-*-

import requests
import json
import pymysql
import math

#获取用户信息
def getUserData(user_data):
	name = user_data['name']
	domain_id = user_data['url_token']
	gender_num = user_data['gender']
	is_advertiser = user_data['is_advertiser']
	user_type = user_data['user_type']
	avatar_url = user_data['avatar_url']
	is_org = user_data['is_org']
	if gender_num == 0:
		gender = '女'
		address = 'https://www.zhihu.com/people/' + domain_id + '/activities'
	elif gender_num == 1:
		gender = '男'
		address = 'https://www.zhihu.com/people/' + domain_id + '/activities'
	else:
		gender = '公众号'
		address = 'https://www.zhihu.com/org/' + domain_id + '/activities'
	return {'name':name, 'address':address, 'gender':gender, 'domain_id':domain_id, 'is_advertiser':is_advertiser, 'user_type':user_type, 'avatar_url':avatar_url, 'is_org':is_org}

#用户信息插入数据库
def insertUserData(user_data):
	sql_insert = "INSERT INTO user_details(address, name, gender, domain_id, parent_id, is_advertiser, user_type, avatar_url, is_org) VALUES('%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s')" % (user_data['address'], user_data['name'], user_data['gender'], user_data['domain_id'], user_data['user_number'], user_data['is_advertiser'], user_data['user_type'], user_data['avatar_url'], user_data['is_org'])
	try:
	    cursor.execute(sql_insert)
	    db.commit()
	except:
	    db.rollback()

#连接数据库
db = pymysql.connect(host='localhost',user='root',passwd='10210103',db='zhihu_spider_v1',port=3306,charset='utf8')
cursor = db.cursor()

# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

user_number = 1
while user_number <= 97:
	sql_fetch = "SELECT * FROM user_details WHERE user_id = '%d'" % (user_number)
	cursor.execute(sql_fetch)
	result = cursor.fetchone()
	user_domain = result[1]

	offset = 0
	limit = 20
	url = 'https://www.zhihu.com/api/v4/members/' + user_domain + '/followees?&offset=' + str(offset) + '&limit=' + str(limit)
	headers = {
	    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	    "Cookie": 'd_c0="AGDCxjZv4AuPTtN8C83BJ3F2YxV6CLSTd2Q=|1496820100"; _zap=80ff2fce-273a-4617-81f7-7868adce8d65; q_c1=487f918bfed043c88f96faa15a2cc6a1|1508206376000|1496643697000; q_c1=487f918bfed043c88f96faa15a2cc6a1|1511142991000|1496643697000; r_cap_id="NzhjMjgzZjc0MTk2NDdmMDkwZmRhY2NhZGE2NTljMmM=|1512466508|58854d93f65c05357fb0fefc01631765b3c71bf0"; cap_id="OWFiZDhlYmNlZDE5NDA5MDg0NzkyOGI5N2QzNDJhMjU=|1512466508|41837841718608fa1c7ce47b32676f62a3a20eeb"; l_cap_id="MzM4ZGI4OWI5ZDU1NDZjZWE1YzkzM2Q1ZGQ2MGVmNjA=|1512466508|cb51185b9145086554a4cc72f09432827a12211a"; z_c0="2|1:0|10:1512466525|4:z_c0|92:Mi4xUHBFNUFnQUFBQUFBWU1MR05tX2dDeWNBQUFDRUFsVk5YZlZOV2dDOGl6RlB2bk4zSFlpM0dIT2cycXBYdkdsZWRR|0a35f2c51d8d513161151dec5e82b6eb1fba87a0972404808ba505f0b834a613"; aliyungf_tc=AQAAAHKfpjKMLQ4A+p6bJ7Qsx+F7efiJ; _xsrf=639cb791-3b1c-450d-9b8a-3ff4494b90f6; __utma=51854390.273555038.1513668868.1513668868.1513668868.1; __utmb=51854390.0.10.1513668868; __utmc=51854390; __utmz=51854390.1513668868.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/stellaaaaaaaa/following; __utmv=51854390.110--|2=registration_date=20151026=1^3=entry_date=20151026=1'
	}
	content = requests.get(url, headers=headers, verify=False)
	parsed_json = json.loads(content.text)

	total = int(parsed_json['paging']['totals'])
	total_page = math.ceil(total / (offset + limit))
	page = 1
	while page <= total_page:
		n = 0
		while n < len(parsed_json['data']):
			user_data = getUserData(parsed_json['data'][n])
			user_data['user_number'] = user_number
			insertUserData(user_data)
			n += 1

		#翻页处理
		offset += 20
		url = 'https://www.zhihu.com/api/v4/members/' + user_domain + '/followees?&offset=' + str(offset) + '&limit=' + str(limit)
		content = requests.get(url, headers=headers, verify=False)
		parsed_json = json.loads(content.text)

		page += 1

	user_number += 1

cursor.close()
db.close()