import json

def get_user_agent() -> str:
	with open('config.json','r',encoding='utf8') as file:
		config = json.load(file)
	user_agent = ""
	api_version = "api-client/"+config['api_version']
	douban_version = 'com.douban.frodo/'+config['douban_version']
	system = 'Android/'+config['system']
	product = 'product/'+config['product']
	vender = 'vendor/'+config['vender']
	model = 'model/'+config['model']
	brand = 'brand/'+config['brand']
	os_rom = 'rom/'+config['os_rom']
	network = 'network/'+config['network']
	udid = 'udid/'+config['udid']
	platform = 'platform/'+config['platform']
	user_agent = ' '.join([
		api_version,douban_version,
		system,product,vender,model,
		brand,os_rom,network,udid,platform
	])
	return user_agent

def get_auth() -> str:
	with open('config.json','r',encoding='utf8') as file:
		config = json.load(file)
	auth = 'Bearer ' + config['access_token']
	return auth

def get_headers():
	headers = {}
	headers['User-Agent'] = get_user_agent()
	headers['authorization'] = get_auth()
	return headers

