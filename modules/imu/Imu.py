import subprocess
import re
import time

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

class Imu():
    def __init__(self, file_name):
        columns = ['timestamp','yaw', 'pitch', 'roll','acelerometer_X','acelerometer_Y','acelerometer_Z','gyro_X','gyro_Y','gyro_Z']
        self.file = open(file_name+".csv","w")
        self.file.write(";".join(columns) +"\n")


        collectCommand = "minimu9-ahrs --output euler $@ "
        process = subprocess.Popen(collectCommand.split(), stdout=subprocess.PIPE)
        self.process = process

    def getSample(self):
        firstTimestamp = time.time()
        dataCollected = self.collect_data()
        timestamp = mean([time.time(), firstTimestamp])
        finalString = str(timestamp) + ";"
        finalString = finalString + ";".join(str(v) for v in dataCollected) +"\n"
        self.file.write(finalString)

    def collect_data(self):
        sample = self.process.stdout.readline()
        sample = sample.decode('utf-8')
        sample = re.split(r'\s*', sample)
        sample = filter(lambda x: x , sample)
        print(sample)
        return sample