# -*-coding:utf-8-*-
arr = [
    {
        "channel_name" : "mysql",
        "context"      : "select * from table1 ",
        "session_key"  :"2290f8da70aefcbde37f98321bb90a11",
    },
    {
        "channel_name" : "mysql",
        "context"   : "select * from table2",
        "session_key": "2290f8da70aefcbde37f98321bb90a11",
    },
    {
        "channel_name" : "mysql",
        "context"   : "select * from table3",
        "session_key":"2290f8da70aefcbde37f98321bb90a11",
    },
    {
        "channel_name" : "log",
        "context"   : "我只是一个记录日志",
        "session_key" : "2290f8da70aefcbde37f98321bb90a11",
    },
    {
        "channel_name" : "mysql",
        "context"   : "select * from table5",
        "session_key" : "2290f8da70aefcbde37f98321bb90a11",
    },
    {
        "channel_name" : "mysql",
        "context"   : "select * from table6",
        "session_key" : "2290f8da70aefcbde37f98321bb90a11",
    },
]

arr_backup = []
dic_backup = {}
channel_name = ''
context_mysql = ''
for key in range(0,len(arr)):
    channel_name = arr[key]['channel_name']
    if channel_name == 'mysql':
        context_mysql += arr[key]['context']
        dic_backup = {'channel_name':'mysql', 'context': context_mysql, 'session_key':'2290f8da70aefcbde37f98321bb90a11'}
    else:
        arr_backup.append(dic_backup)
        context_mysql = arr[key]['context']
        dic_backup = {'channel_name':'log', 'context': context_mysql, 'session_key':'2290f8da70aefcbde37f98321bb90a11'}
        arr_backup.append(dic_backup)
        context_mysql = ''
arr_backup.append(dic_backup)
arr = arr_backup
print(arr)