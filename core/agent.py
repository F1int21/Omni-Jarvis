# core/agent.py
import json
import re
import requests
from core.web_search import search_web
from core.step_executor import execute_step
from core.intent import detect_intent
from core.planner import create_plan

def ask_agent(query: str, model: str = "deepseek-r1:1.5b") -> str:
    # Поиск в интернете
    print("🔍 Ищу информацию в интернете...")
    search_results = search_web(query, max_results=3)
    print("✅ Поиск завершён.")

    # Попытка через LLM (с таймаутом 10 сек, чтобы не ждать)
    plan = None
    try:
        prompt = f"Задача: \"{query}\"\nИнтернет: {search_results}\nВерни JSON-массив действий. Действия: download, run_command, install_exe, search_files, move_file, ask_user.\nПример: [{{\"action\":\"search_files\",\"params\":{{\"pattern\":\"отчёт\",\"roots\":[\"C:\\\\Users\\\\Work\\\\Desktop\"]}}}}]\nОтветь ТОЛЬКО JSON."
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False, "format": "json"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            plan_text = data.get("response", "[]")
            clean_text = re.sub(r'```json\s*|\s*```', '', plan_text).strip()
            if clean_text.startswith('['):
                plan = json.loads(clean_text)
            else:
                match = re.search(r'\[\s*\{.*\}\s*\]', clean_text, re.DOTALL)
                if match:
                    plan = json.loads(match.group(0))
    except Exception as e:
        print(f"⚠️ LLM не ответил: {e}")

    # Если LLM не дал план — используем словарь
    if not plan or not isinstance(plan, list) or len(plan) == 0:
        print("🔄 Использую словарный детектор...")
        intent_data = detect_intent(query)
        plan = create_plan(intent_data["intent"], intent_data["params"])

    # Если план всё ещё ask_user — просто возвращаем сообщение (без рекурсии)
    if plan and len(plan) == 1 and plan[0].get("action") == "ask_user":
        return f"❌ {plan[0].get('params', {}).get('question', 'Задача не распознана')}"

    # Показываем план и подтверждение
    print("\n=== 📋 ПЛАН ДЕЙСТВИЙ ===")
    for i, step in enumerate(plan, 1):
        action = step.get("action")
        params = step.get("params", {})
        print(f"{i}. {action}: {params}")

    print("\nВыполнить план? (да/нет): ", end="")
    confirm = input().strip().lower()
    if confirm != "да":
        return "❌ План отменён пользователем."

    # Выполнение
    print("\n🚀 Выполняю план...")
    results = []
    for i, step in enumerate(plan, 1):
        print(f"\n▶️ Шаг {i}: {step.get('action')}...")
        try:
            result = execute_step(step)
            results.append(f"Шаг {i}: {result}")
        except Exception as e:
            results.append(f"Шаг {i} ❌ Ошибка: {e}")
            print("Продолжить выполнение? (да/нет): ", end="")
            if input().strip().lower() != "да":
                results.append("Выполнение прервано пользователем.")
                break

    return "\n".join(results) if results else "Ничего не выполнено."