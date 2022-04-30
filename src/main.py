__version__ = '0.2'

import os
import uuid
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform

from jnius import autoclass

from plyer import accelerometer, storagepath
from multiprocessing.dummy import Process
from time import sleep

KV = '''
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: '30sp'
        Button:
            text: 'start service'
            on_press:
'''


class ClientServerApp(App):

    def build(self):
        self.root = Builder.load_string(KV)
        return self.root

    def on_start(self):
        from kivy import platform
        if platform == "android":
            self.start_service()
        sleep(5)
        print('The storage path: ' + str(storagepath))
        Process(target=self.init_sensors).start()

    def init_sensors(self):
        """ setup sensors """
        # try:
        #     accelerometer.enable()
        #     print('accelerometer enabled')
        #
        # except:
        #     print('cant enable accelerometer')

        # setup timer to update sensors
        Clock.schedule_interval(self.save_sensors, 30.0/60.0)

    def save_sensors(self, dt):
        """ write sensors' data to txt file """
        try:
            accelerometer.enable()
            print('accelerometer enabled')

            accelerometer_txt = str(round(accelerometer.acceleration[0], 4)) + ',' \
                                + str(round(accelerometer.acceleration[1], 4))\
                                     + ',' + str(round(accelerometer.acceleration[2], 4))
            self.txt = 'accelerometer: ' + accelerometer_txt

            self.save(self.txt)

        except:
            print('cant read sensors')

    def save(self, data):
        now = datetime.utcnow()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        with open('data.txt', mode='a') as f:
            f.writelines(f"{date_time}, {data}\n")
            print(f"ADDED sensors data! \n {date_time}, {data}\n")

    @staticmethod
    def start_service():
        print('------STARTING SERVICE-------')
        from jnius import autoclass
        service = autoclass("org.kivy.oscservice.ServicePong")
        mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
        service.start(mActivity, "")
        return service


ClientServerApp().run()
