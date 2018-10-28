# myTraceRoute.py
# Author: Jan Louis Evangelista, 28912146
# Description: 
# The program implements basic Traceroute functionality
# 1) It displays the router's info as it passes it
# 2) It calculates and displays 3 RTT values (in ms) for 
#    each router, on the same line as the router info
#    If the RTT cannot be calculated within 4 s, display an *
# 3) It displays a terminating message when max number of 30 hops is reached

a = 0

for a in range(0, 10):
    print(a)