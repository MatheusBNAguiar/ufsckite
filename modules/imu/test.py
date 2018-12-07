from Imu import Imu 
import time

imu = Imu("imu")
# Time to settle the coordinates on Euler Angles
time.sleep(1.5)
for item in range(200):
    imu.getSample()
    time.sleep(0.15)

    