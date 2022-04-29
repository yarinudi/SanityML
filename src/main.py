# coding: utf8
__version__ = '0.2'

import os
import uuid
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform

from jnius import autoclass

from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer

from plyer import email, accelerometer

SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.kivy.oscservice',
    servicename=u'Pong'
)

KV = '''
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: '30sp'
        Button:
            text: 'start service'
            on_press: app.start_service()

    ScrollView:
        Label:
            id: label
            size_hint_y: None
            height: self.texture_size[1]
            text_size: self.size[0], None

    BoxLayout:
        size_hint_y: None
        height: '30sp'
        Button:
            text: 'ping'
            on_press: app.send()
        Button:
            text: 'clear'
            on_press: label.text = ''
        Label:
            id: date

'''


class ClientServerApp(App):
    def __init__(self):
        # self.mActivity = None
        # self.root = None
        # self.client = None
        # self.server = None
        # self.service = None

        self.user_id = str(uuid.uuid1())
        print('Current User ID: ', self.user_id)

        # write uid to txt file
        with open('data.txt', mode='a') as f:
            f.writelines(f"{self.user_id}\n\n")
            print("ADDED uid!")

        self.init_sensors()
        # self.email()

    def build(self):
        self.service = None
        # self.start_service()

        self.server = server = OSCThreadServer()
        server.listen(
            address=b'localhost',
            port=3002,
            default=True,
        )

        server.bind(b'/message', self.display_message)
        server.bind(b'/date', self.date)

        self.client = OSCClient(b'localhost', 3000)
        self.root = Builder.load_string(KV)
        return self.root

    def start_service(self):
        if platform == 'android':
            service = autoclass(SERVICE_NAME)
            self.mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
            argument = ''
            service.start(self.mActivity, argument)
            self.service = service

        elif platform in ('linux', 'linux2', 'macos', 'win'):
            from runpy import run_path
            from threading import Thread
            self.service = Thread(
                target=run_path,
                args=['src/service.py'],
                kwargs={'run_name': '__main__'},
                daemon=True
            )
            self.service.start()
        else:
            raise NotImplementedError(
                "service start not implemented on this platform"
            )

    def send(self, *args):
        self.client.send_message(b'/ping', [])

    def display_message(self, message):
        if self.root:
            self.root.ids.label.text += '{}\n'.format(message.decode('utf8'))

    def date(self, message):
        if self.root:
            self.root.ids.date.text = message.decode('utf8')

    def init_sensors(self):
        """ setup sensors """
        try:
            accelerometer.enable()

        except:
            print('cant enable accelerometer')

        # setup timer to update sensors
        Clock.schedule_interval(self.save_sensors, 1.0/60.0)

    def save_sensors(self, dt):
        """ write sensors' data to txt file """
        try:
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
            print("ADDED sensors data!")

    # def email(self):
    #     try:
    #         email.send(recipient='yarin1997udi@gmail.com', subject='Thanks!', text='Enjoyed your lesson')
    #     except:
    #         print('cant email')


if __name__ == '__main__':
    ClientServerApp().run()
