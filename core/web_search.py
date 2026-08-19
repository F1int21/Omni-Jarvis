# core/web_search.py
from ddgs import DDGS

def search_web(query: str, max_results: int = 3) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            if not results:
                return "Ничего не найдено."
            summary = []
            for r in results:
                summary.append(f"- {r['title']}: {r['body'][:200]}...")
            return "\n".join(summary)
    except Exception as e:
        return f"Ошибка поиска: {e}"