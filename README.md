# International COIL Project: ZeroTier SD-WAN, Dual-Tenant HTTPS Intranets, Private PKI, and Deep Packet Inspection

**Course:** Communication Systems II (10th Semester, Electronic Engineering)  
**Institutions:** Universidad de los Llanos (Villavicencio, Meta, Colombia) and Seneca Polytechnic (Toronto, Ontario, Canada)  
**Group:** COIL Group 2  
**Authors (UniLlanos Engineering Team):**
- **Miguel Angel Rodriguez Payares** — ID: `161004834` (`marodriguez.payares@unillanos.edu.co`)
- **Luis Alejandro Leon Velasquez** — (`laleon.velasquez@unillanos.edu.co`)

---

## 1. Executive Summary

This repository contains the complete engineering deliverables, network services, cryptographic certificates, web portals, Wireshark packet captures, demonstration media, and IEEE LaTeX technical documentation developed across the three modules of the Collaborative Online International Learning (COIL) partnership between **Universidad de los Llanos** and **Seneca Polytechnic**.

The core technical architecture interconnects distributed endpoints across a private **ZeroTier Software-Defined Wide Area Network (SD-WAN)** (`abfd31bd47affa39`, `172.22.0.0/16`, MTU `1300 B`) and hosts a dual-tenant HTTPS cultural intranet platform (`https://www.coil-group2.com/unillanos/` and `https://www.coil-group2.com/seneca/`) secured with **TLS 1.3** (`TLS_AES_256_GCM_SHA384`), a custom **2048-bit RSA Root Certificate Authority** (`COIL Group 2 Root CA`), and an authoritative **UDP/53 DNS daemon** (`dnslib` with RFC 2308 negative caching).

---

## 2. Repository Structure

```text
COIL/
├── modulo1/                                      # Module 1: Cultural Exchange Media Assets
│   ├── 20260816_143153.jpg
│   ├── 20261106_113653.jpg
│   ├── Carne-a-la-llanera.webp
│   └── IMG_20220720_114832.jpg
│
├── modulo2/                                      # Module 2 (80%): SD-WAN, Dual HTTPS Intranets, PKI, DNS & Wireshark
│   ├── iniciar_pagina.bat                        # 1-Click Windows launcher (DNS + HTTP/HTTPS Server + Browser)
│   ├── pasos_actividad_modulo2.txt               # Official Module 2 activity rubric and specifications
│   ├── Videos.txt                                # Individual demonstration video delivery links
│   ├── certificados/                             # Two-tier X.509 Public Key Infrastructure (PKI)
│   │   ├── COIL_Group2_Root_CA.crt               # Custom Root CA certificate for client trust stores
│   │   ├── ca-cert.pem / ca-key.pem              # Root CA certificate and private key
│   │   ├── server-cert.pem / server-key.pem      # SAN-enabled TLS leaf certificate and key
│   │   ├── fullchain.pem                         # Complete certificate chain
│   │   ├── openssl.cnf                           # OpenSSL X.509v3 SAN extension configuration
│   │   └── install_root_ca.ps1                   # Automated PowerShell Root CA installer for Windows
│   ├── dns/                                      # Domain Name System (DNS) Resolution
│   │   ├── dns_server.py                         # Authoritative UDP/53 DNS server (dnslib, RFC 2308 SOA)
│   │   └── setup_hosts.ps1                       # Local fallback hosts configuration script
│   ├── servidor/                                 # Application Web Server
│   │   └── server_https.py                       # Multi-threaded Python HTTP:80 -> HTTPS:443 TLS 1.3 server
│   ├── sitio_web/                                # Dual-Tenant Cultural Intranet Web Portals
│   │   ├── portal/index.html                     # Unified gateway landing portal
│   │   ├── unillanos/                            # Universidad de los Llanos cultural intranet & assets
│   │   └── seneca/                               # Seneca Polytechnic cultural intranet & assets
│   ├── wireshark/                                # Deep Packet Inspection (DPI) Telemetry
│   │   └── coil_sdwan_https_traffic.pcapng       # Verified SD-WAN DNS + TCP + TLS 1.3 packet trace (24.8 KB)
│   ├── video/                                    # Individual English Demonstration Video Deliverables
│   │   ├── COIL_Module2_Miguel_Rodriguez_Demo.mp4 # Compiled 1080p 30fps demonstration video
│   │   └── video_script_english.md               # Standardized 4-scene English narration script
│   └── informe/                                  # IEEE Technical Engineering Report (LaTeX & Markdown)
│       ├── main.pdf                              # Compiled IEEE 2-column technical report (48 pages)
│       ├── main.tex                              # Master IEEEtran LaTeX source
│       ├── referencias.bib                       # BibTeX bibliography (RFCs, IEEE, ZeroTier)
│       ├── COIL_Module2_Technical_Report.md      # Markdown technical report reference
│       ├── figuras/                              # TikZ vector architectures & live verification screenshots
│       └── secciones/                            # Modular LaTeX sections (01 through 07)
│
└── modulo3/                                      # Module 3 (10%): Individual Reflection Deliverables
    ├── COIL_Module3_Reflection_Miguel_Rodriguez.pdf # Compiled academic reflection report (6 pages)
    ├── COIL_Module3_Reflection_Miguel_Rodriguez.md  # Markdown reflection document
    ├── COIL_Module3_CopyPaste_Ready.txt             # Plain-text deliverable for LMS submission
    ├── pasos_actividad_modulo3.txt                  # Official Module 3 rubric and guidelines
    └── informe/                                     # Modular LaTeX source & TikZ workflow figures
```

---

## 3. Technical Specifications (Module 2 Infrastructure)

| Subsystem | Parameter / Component | Configured Value |
|---|---|---|
| **SD-WAN Overlay** | ZeroTier Network ID & Subnet | `abfd31bd47affa39` (`172.22.0.0/16`, MTU `1300 B`, TCP MSS `1260 B`) |
| **Primary Server Node** | Miguel Rodriguez (Web + DNS Host) | `172.22.201.2` (ZeroTier Node `AED30A4FDD`) |
| **Partner Gateway Node** | Seneca Polytechnic Gateway | `172.22.31.69` (ZeroTier Node `38DF833716`) |
| **Client Nodes** | Luis Alejandro Leon & Mobile Endpoints | `172.22.100.10`, `172.22.100.11`, `172.22.201.3` |
| **Domain Name (FQDN)** | Authoritative Intranet Domain | `www.coil-group2.com` (`coil-group2.com`) |
| **DNS Daemon** | Engine & Protocol Compliance | Python `dnslib` on `0.0.0.0:53` (UDP), RFC 2308 `NODATA+SOA`, upstream `8.8.8.8` |
| **Web Server Daemon** | Engine & Transport Security | `COIL-DualIntranet/2.0` (`ThreadingHTTPServer`), HTTP/80 (`301`) to HTTPS/443 (TLS 1.3) |
| **Public Key Infrastructure** | Root CA & Leaf Certificate | `COIL Group 2 Root CA` (RSA-2048, SHA-256) + X.509v3 SAN Leaf Certificate |
| **Wireshark Capture** | Trace File & Size Compliance | `modulo2/wireshark/coil_sdwan_https_traffic.pcapng` (`24.81 KB`, limit `< 10 MB`) |

---

## 4. Quick Start & Operational Deployment

### 4.1 One-Click Windows Startup
Run `modulo2\iniciar_pagina.bat` from Windows Explorer or an administrative PowerShell prompt. The launcher automatically:
1. Starts the authoritative DNS server (`modulo2/dns/dns_server.py`) on UDP port `53` if not already running.
2. Starts the dual-stack HTTP/HTTPS server (`modulo2/servidor/server_https.py`) on TCP ports `80` and `443`.
3. Verifies local hostname resolution for `www.coil-group2.com`.
4. Opens `https://www.coil-group2.com/` in the system browser.

### 4.2 Root CA Trust Installation (Bonus Zero-Warning HTTPS)
To eliminate browser self-signed certificate warnings on client endpoints:
- **Windows:** Execute `powershell -ExecutionPolicy Bypass -File modulo2\certificados\install_root_ca.ps1` as Administrator (imports `COIL_Group2_Root_CA.crt` into `Cert:\LocalMachine\Root`).
- **Android:** Install `modulo2/certificados/COIL_Group2_Root_CA.crt` under *Settings -> Security and privacy -> More security settings -> Install from device storage -> CA certificate*.

---

## 5. Individual Demonstration Video

- **Presenter:** Miguel Angel Rodriguez Payares (ID: `161004834`)
- **Target Intranet Demonstrated:** Seneca Polytechnic Intranet (`https://www.coil-group2.com/seneca/`)
- **YouTube Unlisted URL:** https://youtu.be/jrUnb2pqvwg
- **Local Video File:** `modulo2/video/COIL_Module2_Miguel_Rodriguez_Demo.mp4`
