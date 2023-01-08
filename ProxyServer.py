from socket import *
import sys


buffer = []
size = 2**32
blocked_URLs = [
    'www.facebook.com\n',
    'www.youtube.com\n',
    'www.instagram.com\n'
]
file = open("./" + 'blocked_URLs',"w")
file.write("".join(blocked_URLs))
file.close()


if len(sys.argv) < 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)


# Fill in start.
proxyIP = 'localhost'
proxyPort = 8888
print(f'starting up on {proxyIP} port {proxyPort}')
tcpSerSock.bind((proxyIP, proxyPort))
tcpSerSock.listen(1)
# Fill in end.


while 1:
    # Start receiving data from the client
    print('\n\nReady to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)


    # Fill in start.
    message = tcpCliSock.recv(size).decode()
    # Fill in end.
    
    if message != '':
        print(message)

        # Extract the filename from the given message
        print(message.split()[1])
        filename = message.split()[1].partition("/")[2]
        print(filename)
        fileExist = "false"
        filetouse = "/" + filename
        print(filetouse)
    try:
        if message == '':
            raise IOError()

        blocked = open('blocked_URLs', "r")
        URLs = blocked.readlines()
        if (filename+'\n') in URLs:
            filename = 'error_page.org'


        # Check whether the file exist in the cache
        f = open(filename, "r")
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.1 200 OK\r\n".encode())
        tcpCliSock.send("Content-Type:text/html\r\n".encode())


        # Fill in start.
        output = []
        for i in range(len(outputdata)):
            if i+1 < len(outputdata):
                if 'Transfer-Encoding' in outputdata[i+1]:
                    output.extend(outputdata[i:len(outputdata)])
                    break
                if outputdata[i] != '\n' or outputdata[i+1] == '\n':
                    output.append(outputdata[i])
        tcpCliSock.sendall(("".join(output)).encode())
        # Fill in end.


        print ('Read from cache')
        # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver


            # Fill in start.
            c = socket(AF_INET, SOCK_STREAM)
            # Fill in end.            


            hostn = filename.replace("www.","",1)
            print(hostn)
            try:
                # Connect to the socket to port 80


                # Fill in start.
                c.connect((hostn, 80))
                # Fill in end.


                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                c.sendall(f"GET / HTTP/1.1\r\nHost: {filename}\r\n\r\n".encode())
                # fileobj = c.makefile('r', None)
                # fileobj.write("GET "+"http://" + filename + " HTTP/1.0\n\n")
                # Read the response into buffer


                # Fill in start.
                buffer.append(c.recv(size).decode())
                # Fill in end.


                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./" + filename,"w")


                # Fill in start.
                tcpCliSock.sendall(buffer[-1].encode())
                tmpFile.write(buffer[-1])
                tmpFile.close()
                # Fill in end.


            except Exception as e:
                print(e)
                print("Illegal request")
        else:
            # HTTP response message for file not found


            # Fill in start.
            tcpCliSock.send("HTTP/1.1 404 Not Found\r\n".encode())
            print('file not found')
            # Fill in end.


    # Close the client and the server sockets
    tcpCliSock.close()


# Fill in start.
tcpSerSock.close()
# Fill in end.