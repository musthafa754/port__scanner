import socket
import threading
from colorama import Fore, Style, init
from datetime import datetime

init()

# ---- BANNER ----
print(f"""
{Fore.CYAN}
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  ██████╗  ██████╗ ██████╗ ████████╗                             ║
║  ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝                             ║
║  ██████╔╝██║   ██║██████╔╝   ██║                                ║
║  ██╔═══╝ ██║   ██║██╔══██╗   ██║                                ║
║  ██║     ╚██████╔╝██║  ██║   ██║                                ║
║  ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝                                ║
║                                                                  ║
║  ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗   ║
║  ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗  ║
║  ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝  ║
║  ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗  ║
║  ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║  ║
║  ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  ║
║                                             @MUSTHU              ║
╚══════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")

# ---- TARGET ----
target = input(f"{Fore.YELLOW}Enter IP address to scan (try 127.0.0.1 for your own PC): {Style.RESET_ALL}")

# ---- CHECK IF TARGET IS REACHABLE ----
try:
    socket.gethostbyname(target)
    print(f"{Fore.GREEN}[+] Target is reachable ✅{Style.RESET_ALL}")
except:
    print(f"{Fore.RED}[!] Target is not reachable! Please check the IP and try again ❌{Style.RESET_ALL}")
    exit()

print(f"\n{Fore.YELLOW}Starting scan on: {target}{Style.RESET_ALL}")
print(f"Time: {datetime.now()}\n")

# ---- COMMON SERVICES ----
def get_service(port):
    services = {
        21: "FTP", 22: "SSH", 23: "Telnet",
        25: "SMTP", 53: "DNS", 80: "HTTP",
        110: "POP3", 135: "RPC", 139: "NetBIOS",
        143: "IMAP", 443: "HTTPS", 445: "SMB",
        3306: "MySQL", 3389: "RDP", 5900: "VNC",
        8080: "HTTP-Alt", 8443: "HTTPS-Alt"
    }
    return services.get(port, "Unknown")

# ---- PORT SCANNER ----
open_ports = []
lock = threading.Lock()

def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            service = get_service(port)
            with lock:
                print(f"{Fore.GREEN}  [+] Port {port} is OPEN 🟢 ({service}){Style.RESET_ALL}")
                open_ports.append(port)
        sock.close()
    except:
        pass

# ---- OS DETECTION ----
def detect_os(target):
    print(f"\n{Fore.CYAN}[*] Detecting Operating System...{Style.RESET_ALL}")
    try:
        import subprocess
        result = subprocess.run(
            ["ping", "-n", "1", target],
            capture_output=True, text=True
        )
        output = result.stdout

        if "TTL=64" in output or "ttl=64" in output:
            print(f"{Fore.GREEN}  [+] OS Detected: Linux/Unix 🐧{Style.RESET_ALL}")
        elif "TTL=128" in output or "ttl=128" in output:
            print(f"{Fore.GREEN}  [+] OS Detected: Windows 🪟{Style.RESET_ALL}")
        elif "TTL=254" in output or "ttl=254" in output:
            print(f"{Fore.GREEN}  [+] OS Detected: Cisco/Network Device 🌐{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}  [!] OS Could not be detected 🟡{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error detecting OS: {e}{Style.RESET_ALL}")

# ---- BANNER GRABBING ----
def grab_banner(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((target, port))
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        if banner:
            print(f"{Fore.YELLOW}  [*] Banner on port {port}: {banner[:50]}{Style.RESET_ALL}")
        sock.close()
    except:
        pass

# ---- RUN SCANNER ----
print(f"{Fore.CYAN}[*] Scanning ports 1-1024...{Style.RESET_ALL}\n")

threads = []
for port in range(1, 1025):
    t = threading.Thread(target=scan_port, args=(port,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# ---- SUMMARY ----
print(f"\n{Fore.CYAN}[*] Scan Summary:{Style.RESET_ALL}")
print(f"{Fore.GREEN}  [+] Total open ports found: {len(open_ports)} ✅{Style.RESET_ALL}")

# ---- BANNER GRABBING ----
if open_ports:
    print(f"\n{Fore.CYAN}[*] Grabbing Banners from open ports...{Style.RESET_ALL}")
    for port in open_ports:
        grab_banner(port)

# ---- OS DETECTION ----
detect_os(target)

print(f"\n{Fore.GREEN}Scan Complete! ✅{Style.RESET_ALL}")