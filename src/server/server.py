import asyncio
import logging

import message_handler

# Each client connection will get a unique CommanderServerProtocol
class CommanderServerProtocol(asyncio.Protocol):
    def __init__(self, name):
        self.name = name

    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(self.peername))
        self.transport = transport
        self.transport.write('Welcome to COMMANDER server {}'.format(self.name).encode())

    def data_received(self, data):
        message = data.decode()
        print('Data "{}" received from peer {}'.format(message, self.peername))
        response = message_handler.handle(message)
        self.transport.write(response.decode())

    def connection_lost(self, exception):
        print('Connection {} lost'.format(self.peername))

class Server:
    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name

    def start(self):
        print('Starting server {}'.format(self.name))
        loop = asyncio.get_event_loop()
        server = loop.create_server(lambda: CommanderServerProtocol(self.name), self.host, self.port)
        server_loop = loop.run_until_complete(server)

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        server_loop.close()
        loop.run_until_complete(server_loop.wait_closed())
        loop.close()

def main():
    server = Server('localhost', 9999, 'root')
    server.start()

if __name__ == '__main__':
    main()