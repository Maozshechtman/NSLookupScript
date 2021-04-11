import sys
from time import time

from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, ICMP, UDP
from scapy.sendrecv import sr1

ADDRESS_FOR_TRACE = sys.argv[1]
TTL_START = 1
response = ""


def function(TTL_START):
    try:
        my_packet = IP(dst='8.8.8.8') / UDP(sport=24601, dport=53) / DNS(qdcount=1, rd=1) / DNSQR(qname=ADDRESS_FOR_TRACE)
        packet_response = sr1(my_packet, verbose=0)
        temp = packet_response[DNSRR].rdata
        print("but : ",temp)
        temp2 = ""
        while temp2 != temp:
            debut = time()
            my_packet = IP(dst=temp, ttl=TTL_START) / ICMP()
            response = sr1(my_packet,verbose=0,timeout=3) / ICMP()
            temp2 = response[IP].src
            fin = time()- debut
            print(fin)
            print("the address of the router numero :", TTL_START, " is : ", temp2)
            TTL_START += 1
    except Exception:
        print("ERROR ")


function(TTL_START)