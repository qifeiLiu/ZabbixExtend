# -*- coding: utf-8 -*-
from requests import Request, Session
import simplejson as json
import time
import csv

url = r'http://10.108.4.34/zabbix/api_jsonrpc.php'


def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt

def Get_Session_Token(url):
    session = Session()
    headers = {
        "Content-Type": "application/json-rpc; charset=UTF-8"
    }
    data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user":"Admin",
            "password":"zabbix"
        },
        "id": 1,
        "auth": None
    }
    req = Request('POST', url,
                  headers=headers,
                  data = json.dumps(data)
                  )
    prepped = req.prepare()
    r = session.send(prepped)
    print("Status Code: %s" % r.status_code)
    print(r.text)
    return r.json()["result"]

def Get_history_Top10MEM(auth):
    session = Session()
    headers = {
        "Content-Type": "application/json-rpc; charset=UTF-8"
    }
    data ={
    "jsonrpc": "2.0",
    "method": "history.get",
    "params": {
        "output": "extend",
        "history": 4,
        "itemids": "23776",
        "sortfield": "clock",
        "sortorder": "DESC",
        "limit": 1
    },
    "auth": auth,
    "id": 1
}
    req = Request('POST', url,
                  headers=headers,
                  data=json.dumps(data)
                  )
    prepped = req.prepare()
    r = session.send(prepped)
    print("Status Code: %s" % r.status_code)
    print(r.text)
    return r.text

def Get_history_Top10CPU(auth):
    session = Session()
    headers = {
        "Content-Type": "application/json-rpc; charset=UTF-8"
    }
    data ={
    "jsonrpc": "2.0",
    "method": "history.get",
    "params": {
        "output": "extend",
        "history": 4,
        "itemids": "23777",
        "sortfield": "clock",
        "sortorder": "DESC",
        "limit": 1
    },
    "auth": auth,
    "id": 1
}
    req = Request('POST', url,
                  headers=headers,
                  data=json.dumps(data)
                  )
    prepped = req.prepare()
    r = session.send(prepped)
    print("Status Code: %s" % r.status_code)
    print(type(r.json()))
    return r.text

def deal_with_history_data(data):
    json_data = json.loads(data)
    dict_result={}
    time = timestamp_datetime(int(json_data["result"][0]["clock"]))
    # print(time)
    dict_result.update({"time":time})
    str_result = json_data["result"][0]["value"]
    list_line = str_result.split("\n")
    for item in list_line:
            dict_result.update({item[0:-5].strip():item[-4:].strip()})
    print(dict_result)
    return dict_result

def write_dict_csv(dict_result,filename):
    with open(filename,'a+',newline='') as f:
        writer = csv.writer(f)
        for key, value in dict_result.items():
            writer.writerow([key, value])

if __name__=="__main__":
    auth = Get_Session_Token(url)
    data_MEM = Get_history_Top10MEM(auth)
    data_CPU = Get_history_Top10CPU(auth)
    dict_result_MEM = deal_with_history_data(data_MEM)
    dict_result_CPU = deal_with_history_data(data_CPU)
    write_dict_csv(dict_result_MEM,"Top10MEM.csv")
    write_dict_csv(dict_result_CPU, "Top10CPU.csv")