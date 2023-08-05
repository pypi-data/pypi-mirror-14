from dynipman.components import Client

client = Client()

def device_info():
    print("Client host: "+client.info['host'])
    print("Client name: "+client.info['name'])
    return client.info
    
def report_ip():
    update = client.report_ip()
    return update

def show_menu():
    print('\n-Menu---------------------------')
    print('\n1. Show Device Info')
    print('2. Report IP Address to Server')
    print('\n type "exit" to exit ')
    print('--------------------------------')
    return {
            '1': device_info,
            '2': report_ip,
            }

def run():
    KEEP_ALIVE = True
    print('=HELLO==================')
    print(' starting dynipman client ')
    print('========================')
    while KEEP_ALIVE:
        menu = show_menu()
        uin = input(' >> ')
        if uin in menu:
            menu[uin]()
        KEEP_ALIVE = not (uin == 'exit')
    print('========================')
    print(' quitting dynipman client ')
    print('====================BYE=')
    return

if __name__ == "__main__":
    run()