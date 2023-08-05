import platform
import socket
import getpass

def os_name():
    return "{0} {1} {2}".format(platform.system(), platform.release(), platform.version())

def machine_name():
    return socket.gethostname()

def get_username():
    return getpass.getuser()
