# 🔍 Network Port Scanner

A Python-based network port scanner that detects open 
ports and running services on a target machine.

## Features
- ASCII art banner
- Target reachability check
- Scans ports 1-1024
- Detects 17 common services
- OS detection (Windows/Linux/Cisco)
- Banner grabbing
- Multithreaded scanning
- Color coded output

## Requirements
- Python 3
- Colorama library

## Installation

### Windows
```bash
pip install colorama
```

### Kali Linux / Ubuntu
```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install colorama
```

## How to Run

### Windows
```bash
python port_scanner.py
```

### Kali Linux / Ubuntu
```bash
python3 port_scanner.py
```

## Usage
1. Run the script
2. Enter an IP address to scan
4. Example: scanme.nmap.org (legal test target)

## Technologies Used
- Python 3
- Socket programming
- Threading
- Colorama

## ⚠️ Disclaimer
This tool is for educational purposes only.
Only scan systems you have permission to scan.

## Author
musthafa(@MUSTHU)
