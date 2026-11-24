import os
import sys
import socket
import shutil
from http.server import HTTPServer, SimpleHTTPRequestHandler

class RangeRequestHandler(SimpleHTTPRequestHandler):
    """HTTP Request Handler with full Range request support (essential for iOS/Android video seeking)."""
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, must-revalidate')
        super().end_headers()

    def send_head(self):
        path = self.translate_path(self.path)
        if not os.path.exists(path) or os.path.isdir(path):
            self.range = None
            return super().send_head()

        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404, "File not found")
            return None

        fs = os.fstat(f.fileno())
        size = fs[6]

        range_header = self.headers.get('Range')
        if not range_header or not range_header.startswith('bytes='):
            self.range = None
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(size))
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()
            return f

        try:
            ranges = range_header.split('=')[1].split('-')
            start = int(ranges[0]) if ranges[0] else 0
            end = int(ranges[1]) if ranges[1] else size - 1
            if start >= size or end >= size or start > end:
                self.send_error(416, "Requested Range Not Satisfiable")
                f.close()
                return None
        except ValueError:
            self.send_error(400, "Bad Request")
            f.close()
            return None

        length = end - start + 1
        self.range = (start, length)

        self.send_response(206)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(length))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()

        f.seek(start)
        return f

    def copyfile(self, source, outputfile):
        if hasattr(self, 'range') and self.range:
            start, length = self.range
            remaining = length
            buf_size = 64 * 1024
            while remaining > 0:
                chunk = source.read(min(remaining, buf_size))
                if not chunk:
                    break
                try:
                    outputfile.write(chunk)
                except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                    break
                remaining -= len(chunk)
        else:
            try:
                shutil.copyfileobj(source, outputfile)
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                pass

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == '__main__':
    port = 8080
    host = '0.0.0.0'
    local_ip = get_local_ip()

    print("=" * 60)
    print("   AgniNode Local Wi-Fi & Offline Media Server")
    print("=" * 60)
    print(f" Local URL (This PC) : http://localhost:{port}/")
    print(f" Mobile / Wi-Fi URL  : http://{local_ip}:{port}/")
    print("=" * 60)
    print(" Any phone on the same Wi-Fi can scan assets/qr/AgniNode_QR_Local_WiFi.png")
    print(" Press Ctrl+C to stop.")
    print("=" * 60)

    server = HTTPServer((host, port), RangeRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)
