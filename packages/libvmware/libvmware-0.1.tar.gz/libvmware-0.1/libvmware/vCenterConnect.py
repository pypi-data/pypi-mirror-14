from __future__ import print_function
from pyVim.connect import SmartConnect, Disconnect
from Config import settings
import atexit
import ssl

def connect():
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE

    si = SmartConnect(
        host=settings['host'],
        user=settings['user'],
        pwd=settings['password'],
        port=settings['port'],
        sslContext=context
    )
    atexit.register(Disconnect, si)

    return si