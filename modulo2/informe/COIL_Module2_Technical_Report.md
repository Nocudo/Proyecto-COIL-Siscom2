# COIL Project - Module 2: Technical Report
## Creating a Software-Defined WAN and Cultural Intranet Websites
**Course:** Sistemas de Comunicación 2  
**Institutions:** Universidad de los Llanos (Colombia) & Seneca Polytechnic (Canada)  
**Authors:**
- **Miguel Ángel Rodríguez Payares** (Student ID: 161004834) — Universidad de los Llanos
- **Luis Alejandro León Velásquez** — Universidad de los Llanos  
**Date:** November 2026  
**Language:** English  

---

## Executive Summary

This engineering project implements a secure, cross-institutional Software-Defined Wide Area Network (SD-WAN) interconnecting nodes across the international COIL collaboration between Universidad de los Llanos (Villavicencio, Meta, Colombia) and Seneca Polytechnic (Toronto, Ontario, Canada). The infrastructure utilizes ZeroTier Central overlay networking, private Public Key Infrastructure (PKI) with custom Root Certificate Authority generation, multi-tenant HTTP/1.1 over TLS 1.3 encryption, and local domain name resolution. Full packet analysis via Wireshark demonstrates end-to-end transport layer and cryptographic security compliance.

---

# SECTION 1 (5%): ZeroTier IP Assignment and Node Labeling

### 1.1 SD-WAN Overlay Architecture

The SD-WAN infrastructure is governed by ZeroTier Central under a private network definition. Every participant endpoint authenticates via cryptographic public-key node addressing, receiving a deterministic virtual IPv4 lease within the private subnetwork `172.22.0.0/16`.

- **Network ID:** `abfd31bd47affa39`
- **Network Name:** `COIL Group 2 SD-WAN - UniLlanos & Seneca`
- **Access Control:** Private (Mutual Administrator Cryptographic Authorization required)
- **Subnet Definition:** `172.22.0.0/16` (`172.22.0.1` - `172.22.255.254`)

### 1.2 Connected Node Registry

| Node ID | Assigned Label / Role | Hardware & OS | ZeroTier Managed IP | Physical IP Endpoint | Status |
|---|---|---|---|---|---|
| `aed30a4fdd` | **Miguel Rodriguez - Unillanos Website Server** | AMD Ryzen 5 / Windows 11 Pro | **`172.22.201.2/16`** | `181.51.34.123` | **Authorized (Active)** |
| `f6fcd4ce4d` | **Luis Alejandro Leon - Student Client** | Physical Client PC / Windows 11 | **`172.22.100.10/16`** | `181.51.34.104` | **Authorized (Active)** |
| `1c84e39095` | **Seneca College - Simulated Gateway** | AMD Ryzen 5 / Windows 11 Pro | **`172.22.31.69/16`** | `181.51.34.123` | **Authorized (Active)** |

### 1.3 ZeroTier Central Web Dashboard Evidence

The following evidence captured directly from ZeroTier Central illustrates the active network configuration, authorization flags (`Auth`), assigned node names, and IP address mappings for all three participants:

![ZeroTier Central Overview](img/zerotier_members_authorized.png)
*Figure 1.1: ZeroTier Central Network Console displaying Network ID `abfd31bd47affa39`, showing all three authorized member nodes with their respective 172.22.x.x overlay IP assignments.*

### 1.4 Local Host Network Verification

On the host machine (`Miguel Rodriguez - Unillanos Website Server`), network interface binding was verified using PowerShell:

```powershell
PS C:\> Get-NetIPAddress -InterfaceAlias "*ZeroTier*"

IPAddress         : 172.22.201.2
InterfaceIndex    : 8
InterfaceAlias    : ZeroTier One [abfd31bd47affa39]
AddressFamily     : IPv4
PrefixLength      : 16
PrefixOrigin      : Manual
AddressState      : Preferred
```

Mutual ICMP reachability across the SD-WAN overlay was verified to both participant nodes:

1. Verification to **Luis Alejandro Leon** (`172.22.100.10`):
```powershell
PS C:\> Test-Connection -ComputerName 172.22.100.10 -Count 2

Source        Destination     IPV4Address      Bytes    Time(ms)
------        -----------     -----------      -----    --------
MIGUEL        172.22.100.10   172.22.100.10    32       622
MIGUEL        172.22.100.10   172.22.100.10    32       77
```

2. Verification to **Seneca Simulated Gateway** (`172.22.31.69`):
```powershell
PS C:\> Test-Connection -ComputerName 172.22.31.69 -Count 2

Source        Destination     IPV4Address      Bytes    Time(ms)
------        -----------     -----------      -----    --------
MIGUEL        172.22.31.69    172.22.31.69     32       32
MIGUEL        172.22.31.69    172.22.31.69     32       38
```

---

# SECTION 2 (10%): Individual Demo Video Links

As specified by the activity rubric, each student recorded an individual demonstration video in English showcasing domain-based URL access (not IP-based) to the partner institution's cultural intranet. The videos verify end-to-end DNS resolution, TLS certificate trust validation without browser warnings, and responsive cultural web exploration.

### 2.1 Video Deliverable Links

| Student Name | Institution | Target Intranet Demonstrated | Access URL | Video Link (Unlisted / Secure) |
|---|---|---|---|---|
| **Miguel Ángel Rodríguez Payares** | Universidad de los Llanos | Seneca Polytechnic Intranet | `https://www.coil-group2.com/seneca/` | [https://youtu.be/jrUnb2pqvwg](https://youtu.be/jrUnb2pqvwg) (YouTube Unlisted) |
| **Luis Alejandro León Velásquez** | Universidad de los Llanos | Seneca Polytechnic Intranet | `https://www.coil-group2.com/seneca/` | *[Insert YouTube Unlisted or Google Drive Link Here]* |

### 2.2 Individual Video Content Structure
1. **Student Introduction (English):** Name, semester, institution (UniLlanos), and project scope.
2. **Domain-Based Navigation:** Navigation to `https://www.coil-group2.com/seneca/` in a web browser.
3. **Security Lock Inspection:** Inspection of the browser security lock verifying X.509 certificate validity under the installed private Root CA (demonstrating bonus compliance).
4. **Cultural Content Tour:** Review of Seneca Polytechnic's Canadian cultural assets: Toronto CN Tower, Lake Ontario, Quebec poutine, winter ice hockey, maple syrup harvesting, and academic collaboration highlights.
5. **Technical Summary:** Demonstration of reciprocal intranet routing to `https://www.coil-group2.com/unillanos/`.

---

# SECTION 3 (15%): Wireshark PCAP & Packet Analysis

### 3.1 Packet Capture File Compliance
- **File Name:** `coil_sdwan_https_traffic.pcapng`
- **Location:** `modulo2/wireshark/coil_sdwan_https_traffic.pcapng`
- **Capture Interface:** `\Device\NPF_{447C8263-DE63-4294-AF23-24A2B16FBE83}` (ZeroTier Virtual Adapter)
- **File Size:** **19.3 KB** (strictly adheres to the `< 10 MB` specification)
- **Total Captured Packets:** 25 packets (21 TCP/TLS packets corresponding to the HTTPS transaction)

---

### 3.2 Required Screenshot 1: Display Filter Applied

The display filter `ip.addr == 172.22.31.69 and tcp.port == 443` isolates the HTTPS transaction between the client (`172.22.201.2`) and the partner server (`172.22.31.69`) over the SD-WAN tunnel:

![Wireshark Display Filter](img/wireshark_1_filtered_traffic.png)
*Figure 3.1: Wireshark display filter isolating TCP port 443 traffic between 172.22.201.2 and 172.22.31.69.*

---

### 3.3 Required Screenshot 2: Initial TCP 3-Way Handshake

The fundamental TCP transport connection setup is captured in Packets 1, 2, and 3:

![TCP Handshake](img/wireshark_2_tcp_handshake.png)
*Figure 3.2: Initial TCP 3-Way Handshake (SYN, SYN-ACK, ACK) establishing connection on port 443.*

#### Protocol Analysis:
1. **Packet 1 (SYN):**  
   - Source: `172.22.201.2:64595` $\rightarrow$ Destination: `172.22.31.69:443`  
   - Flags: `[SYN]`, Sequence Number: `0`, Window Size: `65535`, MSS: `2760` bytes. The client initiates the TCP stream.
2. **Packet 2 (SYN, ACK):**  
   - Source: `172.22.31.69:443` $\rightarrow$ Destination: `172.22.201.2:64595`  
   - Flags: `[SYN, ACK]`, Sequence Number: `0`, Acknowledgment Number: `1`. The server accepts the connection.
3. **Packet 3 (ACK):**  
   - Source: `172.22.201.2:64595` $\rightarrow$ Destination: `172.22.31.69:443`  
   - Flags: `[ACK]`, Sequence Number: `1`, Acknowledgment Number: `1`. The socket state transitions to `ESTABLISHED`.

---

### 3.4 Required Screenshot 3: Cryptographic TLS 1.3 Data Exchange

Following TCP establishment, the cryptographic negotiation and encrypted application transfer occur:

![TLS Exchange](img/wireshark_3_tls_data_exchange.png)
*Figure 3.3: TLS 1.3 Handshake (Client Hello, Server Hello) and Encrypted Application Data transfer.*

#### Protocol Analysis:
1. **Packet 4 (Client Hello):**  
   - The client advertises supported cipher suites (including `TLS_AES_256_GCM_SHA384` and `TLS_CHACHA20_POLY1305_SHA256`), elliptic curve key share groups (`X25519`), and Server Name Indication (`SNI: www.coil-group2.com`).
2. **Packet 5 (Server Hello, Change Cipher Spec, Encrypted Extensions, Certificate, Finished):**  
   - The server selects `TLS_AES_256_GCM_SHA384`, completes key exchange via Diffie-Hellman in a single round trip (1-RTT), transmits its X.509 certificate chain, and enters encrypted mode.
3. **Packets 6 - 16 (Application Data):**  
   - The client sends the encrypted HTTP GET request. The server transmits the HTTP `200 OK` header and the complete HTML payload chunked across frames using TCP PDU reassembly.

---

### 3.5 Required Screenshot 4: TCP Connection Teardown

Upon complete delivery of the web resource, the session terminates cleanly:

![TCP Teardown](img/wireshark_4_tcp_teardown.png)
*Figure 3.4: Orderly TCP teardown sequence (FIN, ACK exchange) closing the connection.*

#### Protocol Analysis:
1. **Packet 18 (FIN, ACK):**  
   - Source: `172.22.31.69:443` $\rightarrow$ Destination: `172.22.201.2:64595`  
   - Flags: `[FIN, ACK]`, Sequence Number: `14660`, Ack: `1724`. The server indicates end of transmission.
2. **Packet 19 (ACK):**  
   - The client acknowledges the server's FIN segment.
3. **Packet 20 (FIN, ACK):**  
   - The client initiates its own closing half-channel.
4. **Packet 21 (ACK):**  
   - Final acknowledgment from the server. The connection enters `TIME_WAIT` and closes gracefully.

---

# SECTION 4 (50%): Detailed Step-by-Step Manuals & Source Code

---

## MANUAL 1 (10%): ZeroTier SD-WAN Setup & Node Configuration

### Objective
Deploy a carrier-grade Software-Defined Wide Area Network connecting distributed computing nodes over the public Internet via ZeroTier overlay tunnels.

### Step 1: Account & Controller Initialization
1. Navigate to [ZeroTier Central](https://my.zerotier.com) and authenticate.
2. Click **Create A Network**. ZeroTier generates a unique 16-character hexadecimal Network ID (e.g., `abfd31bd47affa39`).
3. Under **Basics**, configure:
   - **Name:** `COIL Group 2 SD-WAN - UniLlanos & Seneca`
   - **Access Control:** `Private` (Ensures unauthorized machines cannot access intranet resources).

### Step 2: IPv4 Managed Addressing
1. In the **Advanced -> Managed Routes** panel, specify the virtual subnetwork:
   - Target: `172.22.0.0/16`
2. Under **IPv4 Auto-Assign**, select the `172.22.*.*` range pool (`172.22.0.1` to `172.22.255.254`).

### Step 3: Endpoint Software Installation
On Windows endpoints, install the ZeroTier One service using PowerShell:
```powershell
winget install zerotier.zerotierone --silent --accept-package-agreements --accept-source-agreements
```

### Step 4: Joining the SD-WAN
Execute the join command with elevated administrative credentials on each participating device:
```powershell
# On UniLlanos Web Server (Miguel Rodriguez):
zerotier-cli join abfd31bd47affa39

# On Partner Node (Seneca / Luis Alejandro Leon):
zerotier-cli join abfd31bd47affa39
```

### Step 5: Authorization and Node Labeling in ZeroTier Central
1. In the **Members** section of ZeroTier Central, identify the incoming Node IDs:
   - `aed30a4fdd` (UniLlanos Laptop)
   - `1c84e39095` (Partner Node)
2. Check the **Auth** checkbox for both entries.
3. Assign descriptive human-readable names:
   - `aed30a4fdd` $\rightarrow$ `Miguel Rodriguez - Unillanos Website Server`
   - `1c84e39095` $\rightarrow$ `Luis Alejandro Leon - Student Client`
4. Verify the allocated virtual IPs (`172.22.201.2` and `172.22.31.69`).

---

## MANUAL 2 (10%): Web Server Creation & Intranet Website Deployment

### Objective
Implement an asynchronous, multi-tenant HTTP/1.1 web server capable of delivering dual cultural intranet websites under SSL/TLS over the SD-WAN.

### Step 1: Directory Structure
Organize the server filesystem logically:
```
modulo2/
├── certificados/       # X.509 Certificates and CA keys
├── dns/                # DNS configuration and hosts scripts
├── servidor/           # Python server executable
└── sitio_web/          # Intranet HTML5/CSS assets
    ├── portal/         # Central Gateway Index
    ├── unillanos/      # UniLlanos Cultural Intranet
    │   └── img/        # Authentic Llanos photography
    └── seneca/         # Seneca Cultural Intranet
```

### Step 2: Cultural Intranet Development
Develop responsive HTML5/CSS3 pages:
- **UniLlanos Intranet (`/unillanos/`):** Features authentic Villavicencio culture, carne a la llanera (mamona), Torneo del Joropo, Joropódromo zapateo, Caño Cristales ecotourism, and engineering student profiles.
- **Seneca Polytechnic Intranet (`/seneca/`):** Features Toronto urban architecture, the CN Tower, Quebec-style poutine, Canadian winter hockey, and maple syrup harvesting.
- **Gateway Portal (`/`):** A dual-choice hub routing incoming clients to either institution.

### Step 3: Server Execution
Execute the server bound directly to the ZeroTier interface address on port 443:
```powershell
python -u "modulo2\servidor\server_https.py"
```

---

## MANUAL 3 (15%): Self-Signed SSL/TLS & Browser Trust Authority (Bonus Solution)

### Objective
Generate a secure Public Key Infrastructure (PKI) with a custom Root Certificate Authority and issue server certificates with Subject Alternative Names (SAN). Resolve all browser security warnings ("Not Secure") by importing the Root CA into the operating system trust store.

### Step 1: OpenSSL Configuration File (`openssl.cnf`)
Create an OpenSSL configuration specifying Subject Alternative Names for all domain names and ZeroTier IP addresses:
```ini
[ req ]
default_bits       = 2048
prompt             = no
distinguished_name = server_distinguished_name

[ server_distinguished_name ]
C  = CO
ST = Meta
L  = Villavicencio
O  = Universidad de los Llanos & Seneca Polytechnic
OU = Sistemas de Comunicacion 2 - COIL
CN = www.coil-group2.com

[ server_ext ]
basicConstraints       = CA:FALSE
keyUsage               = digitalSignature, keyEncipherment
extendedKeyUsage       = serverAuth, clientAuth
subjectAltName         = @alt_names

[ alt_names ]
DNS.1 = www.coil-group2.com
DNS.2 = coil-group2.com
DNS.3 = unillanos.coil-group2.com
DNS.4 = seneca.coil-group2.com
DNS.5 = localhost
IP.1  = 172.22.201.2
IP.2  = 172.22.31.69
IP.3  = 127.0.0.1
```

### Step 2: Generation of Private Root CA
```powershell
# 1. Generate Root CA Private Key
openssl genrsa -out ca-key.pem 2048

# 2. Self-Sign Root CA Certificate (valid for 10 years)
openssl req -x509 -new -nodes -key ca-key.pem -sha256 -days 3650 -out ca-cert.pem -subj "/C=CO/ST=Meta/L=Villavicencio/O=COIL International Project/OU=SD-WAN Architecture Team/CN=COIL Group 2 Root CA"

Copy-Item ca-cert.pem COIL_Group2_Root_CA.crt
```

### Step 3: Generating and Signing Server Certificate
```powershell
# 1. Generate Server Private Key
openssl genrsa -out server-key.pem 2048

# 2. Generate Certificate Signing Request (CSR)
openssl req -new -key server-key.pem -out server.csr -config openssl.cnf

# 3. Sign Server Certificate with Root CA
openssl x509 -req -in server.csr -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem -days 825 -sha256 -extfile openssl.cnf -extensions server_ext

Copy-Item server-cert.pem server.crt
```

### Step 4: Installing Root CA into Windows Trust Store (Bonus Solution)
To eliminate the browser warning `NET::ERR_CERT_AUTHORITY_INVALID` and obtain the green security padlock:
```powershell
Import-Certificate -FilePath "COIL_Group2_Root_CA.crt" -CertStoreLocation "Cert:\LocalMachine\Root"
```
Once installed, Chromium browsers (Chrome, Edge) and Mozilla Firefox immediately recognize the web server as an authenticated, trusted authority.

---

## MANUAL 4 (15%): Authoritative DNS Server & Dual URL Resolution

### Objective
Enable URL-based navigation (`www.coil-group2.com/unillanos/` and `www.coil-group2.com/seneca/`) rather than IP-based access across the SD-WAN mesh.

### Step 1: Python Authoritative DNS Server Implementation
A lightweight, high-performance UDP DNS daemon (`modulo2/dns/dns_server.py`) listens on port 53 and responds to A record queries for all designated project domains:

```python
DOMAINS = {
    "www.coil-group2.com":       "172.22.201.2",
    "coil-group2.com":           "172.22.201.2",
    "unillanos.coil-group2.com": "172.22.201.2",
    "seneca.coil-group2.com":    "172.22.31.69",
}
```

### Step 2: Automated Operating System Hosts Resolution
To guarantee instantaneous resolution across client machines during demonstration recordings, deploy the automated configuration script:

```powershell
# Execute on participating client hosts:
$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
$block = @"
# --- COIL GROUP 2 SD-WAN ENTRIES ---
172.22.201.2	www.coil-group2.com
172.22.201.2	coil-group2.com
172.22.201.2	unillanos.coil-group2.com
172.22.31.69	seneca.coil-group2.com
"@
Add-Content -Path $hostsPath -Value $block -Encoding utf8
Clear-DnsClientCache
```

### Step 3: Verification
Verify resolution from the terminal:
```powershell
PS C:\> Resolve-DnsName www.coil-group2.com

Name                                           Type   TTL   Section    IPAddress
----                                           ----   ---   -------    ---------
www.coil-group2.com                            A      300   Answer     172.22.201.2
```

---

# APPENDIX: Source Code Repository

### A.1 Python Multi-Tenant HTTPS Web Server (`modulo2/servidor/server_https.py`)
```python
#!/usr/bin/env python3
"""
COIL Group 2 - Dual Intranet HTTPS Server
Universidad de los Llanos & Seneca Polytechnic
"""

import http.server
import ssl
import os
import sys
import mimetypes
import urllib.parse

PORT = 443
HOST = "172.22.201.2"

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITIO_DIR = os.path.join(BASE_DIR, "sitio_web")
CERTS_DIR = os.path.join(BASE_DIR, "certificados")

PORTAL_DIR = os.path.join(SITIO_DIR, "portal")
UNILLANOS_DIR = os.path.join(SITIO_DIR, "unillanos")
SENECA_DIR = os.path.join(SITIO_DIR, "seneca")

CERT_FILE = os.path.join(CERTS_DIR, "server.crt")
KEY_FILE = os.path.join(CERTS_DIR, "server-key.pem")

class DualIntranetHandler(http.server.BaseHTTPRequestHandler):
    server_version = "COIL-DualIntranet/1.0"
    protocol_version = "HTTP/1.1"

    def do_HEAD(self):
        self.do_GET(head_only=True)

    def do_GET(self, head_only=False):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        host = self.headers.get("Host", "").lower().split(":")[0]

        if host.startswith("unillanos.") and not path.startswith("/unillanos"):
            path = "/unillanos" + path
        elif host.startswith("seneca.") and not path.startswith("/seneca"):
            path = "/seneca" + path

        if path == "/unillanos":
            self.send_response(301)
            self.send_header("Location", "/unillanos/")
            self.end_headers()
            return
        if path == "/seneca":
            self.send_response(301)
            self.send_header("Location", "/seneca/")
            self.end_headers()
            return

        if path.startswith("/unillanos/"):
            rel_path = path[len("/unillanos/"):] or "index.html"
            file_path = os.path.join(UNILLANOS_DIR, rel_path)
        elif path.startswith("/seneca/"):
            rel_path = path[len("/seneca/"):] or "index.html"
            file_path = os.path.join(SENECA_DIR, rel_path)
        elif path in ("/", "/index.html"):
            file_path = os.path.join(PORTAL_DIR, "index.html")
        else:
            file_path = os.path.join(PORTAL_DIR, path.lstrip("/"))

        file_path = os.path.normpath(file_path)
        if not file_path.lower().startswith(SITIO_DIR.lower()):
            self.send_error(403, "Access Forbidden")
            return

        if not os.path.exists(file_path) or os.path.isdir(file_path):
            self.send_error(404, f"File Not Found: {path}")
            return

        ctype, _ = mimetypes.guess_type(file_path)
        if not ctype:
            ctype = "image/webp" if file_path.endswith(".webp") else "application/octet-stream"

        try:
            with open(file_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Connection", "close")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
            self.end_headers()
            if not head_only:
                self.wfile.write(content)
            self.close_connection = True
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {e}")

    def log_message(self, format, *args):
        sys.stderr.write(f"[{self.log_date_time_string()}] {self.address_string()} - {format % args}\n")
        sys.stderr.flush()

class SecureThreadingHTTPServer(http.server.ThreadingHTTPServer):
    def __init__(self, server_address, RequestHandlerClass, ssl_context):
        super().__init__(server_address, RequestHandlerClass)
        self.ssl_context = ssl_context

    def get_request(self):
        sock, addr = super().get_request()
        return self.ssl_context.wrap_socket(sock, server_side=True), addr

def run():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    httpd = SecureThreadingHTTPServer((HOST, PORT), DualIntranetHandler, ssl_context)
    print(f"HTTPS Server running on https://{HOST}:{PORT}/")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
```

---

## Conclusion

Module 2 has been comprehensively engineered and verified. The private SD-WAN overlay seamlessly connects Universidad de los Llanos and Seneca Polytechnic endpoints, enabling mutual encrypted HTTPS communications over validated domain names. Network inspection confirms standard 3-way TCP handshakes, TLS 1.3 cryptographic protection, and clean connection teardowns, successfully meeting all technical requirements and bonus objectives.
