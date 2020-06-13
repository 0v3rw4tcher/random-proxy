#importing socket for socket port scanning and connection checking and requests for sending web requests
import socket,requests


#making a class
class HANDLER(object):

    #making values with type bool for checking conditions

    #socket is accessible
    SOCKET_ONLY=False

    #can connect to host with web requests
    WEB_ONLY=False

    #both conditions are true
    WEB_AND_SOCKET=False

    #both conditions are false
    UNCONNECTABLE=False

    #ssh is accessible:
    SSH=False

    #list of connectible ports
    SOCKETS=[]

    #main function
    def __init__(self,ip,port=[443,80,8080]):
        
        #try
        try:

            #go to list of ports
            for i in port:

                #make them int
                port[port.index(i)] = int(port[port.index(i)])

        #if you weren't able to make one of ports int
        except:

            #it means we have a wrong value
            raise TypeError("port must be int")

        #go to list of ports
        for i in port:

            #making a socket
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

            #setting timeout
            s.settimeout(2)

            #trying to connect to ip with ports
            p=s.connect_ex((ip,i))

            #if the connection was successful (this function returns 0 if there was no problem)
            if p == 0:

                #can connect to one of sockets
                self.SOCKET_ONLY = True

                #add the port to list of open ports
                self.SOCKETS.append(i)

            #if the connection was unsuccessful
            else:

                #don't give a fuck
                pass
        
        #if we had a empty list
        if self.SOCKETS == []:

            #it means we couldn't connect to ports
            self.SOCKET_ONLY = False
        
        #try
        try:

            #send a get request to host
            r=requests.get("http://{}".format(ip),timeout=6)

        #if the packet didn't reach the host
        except:

            #it means we can't connect to the host with web browsers
            self.WEB_ONLY = False

        #if the packet reached the host
        else:

            #if the page exist and there was no problem with host (host errors start with 5)
            if (r.status_code != 404) and (not str(r.status_code).startswith("5")):

                #it means we can connect to the host with web browsers
                self.WEB_ONLY = True

        #if both socket and web are accessible
        if self.SOCKET_ONLY and self.WEB_ONLY:

            #web and socket var is true
            self.WEB_AND_SOCKET = True

            #we can not "only" connect to socket or "only" to the web
            self.SOCKET_ONLY = False
            self.WEB_ONLY = False

        #if we could not reach the host with any method
        elif (not self.SOCKET_ONLY and not self.WEB_ONLY and not self.WEB_AND_SOCKET) == True:

            #it means the host is unconnectable
            self.UNCONNECTABLE = True

        #i spent two fucking days to fix the socket list bug , i can't explain it
        for i in self.SOCKETS:
            if self.SOCKETS.count(i) != 1:
                while self.SOCKETS.count(i) != 1:
                    if self.SOCKETS.count(i) == 1:
                        break
                    else:
                        self.SOCKETS.remove(i)
        
        #if there was 22 in open ports list
        if 22 in self.SOCKETS:

            #it means we can have ssh connection
            self.SSH = True

#you can use this for:

#[1] : IP scanners
#[2] : port scanners
#[3] : router finders
#[4] : ssh hunters
#[5] : os finders
