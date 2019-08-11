import requests
import bs4
import time

def get_html(episode_number: int) -> str:
    print(f"Getting HTML for episode {episode_number}", flush=True)
    url = f'https://talkpython.fm/{episode_number}'
    res = requests.get(url)
    res.raise_for_status()
    return res.text

def get_title(html: str, episode_number: int) -> str:
    print(f"Getting TITLE for episode {episode_number}", flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    header = soup.select_one('h1')
    if not header:
        return "NOTFOUND"
    return header.text.strip()

def get_title_range():
    for n in range(102, 120):
        html = get_html(n)
        title = get_title(html, n)
        print(f"Title found: {title}", flush=True)

def main():
    get_title_range()
    print("Done.")

if __name__ == '__main__':
    st = time.time()
    main()
    print(f"Time taken: {time.time()-st} seconds", flush=True)