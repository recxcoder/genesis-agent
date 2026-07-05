import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def browse_web(url: str) -> str:
    print(f"\n🌐 Browsing: {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout = 10)

        if response.status_code != 200:
            return f"Failed to fetch page. Status code: {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()

        text = soup.get_text(separator="\n")

        lines = [line.strip() for line in text.splitlines() if line.strip()]

        return "\n".join(lines[:100])

    except requests.exceptions.Timeout:
        return f"Timed out trying to reach {url}"

    except requests.exceptions.ConnectionError:
        return f"Could not connect to {url}"

    except Exception as e:
        return f"Something went wrong: {str(e)}"