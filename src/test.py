from carReader import carsData
import matplotlib.pyplot as plt
import trans as trans
import datetime
import os.path

DATA_PATH = "./data/allData"

def speedRank(num, max_speed):
    bar = max_speed // 10
    return (num+bar-1) // bar

def produre(thisCar, carname):
    x, y, speed, time = [], [], [], []
    x.append(0)
    y.append(0)
    max_speed = 0
    for i in range(len(thisCar)-1):
        x_1, y_1 = trans.wgs2bd(float(thisCar[i]["lat"]), float(thisCar[i]["lng"]))
        x_2, y_2 = trans.wgs2bd(float(thisCar[i+1]["lat"]), float(thisCar[i+1]["lng"]))
        x.append(x[i] + x_2 - x_1)
        y.append(y[i] + y_2 - y_1)
        temp = datetime.datetime.strptime(thisCar[i]['location_time'], '%Y-%m-%d %H:%M:%S')
        time.append(temp)
        speed.append(float(thisCar[i]["gps_speed"]))
        if speed[i] > max_speed:
            max_speed = speed[i]
    time.append(temp)
    px, py = [], []
    v = speedRank(speed[0], max_speed)
    for i in range(len(x)-1):
        if i % 10000 == 0 or i == len(x)-2:
            if i != 0:
                if not os.path.isdir("./figures/{}".format(carname.split(".")[0])):
                    os.makedirs("./figures/{}".format(carname.split(".")[0]))
                plt.savefig("./figures/{}/{}.png".format(carname.split(".")[0], str(i // 10000)))
            plt.figure(figsize = (32, 24))
        if speedRank(speed[i], max_speed) != v or (time[i+1]-time[i]).seconds > 10:
            if (time[i+1]-time[i]).seconds <= 10:
                px.append(x[i])
                py.append(y[i])                
            plt.plot(px, py, linewidth = '2', color='#ff{:0>2x}{:0>2x}'.format(int(200-v*16),int(200-v*16)))
            px, py = [], []
            v = speedRank(speed[i], max_speed)
        else:
            px.append(x[i])
            py.append(y[i])

if __name__ == "__main__":
    
    data = carsData(DATA_PATH)
    for car in data.data:
        thisCar = data.readCarMessage(car)
        produre(thisCar, car)