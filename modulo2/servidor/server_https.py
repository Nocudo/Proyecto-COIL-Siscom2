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

        # Host-based routing support
        if host.startswith("unillanos.") and not path.startswith("/unillanos"):
            path = "/unillanos" + path
        elif host.startswith("seneca.") and not path.startswith("/seneca"):
            path = "/seneca" + path

        # Trailing slash redirects
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

        # Determine target file
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
            # Check portal dir
            rel_path = path.lstrip("/")
            file_path = os.path.join(PORTAL_DIR, rel_path)

        # Normalize and prevent path traversal
        file_path = os.path.normpath(file_path)
        if not (file_path.lower().startswith(SITIO_DIR.lower())):
            self.send_error(403, "Access Forbidden")
            return

        if not os.path.exists(file_path) or os.path.isdir(file_path):
            self.send_error(404, f"File Not Found: {path}")
            return

        # Determine MIME type
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

class HTTPRedirectHandler(http.server.BaseHTTPRequestHandler):
    timeout = 10

    def do_GET(self):
        self.close_connection = True
        host = self.headers.get("Host", "www.coil-group2.com").split(":")[0]
        client_ip = self.client_address[0] if self.client_address else "unknown"
        try:
            if sys.stderr:
                sys.stderr.write(f"[{self.log_date_time_string()}] {client_ip} - HTTP/80 REDIRECT -> https://{host}{self.path}\n")
                sys.stderr.flush()
        except Exception:
            pass
        self.send_response(301)
        self.send_header("Location", f"https://{host}{self.path}")
        self.send_header("Connection", "close")
        self.end_headers()

    def do_HEAD(self):
        self.do_GET()

    def log_message(self, format, *args):
        pass

class NonBlockingSSLThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    request_queue_size = 32

    def __init__(self, server_address, RequestHandlerClass, ssl_context):
        super().__init__(server_address, RequestHandlerClass)
        self.ssl_context = ssl_context

    def process_request_thread(self, request, client_address):
        """Perform SSL wrapping inside the worker thread with a timeout so accept() never hangs."""
        ssl_sock = None
        try:
            request.settimeout(10.0)
            ssl_sock = self.ssl_context.wrap_socket(request, server_side=True)
            ssl_sock.settimeout(15.0)
            self.finish_request(ssl_sock, client_address)
        except ssl.SSLError as e:
            try:
                if sys.stderr:
                    sys.stderr.write(f"[SSL HANDSHAKE ERROR] from {client_address}: {e}\n")
                    sys.stderr.flush()
            except Exception:
                pass
        except (socket.timeout, ConnectionResetError, BrokenPipeError):
            pass
        except Exception as e:
            try:
                if sys.stderr:
                    sys.stderr.write(f"[THREAD ERROR] {client_address}: {e}\n")
                    sys.stderr.flush()
            except Exception:
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
        try:
            if stream is None:
                setattr(sys, stream_name, open(os.devnull, "w"))
            else:
                stream.flush()
        except Exception:
            setattr(sys, stream_name, open(os.devnull, "w"))

    print("=" * 60)
    print("COIL Group 2 - Dual Intranet HTTPS Server (Production)")
    print("=" * 60)
    print(f"Loading SSL certificate: {CERT_FILE}")
    print(f"Loading private key:    {KEY_FILE}")

    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        print("ERROR: Certificate or key file not found!")
        sys.exit(1)

    # Start Dual-Protocol Server: HTTP on Port 80 and HTTPS on Port 443
    def start_http_server():
        try:
            http_server = socketserver.ThreadingTCPServer(("0.0.0.0", 80), DualIntranetHandler)
            http_server.daemon_threads = True
            print("HTTP Server running on http://0.0.0.0:80/ (Direct Mobile & Desktop Access)", flush=True)
            http_server.serve_forever()
        except Exception as e:
            print(f"Port 80 server error: {e}", flush=True)

    t = threading.Thread(target=start_http_server, daemon=True)
    t.start()

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    try:
        ssl_context.set_alpn_protocols(["http/1.1"])
    except Exception:
        pass

    server_address = (HOST, PORT)
    httpd = NonBlockingSSLThreadingServer(server_address, DualIntranetHandler, ssl_context)

    print(f"HTTPS Server running on https://{HOST}:{PORT}/ (All interfaces: 172.22.201.2, localhost, etc.)")
    print(f" - Portal:    https://172.22.201.2/ or https://www.coil-group2.com/")
    print(f" - UniLlanos: https://172.22.201.2/unillanos/ or https://www.coil-group2.com/unillanos/")
    print(f" - Seneca:    https://172.22.201.2/seneca/ or https://www.coil-group2.com/seneca/")
    print("Press Ctrl+C to terminate.")
    print("=" * 60)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down HTTPS server.")
        httpd.server_close()

if __name__ == "__main__":
    run()
