# core/intent.py
# Модуль для распознавания намерений (интентов) из текстовой команды

def detect_intent(text: str) -> dict:
    """
    Преобразует текст в структурированный интент.
    Пока без LLM, только простые правила (регулярки и ключевые слова).
    """
    text_lower = text.lower().strip()
    
    # 1. Проверяем команды сисадмина
    if "порт" in text_lower and ("провер" in text_lower or "открыт" in text_lower):
        # Ищем IP-адрес в тексте (грубо)
        import re
        ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', text)
        ip = ip_match.group(0) if ip_match else "не указан"
        return {
            "intent": "check_port",
            "params": {"ip": ip}
        }
    
    # 2. Команда на закрытие порта
    if "закрой" in text_lower and "порт" in text_lower:
        return {
            "intent": "close_port",
            "params": {"port": 3389}  # по умолчанию, но можно распарсить
        }
    
    # 3. Остальные команды — пока заглушка
    return {
        "intent": "unknown",
        "params": {"text": text}
    }

# Тестовый запуск (для проверки в консоли)
if __name__ == "__main__":
    test_queries = [
        "проверь порт 3389 на сервере 192.168.1.10",
        "закрой порт",
        "сделай чай"
    ]
    for q in test_queries:
        print(f"{q} -> {detect_intent(q)}")# core/intent.py
# Модуль для распознавания намерений (интентов) из текстовой команды

def detect_intent(text: str) -> dict:
    """
    Преобразует текст в структурированный интент.
    Пока без LLM, только простые правила (регулярки и ключевые слова).
    """
    text_lower = text.lower().strip()
    
    # 1. Проверяем команды сисадмина
    if "порт" in text_lower and ("провер" in text_lower or "открыт" in text_lower):
        # Ищем IP-адрес в тексте (грубо)
        import re
        ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', text)
        ip = ip_match.group(0) if ip_match else "не указан"
        return {
            "intent": "check_port",
            "params": {"ip": ip}
        }
    
    # 2. Команда на закрытие порта
    if "закрой" in text_lower and "порт" in text_lower:
        return {
            "intent": "close_port",
            "params": {"port": 3389}  # по умолчанию, но можно распарсить
        }
    
    # 3. Остальные команды — пока заглушка
    return {
        "intent": "unknown",
        "params": {"text": text}
    }

# Тестовый запуск (для проверки в консоли)
if __name__ == "__main__":
    test_queries = [
        "проверь порт 3389 на сервере 192.168.1.10",
        "закрой порт",
        "сделай чай"
    ]
    for q in test_queries:
        print(f"{q} -> {detect_intent(q)}")