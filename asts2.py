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
#    https://adayinthelifeof.nl/2010/07/30/creating-a-traceroute-program-in-php/
# Algorithm: 
# What traceroute does, it take advantage of this TTL field. 
# It sends a packet to a certain destination (the site you want to traceroute to), with a TTL of 1. 
# This means, the packet gets dropped by the first station it passes and returns a ICMP message. 
# We fetch this message, find out who send it (namely, the first station), we figure out how long the roundtrip took (time from send until receiving the ICMP message) 
# and print this on the screen. After this we increase the TTL to 2, and send out the packet again. 
# Now it will pass the first station, and gets dropped by the second station. That station returns a ICMP message and we print the info.. 
# This continues until we have reached a certain TTL (normally, 30) or until we have reached our final destination.

a = 0

for a in range(0, 10):
    print(a)