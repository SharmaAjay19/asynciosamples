import requests
import bs4
import time

import asyncio
from asyncio import AbstractEventLoop
import aiohttp
import aiofiles

async def get_html(episode_number: int) -> str:
    print(f"Getting HTML for episode {episode_number}", flush=True)
    url = f'https://talkpython.fm/{episode_number}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            res.raise_for_status()
            html = await res.text()
            return html

async def download_file(episode_number: str, aud_link: str):
    print(f"Downloading audio for episode {episode_number}", flush=True)
    f_name = f"{episode_number}-{aud_link.split('/')[-1]}"
    url = f'https://talkpython.fm{aud_link}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            res.raise_for_status()
            f = await aiofiles.open(f_name, 'wb')
            await f.write(await res.read())
            await f.close()
    print(f"Downloaded file {f_name}", flush=True)

def get_audiolink(html: str, episode_number: int) -> str:
    print(f"Getting audio link for episode {episode_number}", flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    audio = soup.select_one('source')
    if not audio:
        return "NOTFOUND"
    return audio['src']

async def get_audio_file_range(loop: AbstractEventLoop):
    tasks = []
    dtasks = []
    for n in range(102, 120):
        tasks.append((loop.create_task(get_html(n)), n))
    for task, n in tasks:
        html = await task
        audlink = get_audiolink(html, n)
        dtasks.append(loop.create_task(download_file(n, audlink)))
    for task in dtasks:
        await task

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_audio_file_range(loop))
    print("Done.")

if __name__ == '__main__':
    st = time.time()
    main()
    print(f"Time taken: {time.time()-st} seconds", flush=True)