import http.server
from prometheus_client import start_http_server
from prometheus_client import Counter

REQUESTS = Counter('server_requests_total', 'Total number of requests to this webserver')

class ServerHandler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    REQUESTS.inc()
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"Hello World!")

if __name__ == "__main__":
   start_http_server(3100)
   server = http.server.HTTPServer(('', 8001), ServerHandler)
   print("Prometheus metrics available on port 3100 /metrics")
   print("HTTP server available on port 8001")
   server.serve_forever()
