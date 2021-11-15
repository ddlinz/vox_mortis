import time
from datetime import datetime
from flask import Flask, render_template, url_for
from datetime import datetime
from vox.app import run_flask_server

print("Starting vox application...")

# write to a log file indicating the that the application is running #
while 1:
    time.sleep(5)
    print("application running...")

    run_flask_server()

    # create log file and write
    with open("log.txt", "a") as myfile:
        now = datetime.now()
        time_now = now.strftime("%H:%M:%S")
        myfile.write("log application running..." + str(time_now) + "\n")
