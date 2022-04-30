from time import sleep

from jnius import autoclass
from plyer import accelerometer, barometer, battery, brightness, gyroscope
from datetime import datetime

from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty
from kivy.app import App

PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)

stored_data = JsonStore('data.json')


def save(data, jid):
    now = datetime.utcnow()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    # # Define upload and output folders
    # UPLOAD_FOLDER = date_time
    # send_flag = False
    #
    # if not os.path.exists(UPLOAD_FOLDER) and not send_flag:
    #     os.makedirs(os.path.join(UPLOAD_FOLDER))
    #
    # with open('data.txt', mode='a') as f:
    #     f.writelines(f"{date_time}, {data}\n")
    #     print(f"ADDED sensors data! \n {date_time}, {data}\n")

    app = App.get_running_app()
    app.root.stored_data.put(f'id {jid}, {date_time}', text=data)
    # app.root.stored_data.get('mydata')['text'] if app.root.stored_data.exists('mydata') else ''


data_counter = 0

while True:
    print("service running.....")
    sleep(5)
    try:

        accelerometer.enable()
        print('accelerometer enabled')

        accelerometer_txt = str(round(accelerometer.acceleration[0], 4)) + ',' \
                            + str(round(accelerometer.acceleration[1], 4))\
                            + ',' + str(round(accelerometer.acceleration[2], 4))
        txt = ';accelerometer: ' + accelerometer_txt

    except:
        txt = txt + 'cant read accelerometer'
    #
    # try:
    #
    #     barometer.enable()
    #     print('barometer enabled')
    #     barometer_txt = str(round(barometer.pressure, 4))
    #     txt = txt + '; barometer: ' + barometer_txt
    #
    # except:
    #     txt = txt + 'cant read barometer'
    #
    # try:
    #
    #     battery.enable()
    #     print('battery enabled')
    #     battery_txt = str(battery.isCharge) + str(round(battery.percentage, 4))
    #     txt = txt + '; battery: ' + battery_txt
    #
    # except:
    #     txt = txt + 'cant read battery'
    #
    # try:
    #
    #     brightness.enable()
    #     print('brightness enabled')
    #     brightness_txt = str(brightness.current_level())
    #     txt = txt + '; brightness: ' + brightness_txt
    #
    # except:
    #     txt = txt + 'cant read brightness'
    #
    # try:
    #
    #     gyroscope.enable()
    #     print('gyroscope enabled')
    #     gyroscope_txt = str(round(gyroscope.orientation[0], 4)) + ',' \
    #                              + str(round(gyroscope.orientation[1], 4))\
    #                              + ',' + str(round(gyroscope.orientation[2], 4))
    #     txt = txt + '; gyroscope: ' + gyroscope_txt
    #
    # except:
    #     txt = txt + 'cant read gyroscope'

    save(txt, data_counter)
    data_counter += 1
