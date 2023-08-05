import os, json, datetime, time, socket, requests
from distutils import file_util
from importlib.machinery import SourceFileLoader

_base_dir = os.path.join(os.path.expanduser('~'), '.dynipman')

def load_config():
    if not os.path.exists(_base_dir):
        os.makedirs(_base_dir)
    if not os.path.exists(os.path.join(_base_dir, 'conf')):
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf.py')
        file_util.copy_file(config_file, os.path.join(_base_dir, 'conf'))
    confpy = SourceFileLoader('conf', os.path.join(_base_dir, 'conf')).load_module()
    return confpy

class Server():
    def __init__(self):
        config = load_config()
        
        self.config = config.SERVER
        self.key = config.SHARED_KEY
        self.addressbook = self.load_addressbook()
    
    def load_addressbook(self):
        result = {}
        try:
            with open(os.path.join(_base_dir, self.config['data_file']), 'r') as bookfile:
                result = json.loads(bookfile.read())
        except ValueError:
            pass
        finally:
            return result
        
    def save_addressbook(self):
        try:
            with open(os.path.join(_base_dir, self.config['data_file']), 'w') as bookfile:
                data = json.dumps(self.addressbook)
                bookfile.write(data)
            return True
        except ValueError:
            return False
        
    def update_address(self, name, new_info):
        self.addressbook[name] = new_info
        result = self.save_addressbook()
        if result:
            with open(os.path.join(_base_dir, 'log.txt'), 'a') as logfile:
                new_info['dtstamp'] = datetime.datetime.now().isoformat()
                data = json.dumps(new_info)+'\n'
                logfile.write(data)
        return result


class Client():
    def __init__(self):
        self.config = load_config()
        self.info = {
                     'host': socket.gethostname(),
                     'name': self.config.CLIENT['name']
                     }
        
    def report_ip(self):
        try:
            update = requests.post(self.config.SERVER['url']+'update/?code='+self.config.SHARED_KEY, data=json.dumps(self.info)).json()
            print(datetime.datetime.now())
            print(update)
            return update
        except requests.exceptions.ConnectionError:
            print(datetime.datetime.now())
            print('Connection Error!')
            print('  check config at '+os.path.join(_base_dir, 'conf'))
            print('  if the config is correct, then the server might be down.')
            return None
    
    def start(self):
        while True:
            self.report_ip()
            time.sleep(self.config.CLIENT['update_interval'])