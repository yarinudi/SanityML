from time import sleep

from jnius import autoclass

PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)


while True:
    print("service running.....")
    sleep(5)

# """p4a service using oscpy to communicate with main application."""
# from random import sample, randint
# from string import ascii_letters
# from time import sleep
#
# from jnius import autoclass
#
# from oscpy.server import OSCThreadServer
# from oscpy.client import OSCClient
#
# CLIENT = OSCClient('localhost', 3002)
#
#
# def ping(*_):
#     """answer to ping messages"""
#     CLIENT.send_message(
#         b'/message',
#         [
#             ''.join(sample(ascii_letters, randint(10, 20)))
#             .encode('utf8'),
#         ],
#     )
#
#
# SERVER = OSCThreadServer()
# SERVER.listen('localhost', port=3000, default=True)
# SERVER.bind(b'/ping', ping)
# while True:
#     print("service running.....")
#     sleep(1)