#!/usr/bin/env python3
import http.server
import os
import sys
import urllib.parse
import socket

# Default values (can be overridden by CLI args)
DEFAULT_PORT = 8080
DEFAULT_FILE = "/Users/venkataganeshpatakamuri/Downloads/074290028ecb9421055e6f36ea93b13baa338277-download_files (2).zip"

def human_size(num):
    for unit in ("B","KB","MB","GB","TB"):
        if num < 1024:
            return f"{num:.1f}{unit}"
        num /= 1024
    return f"{num:.1f}PB"

class SingleFileHandler(http.server.BaseHTTPRequestHandler):
    # Set at runtime
    file_path = None
    file_name = None
    file_size = None
    file_quoted = None

    def log_message(self, fmt, *args):
        # Cleaner logging
        sys.stderr.write("[%s] %s\n" % (self.client_address[0], fmt % args))

    def do_GET(self):
        # Normalize path (ignore query string)
        path = self.path.split("?", 1)[0]

        # Allow: /  /<name>  /<urlencoded-name>
        if path in ("/", f"/{self.file_name}", f"/{self.file_quoted}"):
            if not os.path.exists(self.file_path):
                self.send_error(500, "File not found on server")
                return
            try:
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                # Provide both standard and RFC 5987 filename forms
                ascii_name = self.file_name
                quoted_rfc5987 = urllib.parse.quote(self.file_name)
                self.send_header(
                    "Content-Disposition",
                    f'attachment; filename="{ascii_name}"; filename*=UTF-8\'\'{quoted_rfc5987}'
                )
                self.send_header("Content-Length", str(self.file_size))
                self.end_headers()

                with open(self.file_path, "rb") as f:
                    # Stream in 1 MiB chunks
                    while True:
                        chunk = f.read(1024 * 1024)
                        if not chunk:
                            break
                        self.wfile.write(chunk)
            except BrokenPipeError:
                # Client disconnected mid-transfer
                pass
            return

        self.send_error(404, "Not Found")

def run(port, file_path, host="0.0.0.0"):
    if not os.path.isfile(file_path):
        print(f"ERROR: File does not exist: {file_path}", file=sys.stderr)
        sys.exit(1)

    handler_cls = SingleFileHandler
    handler_cls.file_path = file_path
    handler_cls.file_name = os.path.basename(file_path)
    handler_cls.file_size = os.path.getsize(file_path)
    handler_cls.file_quoted = urllib.parse.quote(handler_cls.file_name)

    # Allow quick reuse after restart
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    server = http.server.ThreadingHTTPServer((host, port), handler_cls)

    # Determine a representative local address (for printing)
    try:
        # Connect to a public resolver to discover outbound interface
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"

    print("")
    print("Single File Download Server")
    print("---------------------------")
    print(f"File        : {handler_cls.file_name}")
    print(f"Size        : {human_size(handler_cls.file_size)} ({handler_cls.file_size} bytes)")
    print(f"Listening   : {host}:{server.server_address[1]}")
    print(f"Local URL   : http://localhost:{server.server_address[1]}/{handler_cls.file_quoted}")
    print(f"LAN URL     : http://{local_ip}:{server.server_address[1]}/{handler_cls.file_quoted}")
    print("")
    print("Start ngrok (example):")
    print(f"  ngrok http {server.server_address[1]}")
    print("")
    print("Press Ctrl+C to stop.")
    print("")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        server.server_close()

if __name__ == "__main__":
    # Usage:
    #   python single_file_server.py
    #   python single_file_server.py 8090 /path/to/file.zip
    #   python single_file_server.py /path/to/file.zip
    args = sys.argv[1:]

    port = DEFAULT_PORT
    file_path = DEFAULT_FILE

    if len(args) == 1:
        if args[0].isdigit():
            port = int(args[0])
        else:
            file_path = args[0]
    elif len(args) >= 2:
        # First arg port, second file path
        port = int(args[0]) if args[0].isdigit() else DEFAULT_PORT
        file_path = args[1]

    run(port, file_path)