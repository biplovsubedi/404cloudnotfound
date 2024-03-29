import requests
import json
import boto3
import googlemaps

from googleroutes import fetchDetails,timeConvert,gmapsQuery

APIKEY = 'c031ff79d81c1f77c4331df2ac93ed4b'

map_link = "https://www.google.com/maps/dir/?api=1&origin={}&destination={}&travelmode=driving"

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
    # print("Type of res_dict", str(type(res_dict)))
    return res_dict

def weather_status(emp_name, weather, total_time, distance):
    
    w_id = int(weather['id'])
    w_main = weather['main']
    w_desc = weather['description']

    weather_condition_good = [300, 301 , 302 , 310, 311, 312 , 313 , 314 , 321 ,500 , 501, 520 , 521 , 522, 531, 601,800,801,802,803,804]
    weather_conition_bad  = [502, 503 ,611, 612,613,615,616,620,621 ,701,711,721,731,741,751,761,762,771 ]
    weather_condition_severe  = [504, 511,602,622, 781, 200 , 201 , 202 , 211 , 212 , 210 , 221, 231 , 232, 230 ]

    good_moring = "Good Morniing {}, today you'll see ".format(emp_name) +w_desc
    time_taken = ". \n It will take you {} time to reach your destination (Distance - {}) . \n".format(total_time,distance)



    if w_id in weather_condition_good:
        return good_moring + time_taken+ " Have a wonderful day "

    if w_id in weather_condition_bad:
        return good_moring + time_taken+ " Have a wonderful day "

    if w_id in weather_condition_severe:
        return good_moring + time_taken+ " Please consider staying back at home  as weather conditions may get worse, Have a Wonderful Day "

    

def get_weather(latitude,longitude):
    
    weather_query = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(latitude,longitude,APIKEY)

    res = api_request(weather_query)
    # >>> dq['weather']
    # [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}]

    return res['weather'][0]

def send_sns_email(emailarn,message):
    """[summary]
    
    [description]
    
    Arguments:
        message {[type]} -- [description]
    """
    # Create an SNS client
    sns = boto3.client('sns')

    # Publish a simple message to the specified SNS topic
    response = sns.publish(
        TopicArn=emailarn,    
        Message=message,    
    )

    # Print out the response
    print("Email Response:  ",response)


def query_dynamodb():
    """[summary]
    
    [description]
    """
    dynamodb = boto3.client('dynamodb')

    response = dynamodb.scan(
        TableName='employees'
    )
    #print(response)
    return response

def process_all_users():
    """[summary]
    
    [description]
    """

    print("Processing for all Users")
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
        contact = user['contact']['S']
        email = user['email']['S']
        print ("Current Employee: ", emp_name)

        ##TODO --  process for each user
        resp = gmapsQuery(home_loc, office_loc, "driving",timeConvert(morning_departure))
        all_results = fetchDetails(resp)

        #Office Weather
        office_weather = get_weather(all_results[4],all_results[5])

        #Home Weather
        home_weather = get_weather(all_results[2],all_results[3])

        weather_message = weather_status(emp_name, home_weather, all_results[1], all_results[0])
        #print("Home weather status", home_weather_status)

        map_link_final = map_link.format(home_loc.replace(' ','+'), office_loc.replace(' ','+'))

        final_message = weather_message + '\n\n' + "Here's the link for the quickest travel!! " + map_link_final
        print(final_message)

        ################3
        #Send Message
        send_sns_sms(contact, final_message)

        #Send Email
        send_sns_email(email,final_message)



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
    print("Trying to send sns sms to : {}".format(contact))

    a = sns.publish(
        PhoneNumber=contact,
        Message=message
    )
    print("SMS Response:  ", a)

def lambda_handler(event, context):
    """Entry point for Python Lambda Function

    Arguments:
        event {[type]} -- [description]
        context {[type]} -- [description]
    """ 

    # weather = get_weather(LATITUDE,LONGITUDE)
    # #print(type(weather))
    # w_id = weather['id']
    # w_main = weather['main']
    # w_desc = weather['description']

    # print(w_id, w_main, w_desc)
    ## TODO -- ADD SNS response here
    
    #create_sns_message(weather)
    #query_dynamodb()
    process_all_users()