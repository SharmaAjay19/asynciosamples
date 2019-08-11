import requests
import bs4
import time

def get_html(episode_number: int) -> str:
    print(f"Getting HTML for episode {episode_number}", flush=True)
    url = f'https://talkpython.fm/{episode_number}'
    res = requests.get(url)
    res.raise_for_status()
    return res.text

def download_file(episode_number: str, aud_link: str):
    print(f"Downloading audio for episode {episode_number}", flush=True)
    f_name = f"{episode_number}-{aud_link.split('/')[-1]}"
    url = f'https://talkpython.fm{aud_link}'
    res = requests.get(url)
    res.raise_for_status()
    with open(f_name, 'wb') as f:
        for chunk in res.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Downloaded file {f_name}", flush=True)

def get_audiolink(html: str, episode_number: int) -> str:
    print(f"Getting audio link for episode {episode_number}", flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    audio = soup.select_one('source')
    if not audio:
        return "NOTFOUND"
    return audio['src']

def get_audio_file_range():
    for n in range(102, 120):
        html = get_html(n)
        audlink = get_audiolink(html, n)
        download_file(n, audlink)

def main():
    get_audio_file_range()
    print("Done.")

if __name__ == '__main__':
    st = time.time()
    main()
    print(f"Time taken: {time.time()-st} seconds", flush=True)