# https://www.geeksforgeeks.org/python/creating-a-proxy-webserver-in-python-set-1/
# test it with: curl -x 'http://localhost:10000' 'http://httpforever.com'
import socket as s
import signal
#import sys
import connect_to_site
import helpers
import asyncio
import functools

serverPort = 10000

def ask_exit(signame):
    print("got signal %s: exit" % signame)
    loop.stop()

async def server():
    loop = asyncio.get_event_loop()
    serverSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
    # https://stackoverflow.com/questions/6380057/address-already-in-use-error-when-binding-a-socket-in-python
    serverSocket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)

    # https://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python
    # does not work in async version
    #def signal_handler(sig, frame):
        #serverSocket.close()
        #sys.exit(0)
    #signal.signal(signal.SIGINT, signal_handler)

    print('Proxy running...')

    with serverSocket:
        while 1:
            # "client" is the client of the proxy, for example browser or curl
            clientSocket, _ = await loop.sock_accept(serverSocket) #serverSocket.accept()
            request = await loop.sock_recv(clientSocket, 1024) #clientSocket.recv(1024)
            message_str = request.decode()
            webserver, port = helpers.extract_server_and_port(message_str)
            print('Received client request for destination:', webserver, port)
            
            # send the request to the destination
            data = await connect_to_site.aconnect(webserver, port)

            # send to browser/client
            await loop.sock_sendall(clientSocket, data) #clientSocket.send(data)
            print('Sent response of the destination to the client')

            clientSocket.close()
            print('Client socket closed')
            print('----------------')

# https://docs.python.org/3/library/asyncio-eventloop.html#set-signal-handlers-for-sigint-and-sigterm
async def main():
    loop = asyncio.get_running_loop()
    loop.create_task(server())
    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(
            getattr(signal, signame),
            functools.partial(ask_exit, signame, loop))

if __name__ == '__main__':
    # https://stackoverflow.com/questions/46727787/runtimeerror-there-is-no-current-event-loop-in-thread-in-async-apscheduler
    loop = asyncio.new_event_loop() #loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(server())
    # https://stackoverflow.com/questions/23313720/asyncio-how-can-coroutines-be-used-in-signal-handlers
    #loop.add_signal_handler(getattr(signal, 'SIGINT'), lambda signame='SIGINT': asyncio.create_task(ask_exit(signame)))
    loop.run_forever()
    #asyncio.run(main())