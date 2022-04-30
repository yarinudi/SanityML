__version__ = '0.2'

import os
import uuid
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform

from jnius import autoclass

from plyer import accelerometer
from multiprocessing.dummy import Process

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
        Process(target=self.init_sensors).start()

    # def start_service(self):
    #     if platform == 'android':
    #         print('Starting service...')
    #         service = autoclass(SERVICE_NAME)
    #         self.mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
    #         argument = ''
    #         service.start(self.mActivity, argument)
    #         self.service = service
    #         Process(target=self.init_sensors()).start()
    #
    #         # start sensors
    #         self.user_id = str(uuid.uuid1())
    #         print('Current User ID: ', self.user_id)
    #
    #         # write uid to txt file
    #         with open('data.txt', mode='a') as f:
    #             f.writelines(f"{self.user_id}\n\n")
    #             print("ADDED uid!")
    #
    #         self.init_sensors()
    #
    #     else:
    #         raise NotImplementedError(
    #             "service start not implemented on this platform"
    #         )

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

        # # Define upload and output folders
        # UPLOAD_FOLDER = date_time
        # send_flag = False
        #
        # if not os.path.exists(UPLOAD_FOLDER) and not send_flag:
        #     os.makedirs(os.path.join(UPLOAD_FOLDER))

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
