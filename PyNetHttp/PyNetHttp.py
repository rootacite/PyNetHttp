
# coding:utf-8

#coding=gbk

import socket

from multiprocessing import Process

from http import server
from io import StringIO
 



def handle_client(client_socket):
   
    request_data = client_socket.recv(4096)
    
    request_n=str(request_data,"utf-8").split('\n');
    sv="";
    it=iter(request_n)
    for i in it:
        sv+=i;
        sv+="\n"
    print("request data:", sv)
     
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: ShiYuan Li\r\n"
    response_body = "<h1>Python HTTP Test</h1>"
    response = response_start_line + response_headers + "\r\n" + response_body

    
    client_socket.send(bytes(response, "utf-8"))

    
    client_socket.close()

def get_host_ip():
   
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()

    return ip
if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = get_host_ip();
    print(host)
    server_socket.bind(("0.0.0.0", 8000))
    server_socket.listen(128)

    while True:
        client_socket, client_address = server_socket.accept()
        print("[%s, %s]User connect" % client_address)
        handle_client_process = Process(target=handle_client, args=(client_socket,))
        handle_client_process.start()
        client_socket.close()