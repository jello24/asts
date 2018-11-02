# myTraceRoute.py
# Author: Jan Louis Evangelista, 28912146
# Description: 
# The program implements basic Traceroute functionality
# 1) It displays the router's info as it passes it
# 2) It calculates and displays 3 RTT values (in ms) for 
#    each router, on the same line as the router info
#    If the RTT cannot be calculated within 4 s, display an *
# 3) It displays a terminating message when max number of 30 hops is reached
# References used:
#   https://adayinthelifeof.nl/2010/07/30/creating-a-traceroute-program-in-php/
#   https://web.archive.org/web/20160625004717/https://blogs.oracle.com/ksplice/entry/learning_by_doing_writing_your

import sys
from socket import *
import random

hostname = sys.argv[1] # Get the host name from the argument list (python myTraceRoute.py google.ca)
print("Start Trace")

destAddr = gethostbyname(hostname) # Find the host address and turn it into IP
destPort = 33434

print("Traceroute for: " + hostname + " at IP: " + destAddr + ":" + str(destPort))

# Get protocol constants for socket creation
icmp = getprotobyname('icmp') # Received packets are ICMP messages
udp = getprotobyname('udp') # Sent packets are UDP packets

max_hops = 31 # Set max hops to 30

for ttl in range(1, max_hops):
    # Create the connection
    sendSocket = socket(AF_INET, SOCK_DGRAM, udp)
    recvSocket = socket(AF_INET, SOCK_RAW, icmp)
    print("Socket created!\n")

    # Put a TTL field into the send socket, incremented in the for loop
    print(ttl)
    sendSocket.setsockopt(SOL_IP, IP_TTL, ttl) 

    # Set the receiver socket to listen for data from any host at the traceroute port
    recvSocket.bind(('', destPort))
    print("Receive socket bound")

    # Set the sender socket to send an empty string to the destination address at traceroute port
    sendSocket.sendto(b"", (destAddr, destPort))
    print("Sent empty data...")

    # Receive the address of the socket sending the data

    try:
        print("Trying...")
        recvData, recvAddr = recvSocket.recvfrom(512)
        recvHost = gethostbyaddr(recvAddr)[0]

    except socket.error:
        print("Socket Error")
        pass
    finally:
        sendSocket.close()
        recvSocket.close()