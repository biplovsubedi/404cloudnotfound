def weather_status(ID ):
    
    weather_condition_good = [300, 301 , 302 , 310, 311, 312 , 313 , 314 , 321 ,500 , 501, 520 , 521 , 522, 531, 601,800,801,802,803,804]
    weather_conition_bad  = [502, 503 ,611, 612,613,615,616,620,621 ,701,711,721,731,741,751,761,762,771 ]
    weather_condition_severe  = [504, 511,602,622, 781, 200 , 201 , 202 , 211 , 212 , 210 , 221, 231 , 232, 230 ]

    if ID in weather_condition_good:
        
        return "Good Morniing , today you'll see " +weather(ID)+" Have a wonderful day :) "

    if ID in weather_condition_bad:
        return "Good Morniing , today you'll see " +weather(ID)+" Have a wonderful day :) "

    if ID in weather_condition_severe:
        return "Good Morniing , today you'll see " +weather(ID)+" Please consider staying back at home  as weather conditions may get worse, Have a Wonderful Day :) "

    
def weather(ID ):
    return "behenchod"

a  = weather_status(300)
print(a)
