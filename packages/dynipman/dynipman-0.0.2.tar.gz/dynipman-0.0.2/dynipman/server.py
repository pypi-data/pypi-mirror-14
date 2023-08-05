import json
from dynipman.components import Server
import tornado.ioloop
import tornado.web
    
running_server = Server()

def is_authorized(handler, server):
    code = handler.get_query_arguments('code')
    if len(code) > 0:
        return (code[0] == server.key)
    else:
        return False

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if is_authorized(self, running_server):
            message = '\n'+json.dumps(running_server.addressbook)
            self.write(message)
            print("Main - Authorized")
        else:
            self.write("Unauthorized")
            print("Main - UNAUTHORIZED")
        print(repr(self.request))
        print(self.request.body)
        
class UpdateHandler(tornado.web.RequestHandler):
    def post(self):
        client_data = json.loads(self.request.body.decode())
        if is_authorized(self, running_server):
            print('Update - Authorized')
            client_info = {
                           'ip': self.request.remote_ip,
                           'host': client_data['host'],
                           'name': client_data['name'],
                           }
            print("IP Update Request from "+client_info['name'])
            print('    Client host : '+client_info['host'])
            print('    Client IP   : '+client_info['ip'])
            saved = running_server.update_address(client_info['name'], client_info)
            
            if saved:
                response = { 'result': 'success',
                            'data': 'Update saved successfully',
                            }
            else:
                response = { 'result': 'failure',
                            'data': 'Failed to save data',
                            }
        else:
            print('Update - UNAUTHORIZED')
            response = { 'result': 'failure',
                         'data': 'Unauthorized Access',
                        }
        print(repr(self.request))
        print(self.request.body)
        self.write(response)
        
def make_app():
    print('========================')
    print(' starting dynipman server ')
    print('========================')
    return tornado.web.Application([ (r'/$', MainHandler),
                                     (r'/update/$', UpdateHandler), 
                                    ])
    
def run():
    app = make_app()
    app.listen(running_server.config['port'])
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    run()