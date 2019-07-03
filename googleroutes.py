import googlemaps
import datetime
GMAPS_API_KEY = "AIzaSyAzu_s97D0bESDkKQ"
gmaps = googlemaps.Client(key=GMAPS_API_KEY)

"""
Fetch these details from DynamoDB
"""
    
#Initialise 
start_address = "Grexter La Vie"
dest_address = "RBS RMZ Bengaluru"

link = "https://www.google.com/maps/dir/?api=1&origin=" + start_address + "&destination=" + dest_address + "&travelmode=driving"

now = datetime.now()
dept_time = now

tm = str("1300")


def timeConvert(tm):
    
    now = datetime.datetime.now()
    tm = str(now.year) + " " + str(now.month) + " " + str(now.day) + " " + tm
    newdm = datetime.datetime.strptime(tm, '%Y %m %d %H%M')
    return newdm


def fetchDetails(directions_result):
    #endlocation
    end_lat = directions_result[0]['legs'][0]['end_location']['lat']
    end_lng = directions_result[0]['legs'][0]['end_location']['lng']
    
    #startlocation
    start_lat= directions_result[0]['legs'][0]['start_location']['lat']
    start_lng = directions_result[0]['legs'][0]['start_location']['lng']
    
    #Fetching the distance
    dist = directions_result[0]['legs'][0]['distance']['text']
    #Fetching travel time
    time = directions_result[0]['legs'][0]['duration_in_traffic']['text']
    return [dist, time, start_lat,start_lng, end_lat,end_lng]

def gmapsQuery(start_address, dest_address, mode, departure_time):
    return gmaps.directions(start_address,dest_address,mode=mode,departure_time=departure_time)


# def lambda_handler(event, context):
#     """
#     Entry point for Python Lambda Function
# 	Arguments:
# 		event {[type]} -- [description]
# 		context {[type]} -- [description]
# 	""" 
    
#     directions_result = gmapsQuery(start_address,dest_address,mode=mode,departure_time=dept_time) 
#     dist, time, start_lat,start_lng, end_lat,end_lng = fetchDetails(directions_result)
#     print(dist, time, start_lat,start_lng, end_lat,end_lng)
    



