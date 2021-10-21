import time
from datetime import datetime


print("Starting vox application...")

while 1:
    time.sleep(5)
    print("application running...")

    with open("log.txt", "a") as myfile:
        now = datetime.now()
        time_now = now.strftime("%H:%M:%S")
        myfile.write("loggin application running..." + str(time_now) + "\n")
