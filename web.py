import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from bot import LootDealsBot

bot = LootDealsBot()

class DealCronHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/", "/health"]:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            resp = {
                "status": "online",
                "brand": "DealHype",
                "message": "DealHype Bot is active and healthy!"
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))

        elif self.path in ["/run-deals", "/cron"]:
            print("[CRON TRIGGERED] Executing deal check cycle from cron-job.org...")
            try:
                posted_count = bot.process_and_post_deals(dry_run=False, max_posts=3)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                resp = {
                    "status": "success",
                    "deals_posted": posted_count,
                    "channel": bot.config.TELEGRAM_CHANNEL
                }
                self.wfile.write(json.dumps(resp).encode("utf-8"))
            except Exception as e:
                print(f"[Cron Error] {e}")
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                resp = {"status": "error", "message": str(e)}
                self.wfile.write(json.dumps(resp).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Clean server log
        print(f"[HTTP Request] {self.address_string()} - {format % args}")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), DealCronHandler)
    print("="*60)
    print(f"  DEALHYPE CLOUD WEB SERVER RUNNING ON PORT {port}")
    print("="*60)
    print("Endpoints:")
    print(f"  Health Check : http://localhost:{port}/health")
    print(f"  Cron Trigger : http://localhost:{port}/run-deals")
    print("Ready for cron-job.org!\n")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
