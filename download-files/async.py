import requests
import bs4
import time

import asyncio
from asyncio import AbstractEventLoop
import aiohttp

async def get_html(episode_number: int) -> str:
    print(f"Getting HTML for episode {episode_number}", flush=True)
    url = f'https://talkpython.fm/{episode_number}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            res.raise_for_status()
            html = await res.text()
            return html

def get_title(html: str, episode_number: int) -> str:
    print(f"Getting TITLE for episode {episode_number}", flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    header = soup.select_one('h1')
    if not header:
        return "NOTFOUND"
    return header.text.strip()

async def get_title_range(loop: AbstractEventLoop):
    tasks = []
    for n in range(102, 120):
        tasks.append((loop.create_task(get_html(n)), n))
    for task, n in tasks:
        html = await task
        title = get_title(html, n)
        print(f"Title found: {title}", flush=True)

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_title_range(loop))
    print("Done.")

if __name__ == '__main__':
    st = time.time()
    main()
    print(f"Time taken: {time.time()-st} seconds", flush=True)