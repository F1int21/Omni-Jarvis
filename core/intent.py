# core/intent.py
import re
import requests
import json

def detect_intent(text: str) -> dict:
    """
    Словарный детектор (регулярки и ключевые слова).
    """
    text_lower = text.lower().strip()
    
    # 1. Проверка порта
    if "порт" in text_lower and ("провер" in text_lower or "открыт" in text_lower):
        ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', text)
        ip = ip_match.group(0) if ip_match else "не указан"
        return {"intent": "check_port", "params": {"ip": ip}}
    
    # 2. Закрытие порта
    if "закрой" in text_lower and "порт" in text_lower:
        port_match = re.search(r'\b(\d{1,5})\b', text)
        port = int(port_match.group(1)) if port_match else 3389
        return {"intent": "close_port", "params": {"port": port}}
    
    # 3. Пинг
    if "пинг" in text_lower or "пропинг" in text_lower:
        ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', text)
        ip = ip_match.group(0) if ip_match else "не указан"
        return {"intent": "ping", "params": {"ip": ip}}
    
    # 4. Создание пользователя
    if "создай" in text_lower and ("пользователя" in text_lower or "учётку" in text_lower or "учетку" in text_lower):
        user_match = re.search(r'для\s*([А-Яа-яЁёA-Za-z]+)', text)
        username = user_match.group(1) if user_match else "новый_пользователь"
        return {"intent": "create_user", "params": {"username": username}}
    
    # 5. Неизвестно
    return {"intent": "unknown", "params": {"text": text}}

def detect_intent_llm(text: str, model: str = "deepseek-r1:1.5b") -> dict:
    """
    Отправляет текст в Ollama, возвращает интент.
    Если Ollama недоступна — падает на словарный детектор.
    """
    prompt = f"""
Ты — интеллектуальный помощник. Преобразуй команду пользователя в структурированный JSON.
Поля:
- intent: тип действия (check_port, close_port, create_user, search_file, ping, install_vm, unknown)
- params: параметры (ip, port, username, filename, os и т.д.)

Команда: "{text}"

Ответь ТОЛЬКО JSON, без пояснений.
"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            },
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            result = json.loads(data.get("response", "{}"))
            if "intent" not in result:
                result = {"intent": "unknown", "params": {"text": text}}
            return result
        else:
            return detect_intent(text)
    except Exception as e:
        print(f"[Ошибка Ollama] {e}, используем словарный детектор")
        return detect_intent(text)

# Функция для запуска агента (используется в интерактивном режиме и позже в сервере)
def run_agent(text: str) -> str:
    from core.planner import create_plan
    from core.executor import execute_step
    
    intent_data = detect_intent_llm(text)
    intent = intent_data["intent"]
    params = intent_data["params"]
    plan = create_plan(intent, params)
    results = []
    for step in plan:
        result = execute_step(step)
        results.append(result)
    return "\n".join(results)

if __name__ == "__main__":
    print("=== Omni-Jarvis Agent (симуляция) ===")
    while True:
        cmd = input(">> ")
        if cmd.lower() in ("exit", "quit", "q"):
            break
        output = run_agent(cmd)
        print(f"  → {output}\n")