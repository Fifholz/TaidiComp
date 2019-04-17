from carReader import carsData
import matplotlib.pyplot as plt
import trans as trans
import datetime
import os.path
import json

DATA_PATH = "./data/testData"

def speedRank(num, max_speed = 200):
    bar = max_speed // 10
    return (num+bar-1) // bar

def produre(thisCar, carname, removeHighways = False):
    points = []

    ang = float(thisCar[0]["direction_angle"])
    v = speedRank(float(thisCar[0]["gps_speed"]))
    max_speed = float(thisCar[0]["gps_speed"])
    temp = thisCar[0]
    temp["max_speed"] = 0
    points.append(temp)

    for i in range(len(thisCar)-1):
        new_time = datetime.datetime.strptime(thisCar[i+1]['location_time'], '%Y-%m-%d %H:%M:%S')
        if speedRank(float(thisCar[i+1]["gps_speed"])) != v or abs(float(thisCar[i+1]["direction_angle"])) - ang > 90:

            temp = thisCar[i]
            temp["max_speed"] = max_speed
            points.append(temp)

            temp = thisCar[i+1]
            temp["max_speed"] = max_speed
            points.append(temp)

            v = speedRank(float(thisCar[i+1]["gps_speed"]))
            ang = float(thisCar[i+1]["direction_angle"])
            max_speed = float(thisCar[i+1]["gps_speed"])
        else:
            if float(thisCar[i+1]["gps_speed"]) > max_speed:
                max_speed = float(thisCar[i+1]["gps_speed"])
    
    if removeHighways:
        raw_points = points
        points = []
        for point in raw_points:
            if float(point["gps_speed"]) <= 60 and float(point["gps_speed"]) >= 30:
                points.append(point)

    text = json.dumps(points, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    with open("json/{}.json".format(car), "w+", encoding="utf-8") as f:
        f.write(text)
    print("car:{} with {} points \nhas points:{}\n".format(car, len(thisCar), len(points)))

if __name__ == "__main__":
    
    data = carsData(DATA_PATH)
    for car in data.data:
        thisCar = data.readCarMessage(car)
        produre(thisCar, car, removeHighways=True)