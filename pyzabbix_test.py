from pyzabbix import ZabbixAPI

zapi = ZabbixAPI("http://10.108.4.34/zabbix/api_jsonrpc.php")
zapi.login("Admin", "zabbix")
print("Connected to Zabbix API Version %s" % zapi.api_version())

for h in zapi.host.get(output="extend"):
    print(h['hostid'])