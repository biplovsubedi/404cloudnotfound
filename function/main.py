import requests
import json
import boto3
import googlemaps

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

def send_sns_email(message):
	"""[summary]
	
	[description]
	
	Arguments:
		message {[type]} -- [description]
	"""
	# Create an SNS client
	sns = boto3.client('sns')

	# Publish a simple message to the specified SNS topic
	response = sns.publish(
	    TopicArn='arn:aws:sns:ap-south-1:443236223987:WeatherNotification',    
	    Message=message,    
	)

	# Print out the response
	print(response)


def create_sns_message(weather):
	"""[summary]
	
	[description]
	
	Arguments:
		weather {[type]} -- [description]
	"""
	message = "Current Weather is {}. <b>description</b> {}".format(weather['main'],weather['description'])
	#send_sns_email(message)
	send_sns_sms(message)

def query_dynamodb():
	"""[summary]
	
	[description]
	"""
	dynamodb = boto3.client('dynamodb')

	response = dynamodb.scan(
		TableName='employees'
	)
	print(response)
	return response

def process_all_users():
	"""[summary]
	
	[description]
	"""
	dynamo_res = query_dynamodb()

	#all_users - list of users objects
	all_users = dynamo_res['Items']

	#user = {'shift_end': {'S': '1700'}, 'shift_start': {'S': '0900'}, 'morning_departure': {'S': '0800'}, 'emp_id': {'S': '1002'}, 'emp_name': {'S': 'Shubham'}, 'office_loc': {'S': 'RBS, RMZ, Bangalore'}, 'home_loc': {'S': 'Bangalore Central, Bellandur'}}
	for user in all_users:
		emp_name = user['emp_name']['S']
		shift_start = user['shift_start']['S']
		shift_end = user['shift_end']['S']
		morning_departure = user['morning_departure']['S']
		office_loc = user['office_loc']['S']
		home_loc = user['home_loc']['S']

		##TODO --  process for each user
		


def send_sns_sms(contact,message):
	"""[summary]
	
	[description]
	
	Arguments:
		message {[type]} -- [description]
	"""
	sns = boto3.client('sns')

	# topic = sns.create_topic(Name="notifications")
	# topic_arn = topic['TopicArn']  # get its Amazon Resource Name

	# # Add SMS Subscribers
	# for number in ['+919015066557','+919611048570']:
	#     sns.subscribe(
	#         TopicArn=topic_arn,
	#         Protocol='sms',
	#         Endpoint=number  # <-- number who'll receive an SMS message.
	#     )

	# # Publish a message.
	# sns.publish(Message="Good news everyone!", TopicArn=topic_arn)

	a = sns.publish(
		PhoneNumber=contact,
   		Message=message
	)
	print(a)

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
	
	create_sns_message(weather)
	#query_dynamodb()