from time import sleep

from jnius import autoclass
from plyer import accelerometer, barometer, battery, brightness, gyroscope, gps
from datetime import datetime

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

    try:

        gyroscope.enable()
        print('gyroscope enabled')
        gyroscope_txt = str(round(gyroscope.orientation[0], 4)) + ',' \
                        + str(round(gyroscope.orientation[1], 4)) \
                        + ',' + str(round(gyroscope.orientation[2], 4))
        txt += '; gyroscope: ' + gyroscope_txt

    except:
        txt += '; cant read gyroscope'

    # save(txt, app)


# def save(data, app):
#     app.jid += 1
#     now = datetime.utcnow()
#     date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
#
#     # with open('data.txt', mode='a') as f:
#     #     f.writelines(f"{date_time}, {data}\n")
#
#     app.root.stored_data.put(f'{app.jid}', date=date_time, features=data)
#

while True:
    print("service running.....")
    sleep(5)

    cur_app = App.get_running_app()
    # cur_app.stored_data.put('1111111111111111', date='date_time', features='data')
    # save_sensors(cur_app)
    print('----Saved sensors successfully-------')
