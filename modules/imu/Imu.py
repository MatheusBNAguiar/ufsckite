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

    def getSample(self):
        firstTimestamp = time.time()
        dataCollected = self.collect_data()
        timestamp = mean([time.time(), firstTimestamp])
        finalString = str(timestamp) + ";"
        finalString = finalString + ";".join(dataCollected) +"\n"

    def collect_data(self):
        collectCommand = "minimu9-ahrs --output euler $@ | head -n250"
        process = subprocess.Popen(collectCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        
        samples = re.split(r'\n', output.decode('utf-8'))
        samples = samples[-51:]

        groupedMeasurements = list()

        for sample in samples:
            measurements = re.split(r'\s*', sample)
            for index, measurement in enumerate(measurements):
                try:
                    groupedMeasurements[index].append(float(measurement))
                except:
                    groupedMeasurements.append([float(measurement)])
                
        simplifiedData = map(mean, groupedMeasurements)
        return simplifiedData


imu = Imu("imu")
for item in range(10):
    imu.getSample()
    
