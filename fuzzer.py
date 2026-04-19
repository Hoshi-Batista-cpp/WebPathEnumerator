from pathlib import Path
import aiohttp
import asyncio

async def fetch(session, url):
    try:
        async with session.get(url, timeout=5) as response:
            if response.status != 404: 

                print(f"[+] found ({response.status}): {url}")
    
    except Exception:
        pass

async def main():
    address = "http://github.com/" 
    file_path = Path("wordlist.txt")

    if not file_path.exists():
        print("File not found")
        return

    lines = file_path.read_text(encoding="utf-8").splitlines()

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for line in lines:

            url = address + line.strip()
            task = asyncio.create_task(fetch(session, url))
            tasks.append(task)

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

