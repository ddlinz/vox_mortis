import time
from datetime import datetime
from flask import Flask, render_template, url_for
from datetime import datetime
from vox.flask_app import run_flask_server
import multiprocessing
import vox.runner

print("Starting vox application...")


def init():

    # write to a log file indicating the that the application is running #
    while 1:
        time.sleep(5)
        print("application running...")

        run_flask_server()

        # # create log file and write
        # with open("log.txt", "a") as myfile:
        #     now = datetime.now()
        #     time_now = now.strftime("%H:%M:%S")
        #     myfile.write("log application running..." + str(time_now) + "\n")


if __name__ == "__main__":
    p = multiprocessing.Process(target=vox.runner.f, args=("bob",))
    p.start()
    p.join()
#     init()
