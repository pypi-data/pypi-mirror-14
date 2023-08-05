import json
from dynipman.components import Server
import tornado.ioloop
from tornado.web import Application, URLSpec, RequestHandler
    
running_server = Server()

def is_authorized(handler, server):
    if handler.request.method == 'GET':
        code = handler.get_query_arguments('code')
    elif handler.request.method == 'POST':
        post_data = json.loads(handler.request.body.decode())
        code = [post_data['code']]
    if len(code) > 0:
        return (code[0] == server.key)
    else:
        return False

class MainHandler(RequestHandler):
    def get(self):
        context = {
                   'test': 'TESTING'
                   }
        self.render('index.html', title='dynipman', context=context)
        
    def post(self):
        if is_authorized(self, running_server):
            message = json.dumps(running_server.addressbook)
            self.write(message)
            print("Main - Authorized")
        else:
            self.write("Unauthorized")
            print("Main - UNAUTHORIZED")
#         print(repr(self.request))
#         print(self.request.body)
        
class UpdateHandler(RequestHandler):
    def post(self):
        if is_authorized(self, running_server):
            print('Update - Authorized')
            post_data = json.loads(self.request.body.decode())
            client_info = {
                           'ip': self.request.remote_ip,
                           'host': post_data['host'],
                           'name': post_data['name'],
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
#         print(repr(self.request))
#         print(self.request.body)
        self.write(response)
        
def make_app():
    print('========================')
    print(' starting dynipman server ')
    print('========================')
    return Application([ URLSpec(r'/$', MainHandler, name='main'),
                         URLSpec(r'/update/$', UpdateHandler, name='update'), 
                        ])
    
def run():
    app = make_app()
    app.listen(running_server.config['port'])
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    run()