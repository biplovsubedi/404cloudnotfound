import requests
import json

APIKEY = 'c031ff79d81c1f77c4331df2ac93ed4b'


LATITUDE='12.9716'
LONGITUDE ='77.5946'


def api_request(query):
	"""Send an API request using the query and return the dictionary of the response
	
	Make sure that the response code is 200.
	
	Arguments:
		query {[type]} -- [description]
	
	Returns:
		[type] -- [description]
	"""

	res = requests.get(query)

	status_code = res.status_code
	##TODO -- Make sure that the status code is 200

	res_str = json.dumps(res.json())
	res_dict = json.loads(res_str)
	print("Type of res_dict", str(type(res_dict)))
	return res_dict

def get_weather(latitude,longitude):
	
	weather_query = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(latitude,longitude,APIKEY)

	res = api_request(weather_query)
	# >>> dq['weather']
	# [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}]

	return res['weather'][0]

def lambda_handler(event, context):
	"""Entry point for Python Lambda Function

	Arguments:
		event {[type]} -- [description]
		context {[type]} -- [description]
	""" 

	weather = get_weather(LATITUDE,LONGITUDE)
	#print(type(weather))
	w_id = weather['id']
	w_main = weather['main']
	w_desc = weather['description']

	print(w_id, w_main, w_desc)
	## TODO -- ADD SNS response here
	