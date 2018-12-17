from Gps import Gps
import time

g = Gps()
# Time to settle the coordinates on Euler Angles

for item in range(200):
    print(g.read_data())
    time.sleep(0.15)

    