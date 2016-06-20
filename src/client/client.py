import asyncio
import json

import commands

class ClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.state = 'local'

    def data_received(self, data):
        print('Server: "{}"'.format(data.decode()))
        
        command_string = None
        command = {}
        while not command_string or not commands.is_valid(command):
            command_string = input('>')
            command = commands.parse(command_string)
            if command_string and not commands.is_valid(command):
                print('Invalid command: {}'.format(command_string))
                print_commands()
        
        self.transport.write(json.dumps(command).encode())
        
    def connection_lost(self, exc):
        print('The server closed the connection')
        self.transport.close()

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        loop = asyncio.get_event_loop()
        connection = loop.create_connection(ClientProtocol, self.host, self.port)
        loop.run_until_complete(connection)

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()

def print_commands():
    print('Commands:')
    print('[l]ist, [j]oin <room name>, [c]reate <room name>, [q]uit')

def main():
    client = Client('127.0.0.1', 9999)
    client.start()
    
if __name__ == '__main__':
    main()