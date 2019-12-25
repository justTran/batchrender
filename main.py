import queue
import psutil

while True:
    print(psutil.cpu_percent(interval=0.1))

print('this is working')