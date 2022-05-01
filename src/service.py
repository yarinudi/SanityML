from time import sleep

from jnius import autoclass
from plyer import accelerometer, barometer, battery, brightness, gyroscope, gps, storagepath
from datetime import datetime

from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty
from kivy.app import App

PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)


def save_sensors(app):
    """ write sensors' data to json file """
    txt = ''

    try:
        accelerometer.enable()
        print('accelerometer enabled')

        accelerometer_txt = str(round(accelerometer.acceleration[0], 4)) + ',' \
                            + str(round(accelerometer.acceleration[1], 4)) \
                            + ',' + str(round(accelerometer.acceleration[2], 4))
        txt += 'accelerometer: ' + accelerometer_txt

    except:
        txt += '; cant read accelerometer'

    try:

        barometer.enable()
        print('barometer enabled')
        barometer_txt = str(round(barometer.pressure, 4))
        txt += '; barometer: ' + barometer_txt

    except:
        txt += '; cant read barometer'

    try:

        # battery.enable()
        print('battery enabled')
        battery_txt = str(battery.status.get('isCharge')) + ' ' + str(round(battery.status.get('percentage'), 4))
        txt += '; battery: ' + battery_txt

    except:
        txt += '; cant read battery'

    # try:
    #
    #     # brightness.enable()
    #     # print('brightness enabled')
    #     brightness_txt = str(brightness.current_level())
    #     self.txt += '; brightness: ' + brightness_txt
    #
    # except:
    #     self.txt += '; cant read brightness'

    try:

        gyroscope.enable()
        print('gyroscope enabled')
        gyroscope_txt = str(round(gyroscope.orientation[0], 4)) + ',' \
                        + str(round(gyroscope.orientation[1], 4)) \
                        + ',' + str(round(gyroscope.orientation[2], 4))
        txt += '; gyroscope: ' + gyroscope_txt

    except:
        txt += '; cant read gyroscope'

    # try:
    #
    #     gps.configure(self.save)
    #     gps.start(minTime=1000, minDistance=1)
    #     print('gps started')
    #     gyroscope_txt = str(round(gyroscope.orientation[0], 4)) + ',' \
    #                              + str(round(gyroscope.orientation[1], 4))\
    #                              + ',' + str(round(gyroscope.orientation[2], 4))
    #     self.txt += '; gyroscope: ' + gyroscope_txt
    #
    # except:
    #     self.txt += '; cant read gyroscope'

    save(txt, app)


def save(data, app):
    app.jid += 1
    now = datetime.utcnow()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    # with open('data.txt', mode='a') as f:
    #     f.writelines(f"{date_time}, {data}\n")

    app.root.stored_data.put(f'{app.jid}', date=date_time, features=data)


while True:
    print("service running.....")
    sleep(5)

    app = App.get_running_app()
    save_sensors(app)
    print('----Saved sensors successfully-------')
