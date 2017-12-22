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


def integrate(key, arr):
    while key < len(arr):
        if arr[key]['channel_name'] == arr[key-1]['channel_name']:
            arr[key-1]['context'] += arr[key]['context']
            del arr[key]
        else:
            key += 2
        return integrate(key, arr)

key = 1
integrate(key,arr)
print(arr)




