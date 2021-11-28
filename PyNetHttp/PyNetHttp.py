#coding=gbk

import threading
import time

import json
import socket

from multiprocessing import Process

from http import server
from io import StringIO
 
Data = {'Question': "Q1", 'A1': "A1", 'A2': "A2",'A3': "A3",'A4': "A4"}
Statistical= {'A1': [], 'A2': [],'A3': [], 'A4': []}

def get_host_ip():
   
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()

    return ip


        

def handle_client(client_socket):
    request_data = client_socket.recv(4096)
    response_body="";
    response_start_line = "HTTP/1.1 200 Success\r\n"
    request_n=str(request_data,"utf-8").split('\n');

    not_retuen_404 = False;

    sv="";
    it=iter(request_n)
    for i in it:
        sv+=i;
        sv+="\n"
    print("request methon:","<"+request_n[0][0:4]+">")
    try:
     if request_n[0][0:4]=="POST":
         print("Command:",request_n[len(request_n)-1])
         tx=request_n[len(request_n)-1]
         rtx=tx.split(' ')
         
         if rtx[0]=='set':
             if len(rtx)<6:
                 print("Error : SE");
                 raise;
             with open("Data.json", 'r') as f_obj:
                DataJson=json.load(f_obj)
                DataJson["Question"]=rtx[1];
                DataJson["A1"]=rtx[2];
                DataJson["A2"]=rtx[3];
                DataJson["A3"]=rtx[4];
                DataJson["A4"]=rtx[5];
             with open("Data.json", 'w') as f_obj:
                json.dump(DataJson,f_obj)
             with open("Data.json", 'r') as f_obj:
                DataJson=json.load(f_obj)
                print(DataJson)
                response_body=str(DataJson)
             

             with open("Statistical.json", 'r') as f_obj:
                DataJson=json.load(f_obj)
                DataJson['A1'].clear()
                DataJson['A2'].clear()
                DataJson['A3'].clear()
                DataJson['A4'].clear()
                
             with open("Statistical.json", 'w') as f_obj:
                json.dump(DataJson,f_obj)
         elif rtx[0]=='ans':
             if len(rtx)<3:
                 print("Error : SE");
                 raise;
             
             with open("Statistical.json", 'r') as f_obj:
                DataJson=json.load(f_obj)
                if (rtx[2] in DataJson['A1']) or (rtx[2] in DataJson['A2']) or (rtx[2] in DataJson['A3']) or (rtx[2] in DataJson['A4']):
                  not_retuen_404=True;
                  response_body="SS"
                  raise;
                if rtx[1]=='A1':
                    DataJson['A1'].append(rtx[2])
                elif rtx[1]=='A2':
                    DataJson['A2'].append(rtx[2])
                elif rtx[1]=='A3':
                    DataJson['A3'].append(rtx[2])
                elif rtx[1]=='A4':
                    DataJson['A4'].append(rtx[2])
                
             with open("Statistical.json", 'w') as f_obj:
                json.dump(DataJson,f_obj)
             with open("Statistical.json", 'r') as f_obj:
                DataJson=json.load(f_obj)
                print(DataJson)
                response_body=str(DataJson)
         else:
             raise;
     if request_n[0][0:4]=="GET ":
         print("Command:",request_n[len(request_n)-1])
         tx=request_n[len(request_n)-1]
         rtx=tx.split(' ')
         if True:
             with open("Data.json", 'r') as f_obj:
                DataJson=json.load(f_obj)
                print(DataJson)
                response_body=str(DataJson)
             with open("Statistical.json", 'r') as f_obj:
                DataJson=json.load(f_obj)
                print(DataJson)
                response_body+='\n';
                response_body+=str(DataJson)
     

    except:
        if not(not_retuen_404):
          response_start_line = "HTTP/1.1 400 Bad Request\r\n"
  
    response_headers = "Server: ShiYuan Li\r\n"
    response = response_start_line + response_headers + "\r\n" + response_body

    print("response:",response)
    client_socket.send(bytes(response, "utf-8"))

    
    client_socket.close()
           

if __name__ == "__main__":
    with open("Data.json", 'w+') as f_obj:
        json.dump(Data, f_obj)
    with open("Statistical.json", 'w+') as f_obj:
        json.dump(Statistical, f_obj)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = get_host_ip();
    print(host)
    server_socket.bind((host, 8000))
    server_socket.listen(128)

    
    while True:
        client_socket, client_address = server_socket.accept()
        print("[%s, %s]User connect" % client_address)
        handle_client_process = Process(target=handle_client, args=(client_socket,))
        handle_client_process.start()
        client_socket.close()