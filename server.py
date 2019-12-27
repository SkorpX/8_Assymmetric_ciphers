import socket
import pickle
from random import randint

HOST = '127.0.0.1'
PORT = 8080
def secret_key(g,a,p):
    return g**a%p
def ecrypt(msg, key):
    string = ''
    for i in range(len(msg)):
        string +=chr(ord(msg[i])^key)
    return string
def send_msg(conn, msg, key):
    conn.send(pickle.dumps(ecrypt(msg, key)))
def recv_msg(conn, key):
	msg= ecrypt(pickle.loads(conn.recv(1024)), key)
	return msg

sock = socket.socket()        
sock.bind((HOST,PORT))
print('Your port:',PORT)
sock.listen(0)			
sock.setblocking(1)
conn, addr = sock.accept()

b = randint(1, 32)
msg = conn.recv(1024)
g, A, p = pickle.loads(msg)

B = secret_key(g,b,p)
conn.send(pickle.dumps(B))

K = secret_key(A,b,p)
print('Secret key:',K)
while True:
	try:
		msg = recv_msg(conn, K)
		print(msg)
		send_msg(conn, 'Success', K)
	except:
		break
conn.close() 