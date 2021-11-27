#coding=gbk

import threading
import time

import socket

from multiprocessing import Process

from http import server
from io import StringIO
 
Data = {'Question': "你妈死了吗", 'A1': "死了", 'A2': "没死",'A3': "快死了",'A4': "快复活了"}
Statistical= {'A1': 0, 'A2': 0,'A3': 0, 'A4': 0}

Forbidden = []

def handle_client(client_socket):
   
    request_data = client_socket.recv(4096)
    
    request_n=str(request_data,"utf-8").split('\n');
    sv="";
    it=iter(request_n)
    for i in it:
        sv+=i;
        sv+="\n"
    print("request data:", sv) 
     
    response_start_line = "HTTP/1.1 200 Success\r\n"
    response_headers = "Server: ShiYuan Li\r\n"
    response_body = ""
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

HOST = get_host_ip()
PORT = 4468

us = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

us.bind((HOST, PORT))

def ControlThread():
    while True:
        data, address = us.recvfrom(1024)

        tx=str(data,encoding="utf-8")
        print(address)
        rtx=tx.split(' ')
        if rtx[0]=='show':
            print(Data);
        if rtx[0]=='setq':
            if len(rtx)<2:
                print("Error : SE");
                continue;
            Data['Question']=rtx[1];
            print(Data)
            

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = get_host_ip();
    print(host)
    server_socket.bind((host, 8000))
    server_socket.listen(128)

    th = threading.Thread(target=ControlThread);
    #th.start()
    #th.join()
    while True:
        client_socket, client_address = server_socket.accept()
        print("[%s, %s]User connect" % client_address)
        handle_client_process = Process(target=handle_client, args=(client_socket,))
        handle_client_process.start()
        client_socket.close()