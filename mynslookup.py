__author__ = "Maoz Shechtman"

from scapy.all import *
import sys
import socket

# region Constants
TYPE = 1
DOMAIN_ADDRESS = 2
DNS_SERVER_ADDRESS = '8.8.8.8'
SRC_PORT_NUMBER = 24601
DST_PORT_NUMBER = 53
QD_COUNT = 1


# endregion

def main():
    # cut the type from the user(Bark told us that this is the shape of the script)
    query_type = sys.argv[TYPE][5::]
    domain_address = sys.argv[DOMAIN_ADDRESS]

    if query_type == 'PTR':
        domain_address = domain_address.split('.')
        domain_address.reverse()
        domain_address = ('.'.join(domain_address)) + ".in-addr.arpa"
    # Barak told us to assume that the input is valid
    my_dns_packet = IP(dst=DNS_SERVER_ADDRESS) / UDP(sport=SRC_PORT_NUMBER, dport=DST_PORT_NUMBER) / DNS(
        qdcount=QD_COUNT) / DNSQR(qname=domain_address, qtype=query_type)
    response_packet = sr1(my_dns_packet,verbose=0)
    answers_number = response_packet[DNS].ancount
    print("Non-authoritative answer:")
    for i in range(0, answers_number):
        # handling the rdata
        my_answer = response_packet[DNSRR][i].rdata
        if not isinstance(my_answer, str):
            my_answer = my_answer.decode("utf-8")[0:len(my_answer) - 1]
            if query_type =="PTR":
                print("{}    name = {}".format( domain_address,my_answer))
            else:
                print("Name:     {}".format(my_answer))
        else:
            print("Address:   {} ".format(my_answer))


if __name__ == '__main__':
    main()
