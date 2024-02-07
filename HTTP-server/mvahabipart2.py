import os
import sys
import datetime
import socket
import csv

'''
Honor Code:
https://www.geeksforgeeks.org/socket-programming-python/# 
https://docs.python.org/3/library/csv.html

'''

# closes the connection 
def end(bwrit, conn, param_add, param_sock):
    bwrit = bwrit
    conn.close()
    sys.stdout.write(f"Connection to {param_add}, {param_sock} is closed\n")
    
# http status line
def status(status):
    msg = ""
    if status == 404:
        msg = "HTTP/1.1 404 Not Found\r\n"
    elif status == 501:
        msg = "HTTP/1.1 501 Not Implemented\r\n"
    elif status == 505:
        msg = "HTTP/1.1 505 HTTP Version Not Supported\r\n"
    elif status == 200:
        msg = "HTTP/1.1 200 OK" 
    return msg

# csv status line
def csv_status(status):
    msg = ""
    if status == 404:
        msg = "HTTP/1.1 404 Not Found"
    elif status == 501:
        msg = "HTTP/1.1 501 Not Implemented"
    elif status == 505:
        msg = "HTTP/1.1 505 HTTP Version Not Supported"
    elif status == 200:
        msg = "HTTP/1.1 200 OK"
    return msg

# checks for 
def http_response(port, conn, param_add, param_sock, method, directory, url, file_name, http_version, csv_status_line, bwrit):
    time_now = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    No_error = True
    num = 0
    if os.path.exists(directory + '/' + file_name) == False:
        No_error = False
        num = 1
        status_line = status(404)
        csv_status_line = csv_status(404)
        date = ("Date: " + time_now +"\r\n")
        conn_close = "Connection: closed\r\n\r\n"
        header_lines = (status_line + date + conn_close)
        # This converts the string into a sequence of bytes using a specified encoding (usually UTF-8)
        response = status_line.encode() + date.encode()
        conn.send(response)
        end(bwrit, conn, param_add, param_sock)

    elif method.upper() != 'GET':
        No_error = False
        num = 1
        status_line = status(501)
        csv_status_line = csv_status(501)
        date = ("Date: " + time_now +"\r\n")
        conn_close = "Connection: closed\r\n\r\n"
        header_lines = (status_line + date + conn_close)
        response = status_line.encode() + date.encode()
        conn.send(response)
        end(bwrit, conn, param_add, param_sock)

    elif http_version != "HTTP/1.1":
        No_error = False
        num = 1
        status_line = status(505)
        csv_status_line = csv_status(505)
        date = ("Date: " + time_now +"\r\n")
        conn_close = "Connection: closed\r\n\r\n"
        header_lines = (status_line + date + conn_close)
        response = status_line.encode() + date.encode()
        conn.send(response)
        end(bwrit, conn, param_add, param_sock)
    
    if method.upper() == 'GET' and http_version == "HTTP/1.1" and No_error == True:
        mime_types = {
            "csv": "text/csv", 
            "png": "image/png", 
            "jpg": "image/jpeg", 
            "gif": "image/gif", 
            "zip": "application/zip", 
            "txt": "text/plain", 
            "html": "text/html", 
            "doc": "application/msword", 
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }
        
        input_file = open(directory+'/'+file_name, 'rb')
        data = input_file.read()
        input_file.close()
        
        size = os.path.getsize(directory+'/'+file_name)
        extension = file_name.split('.')[-1]
        file_type = mime_types[extension]
        modified = datetime.datetime.utcfromtimestamp(os.path.getmtime(directory+'/'+file_name)).strftime('%a, %d %b %Y %H:%M:%S GMT')
        status_line = status(200)
        csv_status_line = csv_status(200)

        header_lines = [
            (status_line),
            (f"Content-Length: {size}"),
            (f"Content-Type: {file_type}"),
            (f"Date: {time_now}"),
            (f"Last-Modified: {modified}"),
            "",
            "",
        ]
        
        header_lines = "\r\n".join(header_lines)
        response = header_lines.encode() + data
        conn.send(response)
        bwrit = size

        end(bwrit, conn, param_add, param_sock)
    
    txtfile = open('mvahabiHTTPResponse.txt', 'a', newline = '\n')
    txtfile.write(header_lines)
    # if num == 1:
    #     txtfile.write()
    txtfile.close()

    csvfile = open('mvahabiSocketOutput.csv', 'a', newline='\n')
    writer = csv.writer(csvfile)
    writer.writerow(["Client request server", "4-Tuple:", "127.0.0.1", port,
    param_add, param_sock, "Requested URL", url, csv_status_line, "Bytes sent:",bwrit])
    csvfile.close()


def main():
    
    if len(sys.argv) != 5:
        sys.stderr.write("Input Error. Usage: -p <port#> -d <path-to-file>\n")
        exit()
        
    # input:
    # part1.py -p 100 -d /home/username/web
    port = int(sys.argv[2])
    directory = sys.argv[4]
    
    if port <=0 or port > 65535:
        sys.stderr.write("Error: Invalid port number.\n")
        exit()

    if not os.path.exists(directory):
        sys.stderr.write("Error: Directory not found.\n")
        exit()
        
    '''
    AF_INET specifies that the socket will use IPv4 addressing.
    SOCK_STREAM indicates that this is a TCP socket.
    '''
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sys.stdout.write(f"Welcome socket created: 127.0.0.1, {port}\n")
    sock.bind(('127.0.0.1', port))
    sock.listen()
    
    while True:
        conn, adr = sock.accept()
        
        param_add, param_sock = conn.getpeername() # It's getting the address information of the connected client.
        request = conn.recv(1024)
        sys.stdout.write(f"Connection socket created: {param_add}, {param_sock}\n" )
        
        if request is not None:
            req_parse = request.decode().split('\r\n')  
            method, url, http_version = req_parse[0].split()
            file_name = url.split('/')[-1]
                        
            bwrit = 0
            csv_status_line = ""
            header_lines = ""
            
            http_response(port, conn, param_add, param_sock, method, directory, url, file_name, http_version, csv_status_line, bwrit)
    
if __name__ == '__main__':
    main()
# lsof -i :8000
