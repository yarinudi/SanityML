__version__ = '0.2'

import os
import uuid
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform

from jnius import autoclass

from plyer import accelerometer, barometer, battery, brightness, gyroscope, gps, storagepath
from multiprocessing.dummy import Process

from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore

KV = '''
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: '30sp'
        Button:
            text: 'start service'
            on_press: app.disp_store()
'''


class ClientServerApp(App):
    stored_data = ObjectProperty(None)
    jid = 0

    def build(self):
        self.stored_data = JsonStore('data.json')
        self.jid = 0
        self.root = Builder.load_string(KV)
        return self.root

    def on_start(self):
        from kivy import platform
        if platform == "android":
            self.start_service()
        print('The application path: ' + str(storagepath.get_application_dir()))
        print('The storage path: ' + str(storagepath.get_documents_dir()))
        Process(target=self.init_sensors).start()

    def init_sensors(self):
        """ setup sensors """
        # setup timer to update sensors
        Clock.schedule_interval(self.save_sensors, 30.0/60.0)

    def save_sensors(self, dt):
        """ write sensors' data to json file """
        self.txt = ''

        try:
            accelerometer.enable()
            print('accelerometer enabled')

            accelerometer_txt = str(round(accelerometer.acceleration[0], 4)) + ',' \
                                + str(round(accelerometer.acceleration[1], 4))\
                                     + ',' + str(round(accelerometer.acceleration[2], 4))
            self.txt += 'accelerometer: ' + accelerometer_txt

        except:
            self.txt += '; cant read accelerometer'

        try:

            barometer.enable()
            print('barometer enabled')
            barometer_txt = str(round(barometer.pressure, 4))
            self.txt += '; barometer: ' + barometer_txt

        except:
            self.txt += '; cant read barometer'

        try:

            # battery.enable()
            print('battery enabled')
            battery_txt = str(battery.status.get('isCharge')) + ' ' + str(round(battery.status.get('percentage'), 4))
            self.txt += '; battery: ' + battery_txt

        except:
            self.txt += '; cant read battery'

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
                                     + str(round(gyroscope.orientation[1], 4))\
                                     + ',' + str(round(gyroscope.orientation[2], 4))
            self.txt += '; gyroscope: ' + gyroscope_txt

        except:
            self.txt += '; cant read gyroscope'

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

        self.save(self.txt)

    def save(self, data):
        self.jid += 1
        now = datetime.utcnow()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        # with open('data.txt', mode='a') as f:
        #     f.writelines(f"{date_time}, {data}\n")

        self.stored_data.put(f'{self.jid}', date=date_time, features=data)

        print(f"ADDED sensors data! \n {date_time}, {data}\n")

    def disp_store(self):
        for key in self.stored_data:
            print(key)
            print(self.stored_data[key])

    @staticmethod
    def start_service():
        print('------STARTING SERVICE-------')
        from jnius import autoclass
        service = autoclass("org.kivy.oscservice.ServicePong")
        mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
        service.start(mActivity, "")
        return service


ClientServerApp().run()
