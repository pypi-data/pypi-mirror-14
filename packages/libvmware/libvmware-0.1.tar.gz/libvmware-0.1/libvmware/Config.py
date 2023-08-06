import ConfigParser
from os.path import expanduser

home = expanduser('~')
conf_path = home + '/.config/libvmware.conf'
parser = ConfigParser.ConfigParser()
parser.read(conf_path)

host = parser.get('config', 'host')
user = parser.get('config', 'user')
password = parser.get('config', 'password')
port = parser.get('config', 'port')

settings = {
    'host': host,
    'user': user,
    'password': password,
    'port': port
}
