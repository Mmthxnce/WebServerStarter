import http.server
import socketserver
import socket
import threading
import os
import requests

# Renk kodları
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def get_public_ip():
    """Cihazın dış IP adresini alır."""
    try:
        ip = requests.get("https://api64.ipify.org").text
    except Exception:
        ip = "Dış IP alınamadı"
    return ip

class AuthHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP sunucusu için kimlik doğrulama ekleyen sınıf."""
    def do_HEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Secure"')
        self.end_headers()
    
    def do_GET(self):
        expected_auth = "Basic " + "kalilinux:kalilinux".encode("utf-8").hex()
        if self.headers.get('Authorization') == expected_auth:
            super().do_GET()
        else:
            self.do_HEAD()

def start_server():
    """Cihazın ana dizini üzerinden web sunucusunu başlatır."""
    os.chdir(os.path.expanduser("~"))  # Ana dizine geçiş yap
    
    print(f"""{CYAN}
╔════════════════════════════════╗
║   ✵ W E B  S E R V E R  ✵      ║
║      github.com/mmthxnce       ║
╚════════════════════════════════╝
{RESET}""")

    with socketserver.TCPServer(("0.0.0.0", 8000), AuthHandler) as httpd:
        public_ip = get_public_ip()
        print(f"{GREEN}Web sunucunuz başlatıldı!{RESET}")
        print(f"{YELLOW}URL: {CYAN}http://{public_ip}:8000{RESET}\n")
        print(f"{RED}🔒 Kullanıcı adı ve şifre: {GREEN}kalilinux{RESET}\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n{RED}Sunucu kapatılıyor...{RESET}")
            httpd.server_close()

# Sunucuyu ayrı bir thread'de başlat
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Kullanıcının programı kapatmasını bekle
while True:
    key = input(f"{CYAN}Sunucuyu kapatmak için ',' tuşuna basın...{RESET}\n")
    if key == ',':
        print(f"{RED}Sunucu kapatılıyor...{RESET}")
        break
