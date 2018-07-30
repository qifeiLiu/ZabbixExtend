from requests import Request, Session
import simplejson as json

url = r'http://10.108.4.34/zabbix/api_jsonrpc.php'

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



def Get_item_Top10MEM(auth):
    session = Session()
    headers = {
        "Content-Type": "application/json-rpc; charset=UTF-8"
    }
    data = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params":{
                "output":"extend",
                "hostids": "10106",
                "search":{
                    "key_":"pi3.Top10PsMEM"
                 },
                "sortfield":"name",
        },
        "id": 1,
        "auth": auth
    }
    req = Request('POST', url,
                  headers=headers,
                  data=json.dumps(data)
                  )
    prepped = req.prepare()
    r = session.send(prepped)
    print("Status Code: %s" % r.status_code)
    print(r.text)


if __name__=="__main__":
    auth = Get_Session_Token(url)
    Get_item_Top10MEM(auth)
