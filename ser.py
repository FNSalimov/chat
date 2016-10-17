import socket, time
from threading import Thread

def handler(cli_socket, cli_address):
    global socket_list, names_list
    print(cli_address, 'is connected')
    user_name = cli_socket.recv(1024).decode()
    names_list.append(user_name)
    for name in names_list:
        cli_socket.send(('->' + name).encode())
        time.sleep(0.1)
    for sock in socket_list:
        if sock != cli_socket:
            try:
                sock.send(('->' + user_name).encode())
            except ConnectionAbortedError:
                pass
    while 1:
        rec_data = cli_socket.recv(1024)
        print(len(socket_list))
        if not rec_data:
            break
        message = rec_data.decode()
        #client_address = str(cli_address[0]) + ':' + str(cli_address[1])
        #result = client_address + '->' + message
        result = user_name + ':' + message
        for sock in socket_list:
            if sock != cli_socket:
                try:
                    sock.send(result.encode())
                except ConnectionAbortedError:
                    pass
        #print(cli_address, ':', rec_data.decode())

ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser_socket.bind(('localhost', 5000))
ser_socket.listen(1)
print('server socket listen 5000th port')
socket_list = []
names_list = []
while 1:
    cli_socket, cli_address = ser_socket.accept()
    socket_list.append(cli_socket)
    cli_thread = Thread(target=handler, args=(cli_socket, cli_address))
    cli_thread.start()
ser_socket.close()
