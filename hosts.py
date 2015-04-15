from zapi import ZabbixAPI
import ConfigParser
import time
import logging

def getHosts(url, user, password, groupid):
	api = ZabbixAPI(url, user, password)
        api.login()
        params = { 'output' : 'extend',
		   'groupids': groupid,
                 }
        method = 'host.get'
        obj = api.json_obj(method, params)
        content = api.postRequest(obj)
        hosts = content['result']			
	return hosts

def deleteHosts(logging, hosts):		
	api = ZabbixAPI(url, user, password)
        api.login()
	unactive_hosts = []
	for host in hosts:
		if host['available'] == '2':
			unactive_hosts.append(host['hostid'])
	if len(unactive_hosts) != 0:
		method = 'host.delete'
		params = unactive_hosts
		obj = api.json_obj(method, params)
        	content = api.postRequest(obj)
        	delete_hosts = content['result']	
		
		logging.info("delete hosts:%s successfully", str(delete_hosts['hostids']))
		unsuccess_delete_hosts = list(set(unactive_hosts)-set(delete_hosts['hostids']))
		if len(unsuccess_delete_hosts) != 0:
			logging.error("unsuccessfully delete hosts:%s", str(unsuccess_delete_hosts))
	else:
		pass
	
if __name__ == '__main__':
	logging.basicConfig(format = '%(levelname)s:%(asctime)s %(message)s', filename = "./hosts.log", level = logging.INFO)
	while True:
		cf = ConfigParser.ConfigParser()
		
		try:
			cf.read("./zbxClient.ini")
			url = cf.get('server', 'url')
			user = cf.get('server', 'user')
			password = cf.get('server', 'password')
			timesleep = cf.getfloat('client', 'timesleep')
			groupid = cf.get('host', 'groupid')	

			hosts = getHosts(url, user, password, groupid)
			deleteHosts(logging, hosts)
			time.sleep(timesleep)
		except Exception as e:
			print e		

