from pathlib import Path
from colorama import init, Fore, Back, Style
import argparse
import questionary
import aiohttp
import asyncio

async def fetch(session, url):
    try:
        async with session.get(url, timeout=5) as response:
            status = response.status
            if status != 404:
                # Выбираем цвет в зависимости от статуса
                if 200 <= status < 300:
                    color = Fore.GREEN
                elif 300 <= status < 400:
                    color = Fore.YELLOW
                else:
                    color = Fore.RED
                
                print(color + f"[+] Found ({status}): {url}")
    except Exception:
        pass


async def main():
    parser = argparse.ArgumentParser(description="Web Path Enumerator")
    parser.add_argument('address', type=str, help='Target URL (e.g. http://example.com)')
    args = parser.parse_args()

    target_address = args.address if args.address.endswith('/') else args.address + '/'

    wordlist_dir = Path("WordList")
    if not wordlist_dir.exists():
        wordlist_dir.mkdir()  

    files = [f.name for f in wordlist_dir.glob("*.txt")]
    
    if not files:
        print("[-] No wordlists found in 'wordlists/' folder. Add some .txt files!")
        return

    selected_file = await questionary.select(
        "Select wordlist for scanning:",
        choices=files
    ).ask_async()

    file_path = wordlist_dir / selected_file
    lines = file_path.read_text(encoding="utf-8").splitlines()

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    init(autoreset=True)
    print(Fore.CYAN + f"[*] Starting scan for {target_address} using {selected_file}...")

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for line in lines:
            if not line.strip(): continue 
            
            url = target_address + line.lstrip('/') 
            task = asyncio.create_task(fetch(session, url))
            tasks.append(task)
        
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Stopped by user")

