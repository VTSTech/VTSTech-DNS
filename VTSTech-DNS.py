# Program: VTSTech-DNS.py
# Description: Python script that checks a list of FQDN for DNS and writes the results to a text file.
# Author: Written by VTSTech (veritas@vts-tech.org)
# GitHub: https://github.com/VTSTech
# Homepage: www.VTS-Tech.org
# Dependencies: dnspython
# pip install dnspython
import argparse
import time
import random
import dns.resolver

def resolve_fqdns(fqdns, delay):
    resolved_fqdns = []
    resolver = dns.resolver.Resolver()
    # You can add more DNS servers here if needed
    dns_servers = [
        '1.1.1.1',
        '4.4.4.4',
        '8.8.8.8',
        '9.9.9.9',
        '94.140.14.14',
        '208.67.222.222'
    ]
                
    for fqdn in fqdns:
        resolver.nameservers = [random.choice(dns_servers)]
        
        while True:
            try:
                answer = resolver.query(fqdn)
                for rdata in answer:
                    time.sleep(delay) 
                    resolved_fqdns.append((fqdn, str(rdata)))
                    print(f"Attempting {fqdn} ... SUCCESS")
                    with open(output_file, "w") as f:
                        for fqdn, result in resolved_fqdns:
                            if ((result != "NXDOMAIN") and (result != "No DNS record found")):
                                f.write(f"{fqdn} {result}\n")
                break  # Break the loop if resolved successfully
            except dns.resolver.NXDOMAIN:
                # Unable to resolve the FQDN
                resolved_fqdns.append((fqdn, "NXDOMAIN"))
                print(f"Attempting {fqdn} ... FAIL")
                break  # Break the loop if NXDOMAIN
            except dns.resolver.NoAnswer:
                # No DNS record found
                resolved_fqdns.append((fqdn, "No DNS record found"))
                print(f"Attempting {fqdn} ... NO RECORD")
                break  # Break the loop if NoAnswer
            except dns.resolver.Timeout:
                # Timeout occurred, retry with a different DNS server
                print(f"Attempting {fqdn} ... TIMEOUT")
                break # Break the loop on Timeout
            except dns.exception.DNSException as e:
                # Other DNS exceptions
                print(f"Attempting {fqdn} ... {type(e).__name__}: {e}")
                break  # Break the loop on other DNS exceptions  
            time.sleep(delay)  # Delay between queries
    return resolved_fqdns

def main():
    parser = argparse.ArgumentParser(description="Resolve FQDNs from a file")
    parser.add_argument("-f", "--file", help="Input file containing FQDNs", required=True)
    parser.add_argument("-d", "--delay", help="Delay time between queries (in seconds)", type=float, default=4.0)
    args = parser.parse_args()

    input_file = args.file
    delay = args.delay
    global output_file
    output_file ="resolved_domains.txt"

    with open(input_file, "r") as f:
        fqdns = [line.strip() for line in f.readlines()]

    resolved_fqdns = resolve_fqdns(fqdns, delay)

if __name__ == "__main__":
    main()
