from scapy.all import  *
import  sys
import time
TIME_OUT = 3
ping_address = sys.argv[1]

i = 1
while True:
    p = IP(dst=ping_address, ttl=i) / ICMP()
    try:
        start_time = time.time()
        rp =sr1(p,timeout=TIME_OUT,verbose = 0)/ICMP()
        end_time = time.time() - start_time
    except TypeError:
        print("REQUST TIME OUT")
    finally:
        if rp is not None:
            print("{} ".format(rp[IP].src))
            if rp[ICMP].type == 0:
                break
        i += 1
