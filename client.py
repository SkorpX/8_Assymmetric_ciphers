import socket
import pickle

def secret_key(g,b,p):
    return g ** b % p

def ecrypt(msg, k):
    string=''
    for i in range(len(msg)):
        string+=chr(ord(msg[i])^k)
    return string

def send_msg(sock, msg, k):
    sock.send(pickle.dumps(ecrypt(msg, k)))

def recv_msg(sock, k):
	msg=ecrypt(pickle.loads(sock.recv(1024)), k)
	return msg

HOST = '127.0.0.1'
PORT = 8080
sock = socket.socket()
sock.connect((HOST, PORT))
print('Success!')
print('Write "exit" to disconnect')	

p, g, b = 3,5,7  
A = secret_key(g,b,p)
sock.send(pickle.dumps((g, A, p)))
B = pickle.loads(sock.recv(1024))
K = secret_key(B,b,p)
print('Secret key:',K)
while True: 
    msg = input('Your message: ')
    if msg !='exit':
        send_msg(sock, msg, K)
        print(recv_msg(sock, K))
    else:
        break
sock.close() 