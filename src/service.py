from time import sleep

from jnius import autoclass
from plyer import accelerometer
from datetime import datetime

PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)


def save(data):
    now = datetime.utcnow()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    # # Define upload and output folders
    # UPLOAD_FOLDER = date_time
    # send_flag = False
    #
    # if not os.path.exists(UPLOAD_FOLDER) and not send_flag:
    #     os.makedirs(os.path.join(UPLOAD_FOLDER))

    with open('data.txt', mode='a') as f:
        f.writelines(f"{date_time}, {data}\n")
        print(f"ADDED sensors data! \n {date_time}, {data}\n")


while True:
    print("service running.....")
    sleep(5)
    try:
        accelerometer.enable()
        print('accelerometer enabled')

        accelerometer_txt = str(round(accelerometer.acceleration[0], 4)) + ',' \
                                 + str(round(accelerometer.acceleration[1], 4))\
                                 + ',' + str(round(accelerometer.acceleration[2], 4))
        txt = 'accelerometer: ' + accelerometer_txt

        save(txt)

    except:
        print('cant read sensors')

