import csv
import os

class carsData:
    def __init__(self, path):
        '''
        path: csv文件文件夹
        读取csv文件内数据
        '''
        self.data = {}
        allName = os.listdir(path)
        for i in allName:
            data = []
            a = open(path+'/'+i)
            form = csv.reader(a)
            k = 0
            for j in form:
                if k == 0:
                    parameter = j
                    k = k+1
                    continue
                else:
                    temporaryData = dict(zip(parameter, j))
                data.append(temporaryData)
            self.data.setdefault(i,data)
            a.close()

    def readCarMessage(self, name = None):
        '''
        name: 车辆编号
        得到其中一辆车的行走信息
        '''
        if name:
            carMessage = self.data[name]
        else:
            for name in self.data:
                carMessage = self.data[name]
                break
        return carMessage

    def amount(self):
        return len(self.data)

if __name__ == "__main__":
    import json
    path = './data/testData'
    a = carsData(path)
    with open("temp.json","w+",encoding="utf-8") as f:
        f.write(json.dumps(a.data, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))