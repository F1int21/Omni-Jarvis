# test.py
from core.agent import ask_agent

query = "найди все файлы с отчётом"
print(f"Запрос: {query}\n")
result = ask_agent(query)
print("\n=== РЕЗУЛЬТАТ ===")
print(result)