# COIL Project - Module 2: Technical Report
## Design, Deployment, and Packet-Level Verification of a ZeroTier SD-WAN and Dual-Intranet HTTPS Infrastructure for International COIL Collaboration

**Course:** Sistemas de Comunicacion 2  
**Institutions:** Universidad de los Llanos (Villavicencio, Meta, Colombia) & Seneca Polytechnic (Toronto, Ontario, Canada)  
**Authors:**
- **Miguel Angel Rodriguez Payares** (Student ID: 161004834, `marodriguez.payares@unillanos.edu.co`) — Electronic Engineering, Universidad de los Llanos
- **Luis Alejandro Leon Velasquez** (`laleon.velasquez@unillanos.edu.co`) — Electronic Engineering, Universidad de los Llanos  
**Date:** November 2026  
**Language:** English  

---

## Executive Summary

This engineering report documents the complete design, deployment, live telemetry acquisition, and packet-level verification of a Software-Defined Wide Area Network (SD-WAN) and dual-tenant HTTPS cultural intranet infrastructure developed for Module 2 of the Collaborative Online International Learning (COIL) partnership between Universidad de los Llanos (Villavicencio, Colombia) and Seneca Polytechnic (Toronto, Canada). Five authorized endpoints (three Windows 11 `x86_64` desktop/server hosts and two Android `arm64` mobile handsets) are interconnected across a private ZeroTier overlay subnetwork (`abfd31bd47affa39`, `172.22.0.0/16`, interface MTU `1300 B`, `5/10` included devices, `5` authorized, `0` unauthorized). A custom non-blocking threaded Python web server (`COIL-DualIntranet/2.0`) delivers responsive institutional intranets secured with TLS 1.3 (`TLS_AES_256_GCM_SHA384`, `0x1302`) using a private 2048-bit RSA Root Certificate Authority (`COIL Group 2 Root CA`) with X.509v3 Subject Alternative Name (SAN) leaf certificates trusted natively by Windows and Android clients for zero-warning browser verification (rubric bonus objective). Domain-based routing (`www.coil-group2.com`, `coil-group2.com`, `unillanos.coil-group2.com`, and `seneca.coil-group2.com`) is served by a `dnslib`-based authoritative UDP/53 DNS daemon implementing RFC 1035 and RFC 2308 negative caching (`NODATA+SOA`). Live Wireshark dissection (`modulo2/wireshark/coil_sdwan_https_traffic.pcapng`, `25,408` bytes = `24.81 KB`, strictly `< 10 MB`) validates sub-millisecond (`0.5346 ms`) SD-WAN DNS resolution, `MSS=1260` B TCP three-way handshakes (`14.21 ms` RTT), 1-RTT TLS 1.3 encrypted delivery of the `15,470 B` partner intranet payload, and graceful four-way FIN teardowns (`0.4083 s` duration) with zero TCP resets.

---

# SECTION 1 (5%): ZeroTier SD-WAN IP Assignment and Node Labeling

### 1.1 SD-WAN Overlay Architecture and Addressing Plan

ZeroTier abstracts physical WAN diversity into a flat virtual Ethernet broadcast domain by decoupling the underlay transport (Virtual Layer 1, VL1) from virtualized switching and addressing (Virtual Layer 2, VL2). Each endpoint generates a cryptographic public/private key pair whose hash forms a unique 40-bit (10-hexadecimal-character) Node ID, enabling authenticated UDP/9993 encapsulation and NAT traversal across disparate residential ISPs.

- **Network ID:** `abfd31bd47affa39`
- **Network Name:** `COIL Group 2 SD-WAN - UniLlanos & Seneca`
- **Access Control:** `Private` (Mutual Administrator Cryptographic Authorization required; `5` Authorized, `0` Unauthorized, `5 / 10` Included Devices)
- **Managed IPv4 Subnet:** `172.22.0.0/16` (`172.22.0.1` to `172.22.255.254` Easy Auto-Assign pool, on-link LAN route)
- **Virtual Interface MTU:** `1300` bytes (clamped to prevent outer UDP/VL1 fragmentation across Ethernet `1500 B`, PPPoE `1492 B`, and LTE/5G bearer links, yielding a deterministic TCP `MSS = 1260` bytes)
- **Authoritative SD-WAN DNS Push:** Server `172.22.201.2` (`coil-group2.com`)

### 1.2 Authorized Member Registry and Node Labeling Compliance

All five participating endpoints are authorized in ZeroTier Central with explicit institutional and student role labels:

| Node ID | Virtual MAC | Assigned Label / Role | OS / Arch & Client Version | Managed Overlay IP(s) | Physical Underlay Endpoint | Auth | Activity Status |
|---|---|---|---|---|---|---|---|
| `aed30a4fdd` | `3a:54:7c:4d:f2:ec` | **Miguel Rodriguez - Unillanos Website Server** | Windows `x86_64` (`v1.16.2`) | **`172.22.201.2/16`** | `181.51.34.123` | **Yes** | Active (`1 min`) |
| `1c84e39095` | `3a:e6:2b:a4:2d:a4` | **Seneca College - Simulated Gateway** | Windows `x86_64` (`v1.16.2`) | **`172.22.31.69/16`** | `181.51.34.123` | **Yes** | Active (`1 min`) |
| `b63d8aeba8` | `3a:4c:92:cd:56:99` | **Luis Alejandro Leon - Student Client** | Windows `x86_64` (`v1.16.2`) | **`172.22.100.11`**, **`172.22.164.74`** | `181.51.34.104` | **Yes** | Active (`1 min`) |
| `f6fcd4ce4d` | `3a:0c:53:93:73:7c` | **Luis Alejandro Leon - Student Client** | Android `arm64` (`v1.16.0`) | **`172.22.100.10`** | `181.51.34.104` | **Yes** | Inactive (`37 min`) |
| `8eb3130d2c` | `3a:74:1c:54:b0:1d` | **Miguel Rodriguez - Student Client** | Android `arm64` (`v1.16.0`) | **`172.22.38.108`**, **`172.22.201.50`** | `181.51.34.123` | **Yes** | Inactive (`2 hr`) |

### 1.3 ZeroTier Central Web Dashboard Evidence

The following evidence captured directly from ZeroTier Central illustrates the active network configuration, authorization flags (`Authorized (5)`, `Not authorized (0)`), assigned node names, client versions, underlay endpoints (`181.51.34.123` and `181.51.34.104`), and `172.22.x.x` IP address mappings for all five authorized nodes:

![ZeroTier Central Authorized Members](figuras/zerotier_members_fresh.png)
*Figure 1.1: ZeroTier Central Member Management Console for Network ID `abfd31bd47affa39`, confirming 5/10 included devices, 5 authorized nodes (0 unauthorized), institutional node labeling, managed `172.22.x.x` IP assignments, and underlay public endpoints.*

### 1.4 Host Interface Verification and Live ICMP RTT Matrix

On the host machine (`Miguel Rodriguez - Unillanos Website Server`, node `aed30a4fdd`), the local ZeroTier virtual adapter (`ZeroTier One [abfd31bd47affa39]`) binds `172.22.201.2/16` with an enforced MTU of `1300` bytes:

![Host IP Verification](figuras/host_ip_verification_fresh.png)
*Figure 1.2: Local host network interface verification confirming active ZeroTier One virtual adapter binding within the `172.22.0.0/16` SD-WAN overlay subnet.*

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

Bidirectional Layer-3 reachability across the encrypted SD-WAN overlay was verified via live ICMP echo probes across both local peer-to-peer (`181.51.34.123`) and cross-ISP WAN peer-to-peer (`181.51.34.123 -> 181.51.34.104`) paths:

| Probe Path (Source -> Destination) | Target Node ID & Role | Link Type | Min RTT | Max RTT | Avg RTT | Packet Loss |
|---|---|---|---|---|---|---|
| `172.22.201.2 -> 172.22.31.69` | `1c84e39095` (Seneca Simulated Gateway) | LAN P2P | `9 ms` (`3 ms` peak window) | `13 ms` (`31 ms` peak window) | **`10 ms`** | **`0%`** |
| `172.22.31.69 -> 172.22.201.2` | `aed30a4fdd` (UniLlanos Website Server) | LAN P2P (reverse) | `3 ms` | `10 ms` | **`6 ms`** | **`0%`** |
| `172.22.201.2 -> 172.22.100.11` | `b63d8aeba8` (Luis Alejandro Leon - Windows Client) | Cross-ISP WAN P2P | `22 ms` (`16 ms` ext.) | `46 ms` (`70 ms` ext.) | **`31 ms`** | **`0%`** |
| `172.22.201.2 -> 172.22.164.74` | `b63d8aeba8` (Luis Alejandro Leon - Secondary IP) | Cross-ISP WAN P2P | `19 ms` | `28 ms` | **`23 ms`** | **`0%`** |
| `172.22.201.2 -> 172.22.100.10` | `f6fcd4ce4d` (Luis Alejandro Leon - Android Client) | Mobile VPN (Screen Locked)* | -- | -- | -- | `75%` (1/4 received) |

*\*Note on mobile power management: Probing the Android handset at `172.22.100.10` (`f6fcd4ce4d`) while its screen was locked yielded 1/4 echo replies due to Android Doze background VPN throttling; waking the handset restores immediate Layer-3 reachability for mobile HTTPS and Root CA verification.*

---

# SECTION 2 (10%): Individual Demonstration Video Links

As specified by the activity rubric, each student recorded an individual demonstration video in English showcasing domain-based URL access (`https://www.coil-group2.com/seneca/`, never numeric IP literals) to the partner institution's cultural intranet. The videos verify end-to-end authoritative DNS resolution over UDP port 53, TLS 1.3 certificate trust validation against `COIL Group 2 Root CA` without browser security warnings (bonus compliance), and reciprocal cultural intranet exploration.

### 2.1 Video Deliverable Links

| Student Name & Identifier | Institution | Target Intranet Demonstrated | Access URL (FQDN) | Local Repository Archive & Script | Video Link (Unlisted / Restricted) |
|---|---|---|---|---|---|
| **Miguel Angel Rodriguez Payares** (ID: `161004834`) | Universidad de los Llanos | Seneca Polytechnic Intranet | `https://www.coil-group2.com/seneca/` | `modulo2/video/grabaciones/` (`20261121_192309.mp4`--`20261121_192830.mp4`); `COIL_Module2_Miguel_Rodriguez_Demo.mp4`; `modulo2/video/video_script_english.md` | [https://youtu.be/jrUnb2pqvwg](https://youtu.be/jrUnb2pqvwg) (YouTube Unlisted) |
| **Luis Alejandro Leon Velasquez** (`laleon.velasquez@unillanos.edu.co`) | Universidad de los Llanos | Seneca Polytechnic Intranet | `https://www.coil-group2.com/seneca/` | `modulo2/video/video_script_english.md` (Part 2, Node `b63d8aeba8`, IP `172.22.100.11`) | [Google Drive Video Link](https://drive.google.com/file/d/1cM7jSHlOZLz9tFr89fhZOlAa03Ix47CH/view?usp=sharing) (Google Drive Shared) |

### 2.2 Standardized Four-Scene English Demonstration Protocol
1. **Scene 1 (0:00--0:25) — Student Introduction and ZeroTier Overlay IP Confirmation:** The student introduces themselves in English, states their affiliation at Universidad de los Llanos, and displays the active ZeroTier One interface confirming authorization in network `abfd31bd47affa39` (`172.22.201.2` on node `aed30a4fdd` for Miguel Angel Rodriguez Payares; `172.22.100.11` on node `b63d8aeba8` for Luis Alejandro Leon Velasquez).
2. **Scene 2 (0:25--0:40) — Domain-Based Navigation to Seneca Intranet:** The presenter navigates to `https://www.coil-group2.com/seneca/` by domain name in the browser address bar, exercising live UDP/53 DNS resolution and RFC 9110 `Host` header virtual-host routing.
3. **Scene 3 (0:40--0:55) — Live Browser Security Lock and X.509 Certificate Inspection:** Clicking the browser security padlock opens the connection inspector (*Connection is secure — Certificate is valid*) and X.509 certificate viewer, verifying TLS 1.3 (`TLS_AES_256_GCM_SHA384`) and tracing the certificate chain from `CN = www.coil-group2.com` to the locally trusted `COIL Group 2 Root CA`.
4. **Scene 4 (0:55--1:55) — Cultural Walkthrough and Reciprocal Intranet Routing:** The presenter tours the Seneca Polytechnic intranet sections (*Toronto Metropolis & Landmarks*, *Canadian Heritage & Winter Life*, *Canadian Culinary Classics*, and *Academic & Telecommunications Partnership*) and clicks *Switch to UniLlanos Intranet* (`href="/unillanos/"`) to verify reciprocal routing to `https://www.coil-group2.com/unillanos/`.

---

# SECTION 3 (15%): Wireshark PCAP & Deep Packet Analysis

### 3.1 Packet Capture File Compliance & Flow Metadata

Live traffic was intercepted directly on the ZeroTier virtual adapter while requesting the Seneca Polytechnic cultural intranet (`https://www.coil-group2.com/seneca/`) from the UniLlanos host (`172.22.201.2`) toward the Seneca simulated server (`172.22.31.69`) over TCP port 443.

| Parameter | Measured Value / Verification Result |
|---|---|
| **Capture Artifact** | `modulo2/wireshark/coil_sdwan_https_traffic.pcapng` |
| **Capture Interface** | `\Device\NPF_{447C8263-DE63-4294-AF23-24A2B16FBE83}` (`ZeroTier One [abfd31bd47affa39]`) |
| **File Size** | **`25,408` bytes (`24.81 KB`)** — strictly `< 10 MB` (`0.24%` of the `10,240 KB` rubric limit; `99.76%` safety margin) |
| **Total Trace Frames** | **`44` frames** (`23,451` bytes captured on wire) |
| **Protocol Hierarchy** | **UDP:** `8` frames (`7` DNS frames including Frames 1--2 at `0.5346 ms` + `1` overlay broadcast); **TCP:** `36` frames (`TLSv1.3` record dissection) |
| **Filtered HTTPS Flow** | `172.22.201.2:52382 <-> 172.22.31.69:443` (**`36` frames**, Frames 3--38, `22,785` bytes on wire, **`0.4083 s` duration** from `0.2392395 s` to `0.6475791 s`) |
| **Client Contribution** | `15` frames / `2,505` bytes on wire / `1,684` bytes TCP sequence space (`1,683 B` payload + `FIN`) |
| **Server Contribution** | `21` frames / `20,280` bytes on wire / `19,135` bytes TCP sequence space (`19,134 B` payload + `FIN`, `Ack=19136`) |
| **Transport Anomalies** | **`0` retransmissions, `0` out-of-order segments, `0` `RST` flags** (`tcp.flags.reset == 1` returns 0 packets) |

---

### 3.2 Preceding SD-WAN DNS Resolution (Frames 1--2)

Before opening the TCP socket on port 443, the trace captures the live SD-WAN DNS query and authoritative response over UDP port 53 in **Frames 1--2** (dissected in detail in Manual 4, Figure 4.6):
- **Frame 1 (`0.0000000 s`):** UDP query `172.22.31.69:51420 -> 172.22.201.2:53`, Transaction ID `0x9121`, standard query for `A www.coil-group2.com`.
- **Frame 2 (`0.0005346 s`):** Authoritative UDP response `172.22.201.2:53 -> 172.22.31.69:51420`, Transaction ID `0x9121`, Authoritative Answer flag `AA=1`, resolving `www.coil-group2.com -> 172.22.201.2` with `TTL = 300 s` in **`0.5346 ms`**.

---

### 3.3 Required Screenshot 1: Display Filter Applied

Applying the Wireshark display filter `ip.addr == 172.22.31.69 and tcp.port == 443` isolates all **36 HTTPS frames** (Frames 3--38, `22,785` bytes on wire) between the UniLlanos client (`172.22.201.2:52382`) and the Seneca server (`172.22.31.69:443`) while suppressing the 8 background UDP frames:

![Wireshark Display Filter](figuras/wireshark_1_filtered_traffic.png)
*Figure 3.1: Wireshark packet list with the display filter `ip.addr == 172.22.31.69 and tcp.port == 443` applied, isolating all 36 frames (`22,785` B wire, `0.4083 s` duration) of the HTTPS conversation between `172.22.201.2:52382` and `172.22.31.69:443`.*

---

### 3.4 Required Screenshot 2: Initial TCP 3-Way Handshake (Frames 3--5)

Reliable connection-oriented transport begins with the RFC 9293 three-way handshake captured in **Frames 3, 4, and 5**:

![TCP Handshake](figuras/wireshark_2_tcp_handshake.png)
*Figure 3.2: Wireshark packet details for the initial TCP three-way handshake (Frames 3--5), confirming `MSS=1260` matching the `1300 B` ZeroTier MTU minus `40 B` IPv4/TCP headers, `WS=256` scaling to `Win=65280`, `SACK_PERM`, and a `14.21 ms` handshake RTT.*

#### Protocol Dissection:
1. **Frame 3 (`[SYN]`, `0.2392395 s`, `66 B` wire):**  
   - **Flow:** `172.22.201.2:52382 -> 172.22.31.69:443`  
   - **Parameters:** Relative `Seq=0`, `Win=65535`, `Len=0`, TCP options (`12 B`): `MSS=1260`, Window Scale `WS=256` (shift count 8), and Selective Acknowledgment Permitted (`SACK_PERM`).
2. **Frame 4 (`[SYN, ACK]`, `0.2534503 s`, `66 B` wire):**  
   - **Flow:** `172.22.31.69:443 -> 172.22.201.2:52382`  
   - **Parameters:** Relative `Seq=0`, `Ack=1`, `Win=65535`, `Len=0`, symmetric options `MSS=1260`, `WS=256`, `SACK_PERM`. The timestamp delta between Frame 3 and Frame 4 yields an empirical SD-WAN TCP handshake RTT of **`14.21 ms`** (`0.0142108 s`).
3. **Frame 5 (`[ACK]`, `0.2535554 s`, `54 B` wire):**  
   - **Flow:** `172.22.201.2:52382 -> 172.22.31.69:443`  
   - **Parameters:** Relative `Seq=1`, `Ack=1`, `Len=0`, calculated scaled receive window **`Win=65280`** (`255 * 256`). Both endpoints transition to `ESTABLISHED`.
   - **MTU/MSS Calibration Proof:** Subtracting the `20 B` IPv4 header and `20 B` base TCP header (`40 B` total) from the tuned `1300 B` ZeroTier MTU yields exactly `MSS = 1300 - 40 = 1260 B`.

---

### 3.5 Required Screenshot 3: Cryptographic TLS 1.3 Data Exchange (Frames 6--35)

Immediately following TCP synchronization, **Frames 6--35** execute the RFC 8446 TLS 1.3 1-RTT cryptographic handshake and encrypted HTTP/1.1 payload transfer:

![TLS Exchange](figuras/wireshark_3_tls_data_exchange.png)
*Figure 3.3: Wireshark inspection of the TLS 1.3 cryptographic handshake and encrypted HTTP/1.1 payload exchange (Frames 6--35), showing reassembled `Client Hello` (`1479 B` in Frame 7, `SNI=www.coil-group2.com`), 1-RTT `Server Hello` in Frame 9 selecting `TLS_AES_256_GCM_SHA384` (`0x1302`), encrypted `GET /seneca/ HTTP/1.1` in Frame 15, and `1260 B`-MSS segmented delivery of the `15,470 B` Seneca HTML response up to relative server `Seq=19136`.*

#### Protocol Dissection:
1. **Frames 6--7 (Segmented & Reassembled `Client Hello`, `0.2543708 s`):**  
   - The client generates a `1479 B` TLS 1.3 `Client Hello` record containing Server Name Indication (`SNI=www.coil-group2.com`), `supported_versions` (`TLS 1.3`), AEAD cipher suites `0x1302` (`TLS_AES_256_GCM_SHA384`), `0x1303` (`TLS_CHACHA20_POLY1305_SHA256`), and `0x1301` (`TLS_AES_128_GCM_SHA256`), and hybrid key share groups (`X25519MLKEM768` and `x25519`). Because `1479 B` exceeds `MSS=1260`, TCP segments the record across **Frame 6** (`1260 B`) and **Frame 7** (`219 B`), which Wireshark reassembles in Frame 7 (`1260 + 219 = 1479 B`).
2. **Frames 9--12 (1-RTT `Server Hello` & Encrypted Handshake Flight, `0.2732436 s`):**  
   - After acknowledging Frame 7 (`Ack=1480` in Frame 8), the server responds in **Frame 9** with `Server Hello` selecting cipher suite **`TLS_AES_256_GCM_SHA384` (`0x1302`)** and `x25519` key share, followed by `Change Cipher Spec` and encrypted handshake records across Frames 9, 10, and 12 (`2900 B` total flight: `Encrypted Extensions`, the X.509 certificate chain anchored to `COIL Group 2 Root CA`, `CertificateVerify`, and `Finished`).
3. **Frames 13--16 (Client `Finished`, Session Tickets, and Encrypted HTTP GET Request):**  
   - In **Frame 13** (`0.2744180 s`, `80 B` payload), the client transmits `Change Cipher Spec` and its encrypted `Finished` record. The server delivers two post-handshake TLS 1.3 session tickets in **Frames 14 and 16** (`255 B` payload each). In **Frame 15** (`0.2874402 s`, `178 B` wire, `124 B` TLS application payload, `Seq=1560..1683`), the client transmits the encrypted `GET /seneca/ HTTP/1.1` request.
4. **Frames 17--35 (MSS-Segmented Encrypted HTML Delivery):**  
   - The server transmits the HTTP `200 OK` response headers (`264 B`) and the complete **`15,470 B` Seneca HTML document** (`15,734 B` plaintext HTTP stream) inside TLS 1.3 `Application Data` records. Bulk transfer frames (Frames 17, 19--20, 22--23, 25--26, 28--29, 31--32, and 34) each carry exactly **`1260 B`** of TCP payload (`1314 B` wire), concluding with a `658 B` payload in **Frame 35** that advances the server's relative sequence number to **`Seq=19136`**.

---

### 3.6 Required Screenshot 4: Clean 4-Way TCP Connection Teardown (Frames 35--38)

Upon delivering the final encrypted HTML bytes, the session closes via an orderly four-way FIN handshake in **Frames 35--38**:

![TCP Teardown](figuras/wireshark_4_tcp_teardown.png)
*Figure 3.4: Wireshark inspection of the clean four-way TCP connection teardown (Frames 35--38), showing server `[FIN, PSH, ACK]` (`Seq=18477, Ack=1684, Len=658`), client `[ACK]` (`Ack=19136`), client `[FIN, ACK]`, and final server `[ACK]` (`Ack=1685`) with zero `RST` packets.*

#### Protocol Dissection:
1. **Frame 35 (Server `[FIN, PSH, ACK]`, `0.3358339 s`, `712 B` wire):**  
   - `172.22.31.69:443 -> 172.22.201.2:52382`, `Seq=18477`, `Ack=1684`, `Len=658`. The server piggybacks `FIN` onto the concluding `658 B` TLS record, advancing its cumulative sequence number by `658 + 1 = 659` to `19136`.
2. **Frame 36 (Client `[ACK]`, `0.3359537 s`, `54 B` wire):**  
   - `172.22.201.2:52382 -> 172.22.31.69:443`, `Seq=1684`, `Ack=19136`, `Len=0`. The client acknowledges the server's final data segment and `FIN` within `0.1198 ms`.
3. **Frame 37 (Client `[FIN, ACK]`, `0.6367030 s`, `54 B` wire):**  
   - `172.22.201.2:52382 -> 172.22.31.69:443`, `Seq=1684`, `Ack=19136`, `Len=0`. The client closes its transmit half-channel.
4. **Frame 38 (Server `[ACK]`, `0.6475791 s`, `54 B` wire):**  
   - `172.22.31.69:443 -> 172.22.201.2:52382`, `Seq=19136`, `Ack=1685`, `Len=0`. Final acknowledgment completing the HTTPS conversation in **`0.4083 s`** with **`0` `RST` packets**.

---

# SECTION 4 (50%): Detailed Step-by-Step Manuals & Source Code

---

## MANUAL 1 (10%): ZeroTier SD-WAN Setup, Static IP Pinning & MTU Configuration

### Objective
Deploy a private Software-Defined Wide Area Network connecting distributed Windows and Android computing nodes over the public Internet via ZeroTier VL1/VL2 overlay tunnels with deterministic IP addressing and fragmentation-free MTU clamping.

### Step 1: Account & Controller Initialization
1. Navigate to [ZeroTier Central](https://my.zerotier.com) and authenticate.
2. Click **Create A Network** to allocate the 64-bit Network ID `abfd31bd47affa39`.
3. Under **Settings -> Basics**, configure:
   - **Name:** `COIL Group 2 SD-WAN - UniLlanos & Seneca`
   - **Access Control:** `Private` (Ensures unauthorized Node IDs cannot join or exchange VL2 frames).

### Step 2: Managed Routing, IPv4 Pool, Multicast & DNS Push
1. Under **Settings -> Advanced -> Managed Routes**, define the on-link virtual subnetwork:
   - **Target:** `172.22.0.0/16` | **Via:** *(leave blank for LAN on-link routing)*
2. Under **IPv4 Auto-Assign**, select **Easy** mode and highlight the `172.22.*.*` pool (`172.22.0.1` to `172.22.255.254`).
3. Leave all three **IPv6 Auto-Assign** options (*RFC4193*, *6PLANE*, *Auto-Assign from Range*) unchecked to maintain pure IPv4 SD-WAN routing.
4. Set **Multicast Recipient Limit** to `32` and check **Enable Broadcast**.
5. Under **DNS**, configure **Search Domain:** `coil-group2.com` and **Server Address:** `172.22.201.2` so ZeroTier 1.6+ endpoints receive the authoritative SD-WAN DNS resolver automatically:

![ZeroTier Central Advanced Settings](figuras/zerotier_settings_dns_fresh.png)
*Figure 4.1: ZeroTier Central advanced configuration console for Network ID `abfd31bd47affa39`, showing 5/10 included devices, disabled IPv6 auto-assignment, Multicast Recipient Limit (32) with Broadcast enabled, and authoritative DNS push (`coil-group2.com` -> `172.22.201.2`).*

### Step 3: Endpoint Software Installation, Elevated Join & MTU Clamping
On Windows endpoints (`v1.16.2 x86_64`), install ZeroTier One, join network `abfd31bd47affa39` from an elevated Administrator PowerShell prompt, and clamp the virtual interface MTU to `1300` bytes (`MSS = 1260` bytes):
```powershell
# 1. Install ZeroTier One (v1.16.2 x86_64) via winget
winget install zerotier.zerotierone --silent `
  --accept-package-agreements --accept-source-agreements

# 2. Join SD-WAN from elevated Administrator PowerShell
zerotier-cli join abfd31bd47affa39
zerotier-cli listnetworks

# 3. Clamp virtual interface MTU to 1300 B (MSS = 1260 B)
Set-NetIPInterface `
  -InterfaceAlias "ZeroTier One [abfd31bd47affa39]" `
  -AddressFamily IPv4 -NlMtuBytes 1300
netsh interface ipv4 show subinterfaces
```
On Android mobile endpoints (`v1.16.0 arm64`), install ZeroTier One from Google Play, tap **Add Network**, enter `abfd31bd47affa39`, and enable **Use Network DNS**.

### Step 4: Authorization, Role Labeling & Static IP Pinning in ZeroTier Central
In the **Members** panel of ZeroTier Central (Figure 1.1), check the **Auth** checkbox for all five endpoints, assign institutional role labels, and verify the pinned `172.22.x.x` overlay leases:
- `aed30a4fdd` -> `Miguel Rodriguez - Unillanos Website Server` (`172.22.201.2/16`, Windows `v1.16.2`, `181.51.34.123`)
- `1c84e39095` -> `Seneca College - Simulated Gateway` (`172.22.31.69/16`, Windows `v1.16.2`, `181.51.34.123`)
- `b63d8aeba8` -> `Luis Alejandro Leon - Student Client` (`172.22.100.11`, `172.22.164.74`, Windows `v1.16.2`, `181.51.34.104`)
- `f6fcd4ce4d` -> `Luis Alejandro Leon - Student Client` (`172.22.100.10`, Android `v1.16.0`, `181.51.34.104`)
- `8eb3130d2c` -> `Miguel Rodriguez - Student Client` (`172.22.38.108`, `172.22.201.50`, Android `v1.16.0`, `181.51.34.123`)

---

## MANUAL 2 (10%): Multi-Tenant Web Server Creation & Intranet UI Deployment

### Objective
Implement a production threaded, non-blocking multi-tenant HTTP/1.1 web server (`COIL-DualIntranet/2.0`) delivering dual cultural intranet websites over TLS 1.3 (port 443) and fallback HTTP (port 80) across the SD-WAN.

### Step 1: Directory Structure
All certificates, DNS services, server scripts, and HTML5/CSS3 assets reside under `modulo2/`:
```text
modulo2/
├── certificados/       # Root CA (COIL_Group2_Root_CA.crt), openssl.cnf, server-key.pem, fullchain.pem
├── dns/                # Authoritative dnslib server (dns_server.py) and setup_hosts.ps1
├── servidor/           # Non-blocking threaded HTTPS/HTTP server (server_https.py)
└── sitio_web/          # Responsive HTML5/CSS3 intranet portals
    ├── portal/         # Dual Intranet Gateway Portal (index.html, 6,941 B)
    ├── unillanos/      # Universidad de los Llanos Intranet (index.html, 18,520 B + 12 images in img/)
    └── seneca/         # Seneca Polytechnic Intranet (index.html, 15,470 B + 7 images in img/)
```

### Step 2: Multi-Tenant Server Engine (`COIL-DualIntranet/2.0`)
`modulo2/servidor/server_https.py` implements:
- **`NonBlockingSSLThreadingServer`:** Inherits from `socketserver.ThreadingMixIn` and `http.server.HTTPServer` (`daemon_threads = True`, `request_queue_size = 32`) and performs `ssl_context.wrap_socket()` inside worker threads with a `10.0 s` handshake timeout and `15.0 s` read timeout so stalled clients never block the main accept loop. Moreover, closing directly via `close_request()` without premature Winsock `shutdown(SHUT_WR)` guarantees graceful 4-way TCP `FIN` teardowns (`0` `RST` packets).
- **`DualIntranetHandler`:** Routes requests by `Host` header (`unillanos.*` and `seneca.*`) and URI prefix (`/`, `/unillanos/`, `/seneca/`), distributes `/ca.crt` (`application/x-x509-ca-cert`), prevents directory traversal via `os.path.normpath()`, and emits `Connection: close`, `Cache-Control: no-cache`, and `X-Content-Type-Options: nosniff`.

### Step 3: Windows Firewall Rules & Headless S4U Scheduled Task Persistence
Open inbound TCP ports 443 and 80 and register a persistent Windows Scheduled Task (`COIL_HTTPS_Daemon`) using `S4U` logon so `python.exe -u` runs headlessly in the background without `pythonw.exe` null-`stderr` crashes or SSH Job-Object termination:
```powershell
New-NetFirewallRule -DisplayName "COIL_HTTPS_443" `
  -Direction Inbound -Protocol TCP -LocalPort 443 -Action Allow
New-NetFirewallRule -DisplayName "COIL_HTTP_80" `
  -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow

$act = New-ScheduledTaskAction `
  -Execute "python.exe" `
  -Argument "-u C:\COIL_Server\servidor\server_https.py" `
  -WorkingDirectory "C:\COIL_Server"
$prin = New-ScheduledTaskPrincipal `
  -UserId $env:USERNAME -LogonType S4U
Register-ScheduledTask -TaskName "COIL_HTTPS_Daemon" `
  -Action $act -Principal $prin -Force
Start-ScheduledTask -TaskName "COIL_HTTPS_Daemon"
```

### Step 4: Intranet User Interface (UI/GUI) Verification
1. **Dual Intranet Gateway Portal (`https://www.coil-group2.com/`, `6,941 B`):** Features the *SD-WAN Infrastructure Online* badge, interactive `UL` and `SC` institutional routing cards, and the bottom SD-WAN telemetry bar (`ZeroTier Virtual Ethernet`, `172.22.201.2`, `TLS 1.3 / HTTPS (Port 443)`, `www.coil-group2.com`).

![COIL Gateway Portal UI](figuras/ui_portal_fresh.png)
*Figure 4.2: COIL Group 2 Dual Intranet Gateway Portal (`portal/index.html`, `6,941 B`) rendered at `https://www.coil-group2.com/`.*

2. **Universidad de los Llanos Cultural Intranet (`https://www.coil-group2.com/unillanos/`, `18,520 B`):** Features the sticky `UL` navigation bar with the *Switch to Seneca Intranet* button, Villavicencio panorama hero with glassmorphism telemetry pill, eight cultural cards (*Carne a la Llanera (Mamona)*, *Caldo de Costilla*, *Hayaca Llanera*, *Torneo del Joropo & Joropodromo*, *Sunsets of the Orinoco Basin*, *Villavicencio Metropolis*, *Cano Cristales: River of Five Colors*, *UniLlanos Barcelona Campus*), and the *UniLlanos Engineering Team* showcase.

![UniLlanos Cultural Intranet UI](figuras/ui_unillanos_fresh.png)
*Figure 4.3: Universidad de los Llanos Cultural Intranet (`unillanos/index.html`, `18,520 B`) rendered at `https://www.coil-group2.com/unillanos/`.*

3. **Seneca Polytechnic Cultural Intranet (`https://www.coil-group2.com/seneca/`, `15,470 B`):** Features the sticky `SC` navigation bar with the *Switch to UniLlanos Intranet* button, partner gateway telemetry pill, and eight cards covering Toronto landmarks (*CN Tower & Downtown Skyline*, *Lake Ontario & Toronto Islands*), Canadian heritage (*Ice Hockey & Outdoor Rinks*, *Maple Syrup & Sugar Shacks*), culinary classics (*Authentic Poutine*, *Peameal Bacon & Butter Tarts*), and bilateral IT academics.

![Seneca Polytechnic Cultural Intranet UI](figuras/ui_seneca_fresh.png)
*Figure 4.4: Seneca Polytechnic Cultural Intranet (`seneca/index.html`, `15,470 B`) rendered at `https://www.coil-group2.com/seneca/`.*

---

## MANUAL 3 (15%): Self-Signed SSL/TLS PKI & Browser Trust Authority (Bonus Solution)

### Objective
Engineer a two-tier private Public Key Infrastructure (PKI) with a custom 2048-bit RSA Root Certificate Authority (`COIL Group 2 Root CA`) and an X.509v3 Subject Alternative Name (SAN) server leaf certificate, eliminating browser security warnings (`NET::ERR_CERT_AUTHORITY_INVALID`) across Windows and Android endpoints.

### Step 1: OpenSSL X.509v3 Configuration Policy (`modulo2/certificados/openssl.cnf`)
Define both `[v3_ca]` (`CA:true`, `keyCertSign`, `cRLSign`) and `[server_ext]` (`CA:FALSE`, `serverAuth`, `clientAuth`, `subjectAltName = @alt_names`) binding all five project DNS names and four IPv4 literals:
```ini
[ server_ext ]
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid,issuer
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
IP.3  = 10.51.76.174
IP.4  = 127.0.0.1
```

### Step 2: Root CA Generation (3650 Days) & Leaf Signing (825 Days)
```powershell
# 1. Generate 2048-bit RSA Root CA Key and Self-Signed Root Certificate (10 years)
openssl genrsa -out ca-key.pem 2048
openssl req -x509 -new -nodes -key ca-key.pem -sha256 -days 3650 `
  -out ca-cert.pem -config openssl.cnf -extensions v3_ca
Copy-Item ca-cert.pem COIL_Group2_Root_CA.crt

# 2. Generate 2048-bit Server Key, CSR, and SAN Leaf Certificate (825 days)
openssl genrsa -out server-key.pem 2048
openssl req -new -key server-key.pem -out server.csr `
  -config openssl.cnf -reqexts server_ext
openssl x509 -req -in server.csr -CA ca-cert.pem -CAkey ca-key.pem `
  -CAcreateserial -out server.crt -days 825 -sha256 `
  -extfile openssl.cnf -extensions server_ext
Get-Content server.crt, ca-cert.pem | Set-Content fullchain.pem -Encoding ascii
```

| Cryptographic Parameter | Tier 1: Offline Root CA (`COIL_Group2_Root_CA.crt`) | Tier 2: Server Leaf Certificate (`server.crt` / `fullchain.pem`) |
|---|---|---|
| **Subject DN** | `C=CO, ST=Meta, L=Villavicencio, O=COIL International Project, CN=COIL Group 2 Root CA` | `C=CO, ST=Meta, L=Villavicencio, O=UniLlanos & Seneca Polytechnic, CN=www.coil-group2.com` |
| **Issuer DN** | `CN=COIL Group 2 Root CA` (Self-Signed Root Anchor) | `CN=COIL Group 2 Root CA` (Signed by Tier 1 Root Key) |
| **Public Key & Signature** | RSA `2048 bit`, `sha256WithRSAEncryption` | RSA `2048 bit`, `sha256WithRSAEncryption` |
| **Serial Number (Hex)** | `1CB6CA4983D9BDB6F5CD48F319471E43769657D0` | `173DF529332DD2C5FF047CBF0AE1786A4B1487D7` |
| **Validity Window** | Nov 21, 2026 -- Nov 18, 2036 (`3650 days`) | Nov 21, 2026 -- Feb 23, 2029 (`825 days`) |
| **SHA-256 Fingerprint** | `03:F5:C7:F3:3C:53:40:75:A1:D4:E3:CF:40:D0:4D:A8:BD:D3:A6:1F:44:59:76:89:66:69:C4:6E:AA:92:6E:E7` | `EE:F4:29:54:5D:89:F0:B2:2F:06:D4:8F:FC:C2:59:51:A4:0E:6B:B4:6F:87:E4:43:42:6B:4D:FE:22:10:1E:A3` |

### Step 3: Installing Root CA into Client OS Trust Stores (Bonus Verification)
On Windows endpoints, import `COIL_Group2_Root_CA.crt` into the Trusted Root Certification Authorities store (Thumbprint `6C947986AF9F0C4782255C86F604A2D4D442E0D9`):
```powershell
Import-Certificate -FilePath "modulo2\certificados\COIL_Group2_Root_CA.crt" `
  -CertStoreLocation "Cert:\LocalMachine\Root"
Import-Certificate -FilePath "modulo2\certificados\COIL_Group2_Root_CA.crt" `
  -CertStoreLocation "Cert:\CurrentUser\Root"
```
On Android endpoints, download `http://172.22.201.2/ca.crt` and install it under *Settings -> Security and privacy -> More security settings -> Install from device storage -> CA certificate*.

![Chrome Trusted Certificate](figuras/cert_chrome_trusted_fresh.png)
*Figure 4.5a: Live Google Chrome verification on Windows navigating to `https://www.coil-group2.com/seneca/` with the site security panel confirming a trusted HTTPS connection and zero certificate warnings.*

![X.509 Certificate Viewer](figuras/cert_viewer_details_fresh.png)
*Figure 4.5b: Native X.509 Certificate Viewer inspection confirming the validated trust chain from `COIL Group 2 Root CA` to leaf certificate `www.coil-group2.com`.*

![Android Mobile Verification](figuras/cert_mobile_android.jpg)
*Figure 4.5c: Cross-platform mobile verification on Android (Samsung Galaxy S24+, ZeroTier VPN active) accessing `www.coil-group2.com/unillanos/` over TLS 1.3 with the Root CA installed.*

---

## MANUAL 4 (15%): Authoritative & Forwarding DNS Server Configuration

### Objective
Enable domain-based URL navigation (`www.coil-group2.com/unillanos/` and `www.coil-group2.com/seneca/`) across all SD-WAN endpoints via an RFC 1035 and RFC 2308 compliant authoritative UDP/53 DNS daemon (`modulo2/dns/dns_server.py`).

### Step 1: Authoritative Zone & RFC 2308 Negative Caching Engine (`dnslib`)
The DNS server listens on `UDP 0.0.0.0:53` (with `SIO_UDP_CONNRESET = False` on Windows) and resolves all four COIL hostnames to `172.22.201.2` (`TTL = 300 s`):
- **Type `A` (1) & `ANY` (255):** Returns an authoritative `NOERROR` reply (`AA=1`) with `rdata=A("172.22.201.2")`.
- **Type `AAAA` (28) & `HTTPS` (65) (`NODATA+SOA`):** Returns `NOERROR` with zero answer records and an authoritative `SOA` record (`ns.coil-group2.com`, `admin.coil-group2.com`, serial `2026112101`) in the authority section per RFC 2308, preventing Android `netd` stub resolvers from failing with `FORMERR`.
- **Unregistered `*.coil-group2.com` Subdomains (`NXDOMAIN+SOA`):** Returns `RCODE.NXDOMAIN` with the authoritative `SOA` record.
- **External Domains:** Forwards non-COIL queries upstream to `8.8.8.8:53` (`2.0 s` timeout).

### Step 2: Windows Port 53 Service Provisioning & Live Verification
Stop `SharedAccess` (if reserving UDP/53), open firewall rule `COIL_DNS_53`, and register the `COIL_DNS_Daemon` S4U Scheduled Task:
```powershell
Stop-Service SharedAccess -Force -ErrorAction SilentlyContinue
New-NetFirewallRule -DisplayName "COIL_DNS_53" -Direction Inbound `
  -Protocol UDP -LocalPort 53 -Action Allow
$action = New-ScheduledTaskAction -Execute "python.exe" `
  -Argument '-u "modulo2\dns\dns_server.py"'
$principal = New-ScheduledTaskPrincipal -UserId (whoami) `
  -LogonType S4U -RunLevel Highest
Register-ScheduledTask -TaskName "COIL_DNS_Daemon" -Action $action `
  -Principal $principal -Force
Start-ScheduledTask -TaskName "COIL_DNS_Daemon"
```

Verify both `Type A` and `Type AAAA` (`NODATA+SOA`) responses from PowerShell:
```powershell
PS C:\> Resolve-DnsName www.coil-group2.com -Server 172.22.201.2 -Type A
Name                 Type   TTL   Section    IPAddress
----                 ----   ---   -------    ---------
www.coil-group2.com  A      300   Answer     172.22.201.2

PS C:\> Resolve-DnsName www.coil-group2.com -Server 172.22.201.2 -Type AAAA
Name             Type  TTL  Section    PrimaryServer       NameAdministrator     SerialNumber
----             ----  ---  -------    -------------       -----------------     ------------
coil-group2.com  SOA   300  Authority  ns.coil-group2.com  admin.coil-group2.com 2026112101
```

![Wireshark DNS Resolution](figuras/wireshark_5_dns_resolution.png)
*Figure 4.6: Wireshark protocol dissection of the live SD-WAN DNS query and authoritative response (Frames 1--2, Transaction ID `0x9121`, `0.5346 ms` RTT) resolving `www.coil-group2.com` to `172.22.201.2` (`TTL = 300 s`) over UDP port 53.*

---

# SECTION 5: Quantitative Engineering Analysis & Root-Cause Discussion

### 5.1 Cross-Layer Quantitative Comparison vs. Theoretical Baselines

| Metric / Subsystem | Theoretical / Spec. Baseline | Live Measured SD-WAN Value | Relative Deviation / Overhead |
|---|---|---|---|
| **Maximum Segment Size (MSS)** | Standard Ethernet (`1500 B` MTU -> `1460 B` MSS) | Tuned ZeroTier overlay (`1300 B` MTU -> **`1260 B` MSS** in Frames 3--4) | **`-13.70%`** intentional reduction (`200 B` encapsulation headroom preventing cellular/PPPoE fragmentation) |
| **LAN P2P Overlay Latency** | Direct Gigabit Ethernet (`~0.50 ms` RTT) | ZeroTier UDP/9993 P2P tunnel (**`6.0 ms`--`10.0 ms`** avg ICMP RTT; **`14.21 ms`** TCP SYN/SYN-ACK) | `+5.5 ms` to `+9.5 ms` over bare LAN due to VL1 encryption and user-space TUN/TAP processing |
| **WAN P2P Overlay Latency** | ZeroTier LAN overlay baseline (`10.0 ms` avg RTT) | Partner ISP WAN leaf (`172.22.100.11` / `172.22.164.74`: **`23.0 ms`--`31.0 ms`** avg ICMP RTT, **`0%` loss**) | `+13.0 ms` to `+21.0 ms` Internet routing propagation delta across cross-ISP underlay hops |
| **Authoritative DNS Lookup** | Local OS cache / `hosts` lookup (`< 0.10 ms`) | Live remote `dnslib` UDP/53 query (**`0.5346 ms`** in Frame 2, TxID `0x9121`) | Sub-millisecond SD-WAN name resolution (`0.27%` of a `200 ms` interactive UX budget) |
| **TLS 1.3 + TCP Wire Overhead** | Plaintext HTTP payload (**`15,470 B`** Seneca HTML; `15,734 B` with HTTP headers) | **`22,785 B`** bidirectional wire bytes across 36 TCP/TLS frames (`19,134 B` server TCP payload, `Seq=19136`) | **`47.29%`** total framing + TLS 1.3 1-RTT handshake/AEAD record overhead (`7,315 B` delta over raw HTML) |
| **PCAP Deliverable vs. Limit** | Rubric upper cap (`10.0 MB` = `10,240 KB`) | Captured `coil_sdwan_https_traffic.pcapng` (**`24.81 KB` = `25,408 B`**) | **`99.76%`** safety margin below cap (`0.24%` budget utilization) |

### 5.2 Root-Cause Troubleshooting Summary
1. **Search Domain Suffix Loop & Android Private DNS Bypass:** Clearing duplicate search-domain expansion and turning off Android Private DNS (DoT port 853) ensured mobile queries routed directly to `172.22.201.2:53`.
2. **RFC 2308 Authority SOA on `NODATA` Replies:** Appending `SOA_RECORD` (`ns.coil-group2.com`) on `Type 28 (AAAA)` and `Type 65 (HTTPS)` queries eliminated Android `netd` `FORMERR` rejections.
3. **Eliminating Windows Winsock `TCP RST` on Socket Closure:** Overriding `process_request_thread` and `close_request` in `NonBlockingSSLThreadingServer` with `Connection: close` avoided premature `shutdown(SHUT_WR)` resets, yielding 0 `RST` packets across Frames 35--38.
4. **Headless S4U Persistence vs. `pythonw.exe` Null `sys.stderr`:** Guarding `sys.stderr`/`sys.stdout` in Python and running `python.exe -u` under Windows Task Scheduler (`S4U`) prevented detached GUI-subsystem `AttributeError` exceptions and SSH session termination.
5. **Windows Schannel Offline Revocation Check (`CRYPT_E_NO_REVOCATION_CHECK`):** Because the private PKI operates offline without public CRL/OCSP responders, Chromium and Android validate the Root CA directly while CLI Schannel tests use `--ssl-no-revoke`.

---

# APPENDIX: Production Source Code Repository

### A.1 Python Multi-Tenant HTTPS/HTTP Web Server (`modulo2/servidor/server_https.py`)
```python
#!/usr/bin/env python3
"""
COIL Group 2 - Dual Intranet HTTPS Server (Production Threaded)
Universidad de los Llanos & Seneca Polytechnic
Authors: Miguel Rodriguez Payares & Luis Alejandro Leon Velasquez
"""

import http.server
import socketserver
import ssl
import socket
import os
import sys
import mimetypes
import urllib.parse
import threading

PORT = 443
HOST = "0.0.0.0"

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITIO_DIR = os.path.join(BASE_DIR, "sitio_web")
CERTS_DIR = os.path.join(BASE_DIR, "certificados")

PORTAL_DIR = os.path.join(SITIO_DIR, "portal")
UNILLANOS_DIR = os.path.join(SITIO_DIR, "unillanos")
SENECA_DIR = os.path.join(SITIO_DIR, "seneca")

CERT_FILE = os.path.join(CERTS_DIR, "fullchain.pem")
KEY_FILE = os.path.join(CERTS_DIR, "server-key.pem")

class DualIntranetHandler(http.server.BaseHTTPRequestHandler):
    server_version = "COIL-DualIntranet/2.0"
    protocol_version = "HTTP/1.1"
    timeout = 15

    def do_HEAD(self):
        self.close_connection = True
        self.do_GET(head_only=True)

    def do_GET(self, head_only=False):
        self.close_connection = True
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        host = self.headers.get("Host", "").lower().split(":")[0]

        if host.startswith("unillanos.") and not path.startswith("/unillanos"):
            path = "/unillanos" + path
        elif host.startswith("seneca.") and not path.startswith("/seneca"):
            path = "/seneca" + path

        if path == "/data":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(b"{}")
            return

        if path in ("/ca.crt", "/COIL_Group2_Root_CA.crt"):
            ca_file = os.path.join(CERTS_DIR, "COIL_Group2_Root_CA.crt")
            if os.path.exists(ca_file):
                with open(ca_file, "rb") as f:
                    ca_content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/x-x509-ca-cert")
                self.send_header("Content-Disposition", 'attachment; filename="COIL_Group2_Root_CA.crt"')
                self.send_header("Content-Length", str(len(ca_content)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(ca_content)
                return

        if path == "/unillanos":
            self.send_response(301)
            self.send_header("Location", "/unillanos/")
            self.send_header("Connection", "close")
            self.end_headers()
            return
        if path == "/seneca":
            self.send_response(301)
            self.send_header("Location", "/seneca/")
            self.send_header("Connection", "close")
            self.end_headers()
            return

        if path.startswith("/unillanos/"):
            rel_path = path[len("/unillanos/"):]
            if not rel_path or rel_path == "/":
                rel_path = "index.html"
            file_path = os.path.join(UNILLANOS_DIR, rel_path)
        elif path.startswith("/seneca/"):
            rel_path = path[len("/seneca/"):]
            if not rel_path or rel_path == "/":
                rel_path = "index.html"
            file_path = os.path.join(SENECA_DIR, rel_path)
        elif path == "/" or path == "/index.html":
            file_path = os.path.join(PORTAL_DIR, "index.html")
        else:
            rel_path = path.lstrip("/")
            file_path = os.path.join(PORTAL_DIR, rel_path)

        file_path = os.path.normpath(file_path)
        if not (file_path.lower().startswith(SITIO_DIR.lower())):
            self.send_error(403, "Access Forbidden")
            return

        if not os.path.exists(file_path) or os.path.isdir(file_path):
            self.send_error(404, f"File Not Found: {path}")
            return

        ctype, _ = mimetypes.guess_type(file_path)
        if not ctype:
            if file_path.endswith(".webp"):
                ctype = "image/webp"
            elif file_path.endswith(".avif"):
                ctype = "image/avif"
            else:
                ctype = "application/octet-stream"

        try:
            with open(file_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Connection", "close")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("X-Content-Type-Options", "nosniff")
            if isinstance(self.request, ssl.SSLSocket):
                self.send_header("Strict-Transport-Security", "max-age=0")
            self.end_headers()
            if not head_only:
                self.wfile.write(content)
            self.close_connection = True
        except Exception as e:
            try:
                self.send_error(500, f"Internal Server Error: {e}")
            except Exception:
                pass

    def log_message(self, format, *args):
        client_ip = self.client_address[0] if self.client_address else "unknown"
        try:
            if sys.stderr:
                sys.stderr.write(f"[{self.log_date_time_string()}] {client_ip} - {format % args}\n")
                sys.stderr.flush()
        except Exception:
            pass

class NonBlockingSSLThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    request_queue_size = 32

    def __init__(self, server_address, RequestHandlerClass, ssl_context):
        super().__init__(server_address, RequestHandlerClass)
        self.ssl_context = ssl_context

    def process_request_thread(self, request, client_address):
        ssl_sock = None
        try:
            request.settimeout(10.0)
            ssl_sock = self.ssl_context.wrap_socket(request, server_side=True)
            ssl_sock.settimeout(15.0)
            self.finish_request(ssl_sock, client_address)
        except (ssl.SSLError, socket.timeout, ConnectionResetError, BrokenPipeError, Exception):
            pass
        finally:
            self.close_request(ssl_sock if ssl_sock else request)

    def close_request(self, request):
        try:
            request.close()
        except Exception:
            pass

def run():
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None:
            setattr(sys, stream_name, open(os.devnull, "w"))

    def start_http_server():
        http_server = socketserver.ThreadingTCPServer(("0.0.0.0", 80), DualIntranetHandler)
        http_server.daemon_threads = True
        http_server.serve_forever()

    threading.Thread(target=start_http_server, daemon=True).start()

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    ssl_context.set_alpn_protocols(["http/1.1"])

    httpd = NonBlockingSSLThreadingServer((HOST, PORT), DualIntranetHandler, ssl_context)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
```

### A.2 Authoritative & Forwarding DNS Server (`modulo2/dns/dns_server.py`)
```python
#!/usr/bin/env python3
"""
COIL Group 2 - Authoritative & Forwarding DNS Server (dnslib RFC 1035 / RFC 2308 Compliant)
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

def run_dns():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if hasattr(socket, "SIO_UDP_CONNRESET"):
        try:
            sock.ioctl(socket.SIO_UDP_CONNRESET, False)
        except Exception:
            pass
    sock.bind((LISTEN_ADDR, PORT))

    while True:
        data, addr = sock.recvfrom(4096)
        request = DNSRecord.parse(data)
        qname = str(request.q.qname).rstrip('.').lower()
        qtype = request.q.qtype

        if qname in DOMAINS:
            reply = request.reply()
            if qtype in (QTYPE.A, QTYPE.ANY):
                reply.add_answer(RR(request.q.qname, QTYPE.A, rdata=A(DOMAINS[qname]), ttl=300))
            else:
                reply.add_auth(RR("coil-group2.com", QTYPE.SOA, rdata=SOA_RECORD, ttl=300))
            sock.sendto(reply.pack(), addr)
        elif qname.endswith(".coil-group2.com"):
            reply = request.reply()
            reply.header.rcode = RCODE.NXDOMAIN
            reply.add_auth(RR("coil-group2.com", QTYPE.SOA, rdata=SOA_RECORD, ttl=300))
            sock.sendto(reply.pack(), addr)
        else:
            resp = forward_query(data)
            if resp:
                sock.sendto(resp, addr)

if __name__ == "__main__":
    run_dns()
```

---

## Conclusion

Module 2 has been comprehensively engineered, deployed, and forensically verified across all five authorized ZeroTier SD-WAN endpoints (`abfd31bd47affa39`, `172.22.0.0/16`, `1300 B` MTU). The dual-tenant `COIL-DualIntranet/2.0` HTTPS infrastructure and `dnslib` authoritative UDP/53 DNS server enable seamless domain-based navigation (`www.coil-group2.com/unillanos/` and `www.coil-group2.com/seneca/`) secured by TLS 1.3 (`TLS_AES_256_GCM_SHA384`) and our locally trusted 2048-bit RSA Root Certificate Authority (`COIL Group 2 Root CA`). Deep Packet Inspection of `modulo2/wireshark/coil_sdwan_https_traffic.pcapng` (`25,408` bytes = `24.81 KB`, `0.24%` of the `10 MB` ceiling) confirms `0.5346 ms` SD-WAN DNS resolution, `MSS=1260` B TCP three-way synchronization (`14.21 ms` RTT), 1-RTT TLS 1.3 encrypted transfer of the `15,470 B` Seneca intranet HTML payload, and an orderly four-way `FIN` teardown (`0.4083 s` duration, `0` `RST` packets), fulfilling every technical requirement and the bonus browser-trust objective.
