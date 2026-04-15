# ProcLS
### The first program you should launch after finding an LFI.

## What is it?
It's a simple python that:  
- Checks that the LFI is working : it tries to get ``/etc/passwd`` and checks that it starts with ``root:x:``  
- Shows the target system version : it simply prints ``/proc/version``  
- List ``/proc/*`` processes (The most interesting part)  

---

## How to use it?
Download:```git clone https://github.com/abgache/procls.git
cd procls```  
Usage: ```procls <target> [-p PORT] [-s PATH] [--max MAX] [--param PARAM]```  

---

## License  
### ProcLS License (PL-1.0)  
#- Copyright (c) 2026 Abgache  
Permission is hereby granted to use, copy, modify, and distribute this software for personal, educational, and security research purposes, subject to the following conditions:  
1. Do not use this software for illegal activities.  
2. Do not claim it as your own work without credit.  
3. If you break it, you fix it yourself.  
**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.**  