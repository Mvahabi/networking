# HTTP Server Script

This Python script is a simple HTTP server that generates a basic HTTP response for a specified file in a given directory. The server supports different file types and provides essential header information, such as content length, content type, date, and last modified.

## Functionality

The script takes a port number and a file path as input arguments. It then checks the port number against predefined ranges, then it checks if the given directory exists in the operating system. In a seperate terminal, the user will request a GEt opertaion and upon succesfull execution will prints the HTTP response of the requested file in two seperate text and csv file.

## Usage

To run the script, execute it from the command line with the following arguments:

```bash
python3 part2.py -p <port_number> -d <path_to_directory>
```
then, open a second terminal and run a HTTP GET request like such:
```bash
wget/curl http://127.0.0.1:49151/<file in the directory>
```

## Port Handling
Any ports between 0 and 65535 are accepted and any other ones are rejected and results in a termination of the program

## HTTP Responses
1. Resource not Available errors: If requested resource is not present in the webserver’s file
system return 404 File Not Found
2. Unsupported HTTP Methods: You are only required to handle HTTP GET requests.
Return 501 Not Implemented for any other request methods.
3. Unsupported HTTP Version: You are only required to handle HTTP 1.1 requests. Return
505 HTTP Version Not Supported
4. Succesfull methods, supported HTTP version, file exists: Return 200 OK

