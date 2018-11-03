# myTraceRoute.py
#
# Author: Jan Louis Evangelista, 28912146
#
# Description: 
# The program implements basic Traceroute functionality
# 1) It displays the router's info as it passes it
# 2) It calculates and displays 3 RTT values (in ms) for 
#    each router, on the same line as the router info
#    If the RTT cannot be calculated within 4 s, display an *
# 3) It displays a terminating message when max number of 30 hops is reached
#
# Usage:
# YOU MUST USE LINUX. SOCK_RAW requires root privileges in order to run and receive raw socket streams.
# > sudo python myTraceRoute.py hostname.com
#
# References used:
#   https://web.archive.org/web/20160625004717/https://blogs.oracle.com/ksplice/entry/learning_by_doing_writing_your
#   The above tutorial given by Oracle outlines how to create a traceroute program,
#   The tutorial above lacks RTT and triple packet sending functionality

import sys
from socket import *
import time

hostname = sys.argv[1] # Usage: sudo python myTraceRoute.py hostname.com

# Use try block to catch invalid host names
try:
    destAddr = gethostbyname(hostname) # Find the host address and turn it into IP
except error:
    print("Error getting hostname, please try a different hostname.")
    quit()

destPort = 33434

print("Traceroute for: " + hostname + " at IP: " + destAddr + ":" + str(destPort))

# Get protocol constants for socket creation
icmp = getprotobyname('icmp') # Received packets are ICMP messages
udp = getprotobyname('udp') # Sent packets are UDP packets

max_hops = 31 # Set max hops to 30 + 1
timeList = list()

for ttl in range(1, max_hops):
    for repeats in range(3):
        # Create the connection
        sendSocket = socket(AF_INET, SOCK_DGRAM, udp)
        recvSocket = socket(AF_INET, SOCK_RAW, icmp)

        # Put a TTL field into the send socket, incremented in the for loop
        sendSocket.setsockopt(SOL_IP, IP_TTL, ttl) 
        recvSocket.settimeout(4)

        # Set the receiver socket to listen for data from any host at the traceroute port
        recvSocket.bind(('', destPort))

        # Set the sender socket to send an empty string to the destination address at traceroute port
        # Start RTT timer here
        t0 = time.time()
        sendSocket.sendto(b"", (destAddr, destPort))

        recvAddr = None

        # Use try-except block to catch socket errors, close sockets after use
        try:          
            recvData, recvAddr = recvSocket.recvfrom(512)
            
            #Able to receive data, end RTT timer
            t1 = time.time()
            tf = t1 - t0
            timeList.append('{:.3}'.format(tf)) # Format to 3 significant digits
            
            # Convert the received IP addr to a host name, set to IP if none
            try:
                recvName = gethostbyaddr(recvAddr[0])[0]
            except error:
                recvName = recvAddr[0]

        except error:
            # Receiver socket timed out, set time to *
            timeList.append("*")
            pass
        finally:
            sendSocket.close()
            recvSocket.close()
    
    # Print out the router data, unless the connection timed out
    if timeList != ["*", "*", "*"]:
        print(str(ttl) + ": " + recvName + " (" + recvAddr[0] + ") - " +  timeList[0] + "s " + timeList[1] + "s " + timeList[2] + "s")
        del timeList[:]
    else:
        print(str(ttl) + ": * * *" )
        break

    # Break the for loop when the received IP addr is the same as the dest IP addr
    if recvAddr[0] == destAddr:
        break

if ttl >= max_hops:
    print("Terminating trace, max hops of 30 reached.")
        