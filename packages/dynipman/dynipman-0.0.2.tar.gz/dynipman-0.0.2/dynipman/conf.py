# Change this secret to something only you know
SHARED_KEY = 'ThisIsNotASecureSecret'

SERVER = {
          'url': 'http://localhost:7883/', # Change this to your public domain host
          'port': 7883,
          'data_file': 'addressbook.json' # You can find this file in ~/.dynipman/
          }

CLIENT = {
          'name': 'my-home-ubuntu', # This is the name with which you would identify client machines
          'update_interval': 60 # Interval at which the client reports to server
          }