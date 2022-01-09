#   creating NSlookup exercise
#   Author: Chani Viner 2021
import sys
i, o, e = sys.stdin, sys.stdout, sys.stderr
from scapy.all import *
sys.stdin, sys.stdout, sys.stderr = i, o, e


def dns_nslookup(domain_address):
    """
    find the ip address/es 0f a domain name. also print CNAME if exixt
    :param domain_address: the domain to find the ip of
    :return: none
    """
    dns_packet = IP(dst='8.8.8.8') / UDP(sport=24601) / DNS(qdcount=1) / DNSQR(
        qname=domain_address)  # creating a dns packet
    response_packet = sr1(dns_packet)  # send the packet and get a response packet
    if response_packet[DNS].rcode == 3:  # checking if the domain not exist
        print("Non-existent domain")
    else:
        # printing all the ip addresses that gotten
        for i in range(response_packet[DNS].ancount):
            if response_packet[DNSRR][i].type == 1:
                print(response_packet[DNSRR][i].rdata)
    # looking for a CNAME
    for i in range(response_packet[DNS].ancount):
        if response_packet[DNSRR][i].type == 5:
            print("CNAME: " + response_packet[DNSRR][0].rdata.decode())
            break


def reverse_dns_nslookup(ip_address):
    """
    find the domain name of a given ip address
    :param ip_address: the ip address to find the domain name of
    :return: none
    """
    list_of_ip = ip_address.split('.')
    if len(list_of_ip) == 4:
        reverse_ip = list_of_ip[3] + '.' + list_of_ip[2] + '.' + list_of_ip[1] + '.' + list_of_ip[
            0]  # reversing the ip address that gotten
        rv_packet = IP(dst='8.8.8.8') / UDP(sport=24601) / DNS(qdcount=1) / DNSQR(qname=reverse_ip + '.in-addr.arpa',
                                                                        qtype=12)  # creating the reverse dns packet
        response_packet = sr1(rv_packet)
        if response_packet[DNS].rcode == 3:
            print("Non-existent ip address")
        else:
            print(response_packet[DNSRR].rdata.decode())  # printing the name of the domain
    else:
        print("Non-existent ip address")

def main():
    if len(sys.argv) == 2:
        dns_nslookup(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[1] == "-type=PTR" and valid_ip(sys.argv[2]):
        reverse_dns_nslookup(sys.argv[2])
    else:
        print("error")


if __name__ == '__main__':
    main()
