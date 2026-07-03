from ddgs import DDGS

def search_web(query: str, max_results: int = 4) -> str:
    print(f"\n🔍 Searching: {query}")

    with DDGS() as ddgs:
        result = list(ddgs.text(query, max_results=max_results))

    if not result:
        return "No results found."

    formatted = ""
    for i, r in enumerate(result, 1):
        formatted += f"\nResult {i}:\nTitle: {r['title']}\nURL: {r['href']}\nSummary: {r['body']}\n"

    return formatted