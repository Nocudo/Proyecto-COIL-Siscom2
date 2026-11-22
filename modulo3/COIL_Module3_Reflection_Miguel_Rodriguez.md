# COIL International Exchange - Module 3 Individual Reflection (10%)
## Lessons Learned from COIL: Critical Incident Analysis and Academic Growth

- **Student:** Miguel Ángel Rodríguez Payares
- **Student ID:** 161004834
- **Program:** Electronic Engineering (10th Semester)
- **Home Institution:** Universidad de los Llanos (Villavicencio, Colombia)
- **Partner Institution:** Seneca Polytechnic (Toronto, Canada)
- **Course:** Sistemas de Comunicación 2
- **Team:** Group 2
- **Submission Window:** November 16 - November 22, 2026
- **Language:** English

---

## Evaluation Structure Summary

| Module Component | Included Deliverable | Weight |
|---|---|---|
| **Part 1: Critical Incident Analysis** | Option A (300-word written summary) + Option B (1-minute video script, 146 spoken words) | 5% |
| **Part 2: Academic Growth and Development** | Detailed analytical responses to Question 1 (2.5%) and Question 2 (2.5%) | 5% |
| **Total Module 3** | **Individual Final Reflection** | **10%** |

---

## 1. Part 1: Critical Incident Analysis (5%)

Both Option A (written summary) and Option B (1-minute video script) are provided below using the exact same verified Group 2 experience so you can submit either format directly.

### 1.1 Option A: Written Critical Incident Summary (300 Words)

During our COIL Group 2 collaboration between Universidad de los Llanos in Colombia and Seneca Polytechnic in Canada, the primary critical incident emerged at the very outset of the project. Although the technical assignment required an interconnected Software-Defined Wide Area Network linking servers and student clients across both institutions, we experienced a complete absence of contact from our assigned Seneca Polytechnic counterparts from the beginning of the exchange. Neither initial outreach messages nor coordination attempts through the shared course channels produced a reply, leaving our bilateral team without active Canadian participation.

This communication breakdown created a severe operational obstacle. According to the Module 2 guidelines, Seneca students were responsible for configuring the authoritative DNS server inside the overlay network and deploying their institutional cultural intranet, while both universities were expected to negotiate and sign a Group Contract. Without partner engagement, our UniLlanos sub-team faced the risk of being unable to validate cross-institutional domain resolution, end-to-end TLS encryption, or live Wireshark traffic capture.

To prevent project failure, my UniLlanos teammate, Luis Alejandro León Velásquez, and I documented the lack of response and established an internal contingency plan. I assumed end-to-end architecture for the ZeroTier SD-WAN overlay, the RFC-compliant authoritative DNS service, our private Root Certificate Authority, the dual-protocol HTTPS server, and a secondary gateway node simulating the Seneca endpoint. I also researched Canadian landmarks, traditions, and gastronomy to build the Seneca cultural intranet respectfully, while Alejandro administered the ZeroTier Central network and verified domain navigation from an external physical client node across the Americas.

This experience taught me that international engineering projects often fail not over code or protocols, but due to early coordination gaps and academic calendar mismatches. Proactive contingency planning, clear documentation, and willingness to absorb critical dependencies transformed an initial deadlock into a fully verified, cross-cultural technical delivery.

*(Verified length: 300 words across four cohesive paragraphs covering context, impact, technical resolution, and intercultural reflection.)*

---

### 1.2 Option B: One-Minute Video Presentation Script (146 Spoken Words)

#### Delivery Timing Cue Sheet

| Time Window | Rubric Beat | Visual / Screen Cue |
|---|---|---|
| **0:00 - 0:14** | Context | Title slide or webcam introduction showing COIL Group 2 header and UniLlanos affiliation. |
| **0:14 - 0:28** | Challenge & Impact | Brief view of Module 2 topology highlighting Seneca's planned DNS and intranet dependencies. |
| **0:28 - 0:47** | Technical Resolution | Show ZeroTier Central (`abfd31bd47affa39`), dual HTTPS portal, and `https://www.coil-group2.com/seneca/`. |
| **0:47 - 1:00** | Lesson Learned | Closing slide or direct camera view summarizing proactive ownership and cross-cultural learning. |

#### Continuous Oral Monologue (Approx. 60 Seconds at Natural Pace)

> "Hello everyone, my name is Miguel Ángel Rodríguez Payares, a tenth-semester Electronic Engineering student at Universidad de los Llanos. During our Group 2 COIL exchange with Seneca Polytechnic, we faced a critical incident right from the start: complete silence from our assigned Canadian partners.
>
> Because Seneca was originally expected to host the DNS service and their cultural intranet, and both sides needed to sign a Group Contract, this lack of communication threatened our ability to demonstrate domain-based HTTPS connectivity.
>
> Instead of stalling, my teammate Luis Alejandro León and I agreed on a contingency plan. I deployed the ZeroTier SD-WAN, the authoritative DNS server, a custom Root CA, both cultural intranets, and a simulated Seneca gateway, while Alejandro managed ZeroTier Central and external client verification.
>
> This taught me that resilient engineering depends on early verification, clear documentation, and proactive ownership whenever international coordination breaks down. Thank you."

---

## 2. Part 2: Academic Growth and Development (5%)

### 2.1 Question 1: Project Responsibilities and New Technical Skills (2.5%)

> **Prompt:** *"Through the course of the COIL project and your participation in it, explain which part(s) of the project you were responsible for, and what new technical skills you have developed while completing your portion of the project."*

Because our assigned Seneca Polytechnic counterparts never established contact, the technical workload of COIL Group 2 had to be absorbed entirely by our two-person team at Universidad de los Llanos. Within our internal division of responsibilities, my partner Luis Alejandro León Velásquez owned ZeroTier Central network administration and external physical client testing (`f6fcd4ce4d` at `172.22.100.10/16`), while I assumed architectural and implementation ownership for the core networking, cryptographic, web application, packet-inspection, and documentation layers of the project.

Specifically, I was responsible for five integrated subsystems. First, I designed and operated the host overlay topology on ZeroTier Network ID `abfd31bd47affa39` (`172.22.0.0/16`), deploying both the primary server node (`aed30a4fdd`, `172.22.201.2/16`) and a secondary node (`1c84e39095`, `172.22.31.69/16`) that simulated the missing Seneca gateway so cross-node verification remained authentic. Second, I programmed the multi-threaded dual-protocol web server (`server_https.py`) listening on ports 80 and 443, and developed the responsive HTML5/CSS3 gateway portal alongside both the UniLlanos and Seneca cultural intranets. Third, to fulfill the strict HTTPS requirement and achieve the bonus trust criteria, I designed an internal Public Key Infrastructure (`openssl.cnf`), generated a 2048-bit RSA Root Certificate Authority (`COIL Group 2 Root CA`), and issued Subject Alternative Name (SAN) leaf certificates covering every domain and virtual IP. Fourth, I absorbed Seneca's originally assigned DNS scope by building an RFC-compliant authoritative and forwarding DNS server (`dns_server.py`) using `dnslib` on UDP port 53, complemented by automated PowerShell host-setup and batch launch scripts. Fifth, I captured live SD-WAN traffic in Wireshark (`coil_sdwan_https_traffic.pcapng`, 19.3 KB) and authored the formal Module 2 English technical report, four step-by-step manuals, and demonstration scripts.

Completing these subsystems forced me to move beyond textbook theory and develop several practical systems-engineering skills through real troubleshooting:

- **RFC-Compliant DNS Engineering and Mobile Diagnostics:** While testing smartphone access over ZeroTier (`172.22.201.50`), Android's `netd` resolver failed with `FORMERR` because initial responses lacked authoritative `SOA` records on `NODATA` replies for IPv6 (`AAAA`) and `HTTPS` (Type 65) queries. I also diagnosed a ZeroTier Search Domain suffix loop (`www.coil-group2.com.coil-group2.com`) triggering `DNS_PROBE_STARTED`, and cleared a Windows `SharedAccess` (ICS) UDP 53 port conflict.
- **Concurrent TLS Socket Handling:** Standard synchronous SSL wrapping blocks the server accept loop when clients probe and stall, and calling `shutdown(SHUT_WR)` on wrapped Windows TLS sockets can emit TCP `RST` frames that trigger `ERR_CONNECTION_CLOSED`. Implementing `NonBlockingSSLThreadingServer` with worker-thread handshakes and bounded timeouts taught me production-safe TLS concurrency.
- **Custom X.509 v3 PKI and OS Trust Stores:** Configuring `basicConstraints`, `authorityKeyIdentifier`, and SAN entries in OpenSSL, then automating Root CA installation into Windows (`Cert:\LocalMachine\Root`) and Android, gave me hands-on mastery of browser trust chains.
- **Overlay MTU Tuning and Deep Packet Inspection:** Tuning ZeroTier's virtual interface MTU to 1300 bytes prevented cellular fragmentation, adjusting Windows firewall interface profiles from `Public` to `Private` unblocked inbound routing, and applying Wireshark display filters (`ip.addr == 172.22.31.69 and tcp.port == 443`) sharpened my ability to audit TCP 3-way handshakes, TLS 1.3 1-RTT exchanges (`X25519`, `TLS_AES_256_GCM_SHA384`), and orderly `FIN/ACK` teardowns.

| Subsystem | Concrete Deliverables | New Technical Skills Developed |
|---|---|---|
| **SD-WAN Overlay & Firewalling** | ZeroTier `abfd31bd47affa39` host (`172.22.201.2`) and simulated gateway (`172.22.31.69`) | Virtual interface MTU tuning (1300 bytes), Windows `Private` profile routing, and cross-node ICMP diagnostics. |
| **Authoritative DNS Service** | `dns_server.py` (`dnslib`), `setup_hosts.ps1`, and `iniciar_pagina.bat` | RFC 1035/2308 `SOA` `NODATA` handling for `AAAA`/Type 65, upstream forwarding, and UDP 53 port conflict recovery. |
| **Custom PKI & TLS 1.3** | `openssl.cnf`, `COIL_Group2_Root_CA.crt`, SAN cert, and `install_root_ca.ps1` | X.509 v3 Root CA chaining, multi-SAN signing, and Windows/Android trust-store deployment (bonus compliance). |
| **Multi-Tenant Web Server** | `server_https.py`, gateway portal, `/unillanos/`, and `/seneca/` frontends | Thread-safe non-blocking TLS wrapping, dual HTTP/HTTPS sockets, host/path routing, and responsive HTML5/CSS3 design. |
| **Traffic Audit & Documentation** | `coil_sdwan_https_traffic.pcapng`, 4 Wireshark screenshots, report, and scripts | Boolean packet filtering, TLS 1.3 cipher/SNI dissection, TCP state-machine verification, and formal English technical writing. |

---

### 2.2 Question 2: Group Contract Comparison and Reflection (2.5%)

> **Prompt:** *"Compare what you have completed in the project to the original Group Contract that was signed. Was the group contract followed? Please elaborate and reflect on why the contract was or wasn't followed."*

To answer honestly and directly: **no, the original bilateral Group Contract was not followed, because it was never formally signed or put into effect with our Seneca Polytechnic counterparts.** From the initial launch of the COIL exchange, our assigned Canadian teammates never responded to outreach messages or joined any planning touchpoints. Consequently, a shared cross-institutional agreement governing meeting schedules, communication response windows, and joint deliverables could not be negotiated or signed.

Faced with complete silence from the partner side, Luis Alejandro León Velásquez and I faced a clear risk of leaving critical dependencies - specifically the authoritative DNS server and Seneca's cultural intranet - unbuilt. Rather than allowing an unexecuted contract to block our progress on Module 2 (which carries 80% of the project grade), we established an informal internal working agreement within Universidad de los Llanos. Under this contingency pact, we preserved 100% of the technical objectives defined in the course guide by reallocating Seneca's unfulfilled responsibilities to ourselves and documenting every step transparently.

| Project Element | Planned Bilateral Contract | Actual Execution (UniLlanos) | Outcome |
|---|---|---|---|
| **Signed Group Contract** | Jointly negotiated rules, roles, and meeting cadence across both schools | Never signed due to zero Seneca contact; replaced by internal UniLlanos pact | Not Followed (Contingency Used) |
| **ZeroTier SD-WAN Mesh** | At least one PC per student across Seneca and UniLlanos | Miguel host (`172.22.201.2`), Alejandro client (`172.22.100.10`), simulated gateway (`172.22.31.69`), mobile | Completed Internally |
| **Authoritative DNS Server** | Configured and operated by Seneca students | Designed and deployed in Python (`dnslib`) by Miguel on UDP 53 | Reallocated & Completed |
| **Cultural Intranet Sites** | UniLlanos builds Colombian site; Seneca builds Canadian site | UniLlanos built both `/unillanos/` and `/seneca/` portals with authentic research | Reallocated & Completed |
| **HTTPS, PKI & Bonus Trust** | Self-signed TLS required; trusted Root CA optional bonus | Full OpenSSL Root CA + SAN certs installed in OS trust stores (zero warnings) | Completed + Bonus Met |
| **Wireshark, Report & Videos** | Joint English technical report and individual member videos | Full 19.3 KB PCAP, 4 packet figures, 4 manuals, and UniLlanos individual demos | Completed by UniLlanos |

Reflecting critically on *why* the Group Contract was never signed or followed reveals three structural root causes common to international virtual exchanges:

1. **Absence of a Verified Week 1 Synchronous Kickoff:** Without a mandatory live video orientation where both sides confirm active course enrollment, verify email or messaging handles, and co-sign the contract in real time, asynchronous outreach fails silently. Once initial momentum is lost during the first week, re-engaging unresponsive remote members becomes exceedingly difficult.
2. **Institutional and Academic Calendar Asymmetry:** Partner cohorts across Colombia and Canada operate under different semester timelines, add/drop windows, workload peaks, and grading weights. If students from one institution drop the course, change sections, or deprioritize an unaligned assignment before team formation stabilizes, the bilateral contract collapses before technical work even begins.
3. **Lack of an Automated Early-Escalation Clause:** The standard COIL workflow assumed bilateral participation would materialize organically, without specifying a strict 72-hour response Service Level Agreement (SLA) or an automatic instructor-mediated reassignment mechanism when a partner team goes silent.

Ultimately, while the formal cross-institutional Group Contract could not be followed, the discipline of honoring its underlying technical and ethical standards led us to a stronger outcome. Within UniLlanos, Alejandro and I maintained clear accountability, met our technical milestones ahead of deadlines, and never lowered the engineering bar just because a partner was absent. In future international collaborations, I will insist on three safeguards from day one: a synchronous verification call in Week 1, explicit response-time SLAs with an instructor escalation trigger, and decoupled system interfaces so that a sub-team can always test and deliver reliably even when external dependencies fail.
