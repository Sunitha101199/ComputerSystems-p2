'''
    Disclaimer
    tiny httpd is a web server program for instructional purposes only
    It is not intended to be used as a production quality web server
    as it does not fully in compliance with the 
    HTTP RFC https://tools.ietf.org/html/rfc2616

'''
import socket
import sys
import os
import mimetypes

class HTTPServer:
    '''
        Remove the pass statement below and write your code here
    '''
    def __init__(self, localhost, port_number):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = (localhost, port_number)
        print(sys.stderr, 'starting up on %s port %s' % server_address)
        sock.bind(server_address)
        
        # Listen for incoming connections
        sock.listen()
        print("Current Working Directory: "+os.getcwd())
        print("Length of the directory: "+str(len(os.getcwd())))
        
        while True:
            # Wait for a connection
            print(sys.stderr, 'waiting for a connection')
            connection, client_address = sock.accept()
            message = connection.recv(1024).decode()
            print(message)
            getmsg = message.splitlines()
            print(getmsg,"getmsg")
            cdirectory = getmsg[0].split(" ")[1]
            print(cdirectory,"cd")
            fname = cdirectory.split("/")[-1]
            print(fname,"frequest")#
             
            data_url = os.getcwd()+cdirectory
            print(data_url,"!!!!!")
            # print(fname)

            if(cdirectory=="/www"):
                body = ""
                for files in os.listdir(cdirectory.split("/")[1]):
                    body+=f'<a href="{os.path.join(cdirectory.split("/")[1],files)}">{files}</a><br>'
                head = f'HTTP/1.1 200 OK \nContent-Type: text/html\nContent-Length: {str(len(body))} \nConnection: close\n\n'
                print(head)
                connection.sendall((head+body).encode())
                   
             # checking if it is a file        
            elif os.path.isfile(data_url):
                file = open(data_url, 'rb')
                file_data = file.read()
                file.close()
                headers = "HTTP/1.1 200 OK"+'\r\n'
                headers += f"Content-Type: {(mimetypes.MimeTypes().guess_type(fname)[0])}"+'\r\n'
                headers += "Content-Length: %s "%str(len(file_data))+'\r\n'
                headers += "Connection: close "+'\r\n'
                headers += "\n"
                headers = headers.encode()
                headers += file_data
                connection.sendall(headers)
                
            elif os.path.isdir(data_url) and fname!="":
                body=""
                # print(os.path.join(data_url,file),"printing")
                for file in os.listdir(cdirectory[1:]):
                    print("printing")
                    body+=f'<a href="{os.path.join(data_url,file)}">{file}</a><br>'
                    print(os.path.join(data_url,file))
                head = f'HTTP/1.1 200 OK \nContent-Type: {(mimetypes.MimeTypes().guess_type(fname)[0])}\nContent-Length: {str(len(body))} \nConnection: close\n\n'
                print(head)
                connection.sendall((head+body).encode())

            else:
                body = "<h1>Developing Web Server</h1><br>"+'\r\n'
                headers = ""
                headers += "HTTP/1.1 200 OK"+'\r\n'
                headers += "Content-Type: text/HTML "+'\r\n'
                headers += "Content-Length: %s "%str(len(body))+'\r\n'
                headers += "Connection: close "+'\r\n'
                headers += "\n"
                data = bytes(headers+body,'utf-8')
                connection.sendall(data)
            # msg = connection.recv(1024).decode()    
            connection.close()
            


def main():
    # test harness checks for your web server on the localhost and on port 8888
    # do not change the host and port
    # you can change  the HTTPServer object if you are not following OOP
    HTTPServer('127.0.0.1', 8888)

if __name__ == "__main__":
    main()
