#!/usr/bin/env python3
"""
COIL Group 2 - Authoritative & Forwarding DNS Server (dnslib RFC Compliant)
Serves DNS resolution for COIL SD-WAN domain names:
  - www.coil-group2.com        -> 172.22.201.2
  - coil-group2.com            -> 172.22.201.2
  - unillanos.coil-group2.com  -> 172.22.201.2
  - seneca.coil-group2.com     -> 172.22.201.2

Full RFC 1035 / RFC 2308 compliance via dnslib:
- Handles Type A, AAAA, HTTPS (Type 65), ANY
- Returns valid authoritative SOA for negative caching (NODATA)
- Forwards non-COIL queries to upstream DNS (8.8.8.8)
"""

import os
import socket
import sys
from dnslib import DNSRecord, QTYPE, RCODE, A, SOA, RR

DNS_IP = "172.22.201.2"
PORT = 53
LISTEN_ADDR = "0.0.0.0"
UPSTREAM_DNS = "8.8.8.8"
UPSTREAM_PORT = 53

DOMAINS = {
    "www.coil-group2.com": DNS_IP,
    "coil-group2.com": DNS_IP,
    "unillanos.coil-group2.com": DNS_IP,
    "seneca.coil-group2.com": DNS_IP,
}

SOA_RECORD = SOA("ns.coil-group2.com", "admin.coil-group2.com", (2026112101, 3600, 600, 86400, 300))

def forward_query(data, timeout=2.0):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as upstream_sock:
            upstream_sock.settimeout(timeout)
            upstream_sock.sendto(data, (UPSTREAM_DNS, UPSTREAM_PORT))
            resp, _ = upstream_sock.recvfrom(4096)
            return resp
    except Exception:
        return None

def is_coil_domain(qname):
    return qname in DOMAINS

def is_subdomain_of_coil(qname):
    return qname.endswith(".coil-group2.com") and qname not in DOMAINS

def safe_print(msg):
    try:
        if sys.stdout:
            print(msg, flush=True)
    except Exception:
        pass

def run_dns():
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        try:
            if stream is None:
                setattr(sys, stream_name, open(os.devnull, "w"))
            else:
                stream.flush()
        except Exception:
            setattr(sys, stream_name, open(os.devnull, "w"))

    safe_print("=" * 60)
    safe_print("COIL Group 2 - Authoritative DNS Server (dnslib Engine)")
    safe_print(f"Listening on UDP {LISTEN_ADDR}:{PORT}")
    safe_print(f"Upstream DNS Forwarder: {UPSTREAM_DNS}:{UPSTREAM_PORT}")
    safe_print("Configured COIL Records:")
    for d, ip in DOMAINS.items():
        safe_print(f"  {d:30} -> {ip}")
    safe_print("=" * 60)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if hasattr(socket, "SIO_UDP_CONNRESET"):
        try:
            sock.ioctl(socket.SIO_UDP_CONNRESET, False)
        except Exception:
            pass

    try:
        sock.bind((LISTEN_ADDR, PORT))
    except Exception as e:
        print(f"ERROR: Could not bind UDP port {PORT}: {e}")
        sys.exit(1)

    while True:
        try:
            data, addr = sock.recvfrom(4096)
            try:
                request = DNSRecord.parse(data)
                qname = str(request.q.qname).rstrip('.').lower()
                qtype = request.q.qtype
            except Exception:
                continue

            if is_coil_domain(qname):
                reply = request.reply()
                if qtype in (QTYPE.A, QTYPE.ANY):
                    target = DOMAINS.get(qname, DNS_IP)
                    reply.add_answer(RR(request.q.qname, QTYPE.A, rdata=A(target), ttl=300))
                    sock.sendto(reply.pack(), addr)
                    safe_print(f"[COIL DNS] {addr[0]} -> '{qname}' (Type {QTYPE.get(qtype, qtype)}) resolved to {target}")
                else:
                    reply.add_auth(RR("coil-group2.com", QTYPE.SOA, rdata=SOA_RECORD, ttl=300))
                    sock.sendto(reply.pack(), addr)
                    safe_print(f"[COIL DNS] {addr[0]} -> '{qname}' (Type {QTYPE.get(qtype, qtype)}) returned NODATA+SOA")
            elif is_subdomain_of_coil(qname):
                reply = request.reply()
                reply.header.rcode = RCODE.NXDOMAIN
                reply.add_auth(RR("coil-group2.com", QTYPE.SOA, rdata=SOA_RECORD, ttl=300))
                sock.sendto(reply.pack(), addr)
                safe_print(f"[COIL DNS] {addr[0]} -> '{qname}' returned NXDOMAIN+SOA")
            else:
                resp = forward_query(data)
                if resp:
                    try:
                        sock.sendto(resp, addr)
                    except Exception:
                        pass
        except KeyboardInterrupt:
            safe_print("\nShutting down DNS server.")
            break
        except ConnectionResetError:
            pass
        except Exception as e:
            safe_print(f"Error handling query: {e}")

if __name__ == "__main__":
    run_dns()
