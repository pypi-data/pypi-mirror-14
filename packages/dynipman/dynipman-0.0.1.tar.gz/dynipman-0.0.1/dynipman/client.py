from dynipman.components import Client

running_client = Client()

def run():
    running_client.start()
    
if __name__ == "__main__":
    run()