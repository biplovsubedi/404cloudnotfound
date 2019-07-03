import googlemaps
import datetime
GMAPS_API_KEY = ""
gmaps = googlemaps.Client(key=GMAPS_API_KEY)

"""
Fetch these details from DynamoDB
"""
    
#Initialise 
start_address = "Grexter La Vie"
dest_address = "RBS RMZ Bengaluru"


now = datetime.datetime.now()
dept_time = now

tm = str("1300")


def timeConvert(tm):
    
    now = datetime.datetime.now()
    tm = str(now.year) + " " + str(now.month) + " " + str(now.day) + " " + tm
    newdm = datetime.datetime.strptime(tm, '%Y %m %d %H%M')
    print("Time Converted: ", str(newdm))
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

    



