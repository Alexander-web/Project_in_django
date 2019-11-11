import socket

def send_and_return(data_to_send):
        sock = socket.socket()
        port = 33333
        sock.connect(("127.0.0.1", port))
        data = b""
        
        sock.send(bytes(data_to_send,'utf-8'))
        
        tmp=True
        while tmp:   
                tmp = sock.recv(1024)
                data += tmp
                if '\n' in tmp.decode('utf-8'):
                        break
        sock.send(bytes('@stop','utf-8'))
        sock.close()
        return data.decode('utf-8')
