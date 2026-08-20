# core/intent.py
import re

def detect_intent(text: str) -> dict:
    text_lower = text.lower().strip()
    
    # Проверка порта
    if "порт" in text_lower and ("провер" in text_lower or "открыт" in text_lower):
        ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', text)
        ip = ip_match.group(0) if ip_match else "не указан"
        return {"intent": "check_port", "params": {"ip": ip}}
    
    # Закрытие порта
    if "закрой" in text_lower and "порт" in text_lower:
        port_match = re.search(r'\b(\d{1,5})\b', text)
        port = int(port_match.group(1)) if port_match else 3389
        return {"intent": "close_port", "params": {"port": port}}
    
    # Пинг
    if "пинг" in text_lower or "пропинг" in text_lower:
        ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', text)
        ip = ip_match.group(0) if ip_match else "не указан"
        return {"intent": "ping", "params": {"ip": ip}}
    
    # Создание пользователя
    if "создай" in text_lower and ("пользователя" in text_lower or "учётку" in text_lower or "учетку" in text_lower):
        user_match = re.search(r'для\s*([А-Яа-яЁёA-Za-z]+)', text)
        username = user_match.group(1) if user_match else "новый_пользователь"
        return {"intent": "create_user", "params": {"username": username}}

    # Клик по кнопке
    if "нажми" in text_lower or "клик" in text_lower:
        # Ищем название кнопки после "нажми" или "клик"
        match = re.search(r'(?:нажми|клик)\s+(.+)', text, re.IGNORECASE)
        target = match.group(1).strip() if match else "ОК"
        return {"intent": "click", "params": {"target": target}}

    # ПОИСК ФАЙЛОВ (с коррекцией окончаний)
    if "найди" in text_lower and ("файл" in text_lower or "файлы" in text_lower):
        # 1. Сначала проверяем, есть ли в запросе слово "отчёт" (в любом падеже)
        if "отчёт" in text_lower:
            filename = "отчёт"
        else:
            # 2. Иначе пытаемся вытащить первое слово после "файл" или "файлы"
            match = re.search(r'(?:файл|файлы)\s+(?:с|на|по|для)?\s*([А-Яа-яЁёA-Za-z0-9_\-]+)', text, re.IGNORECASE)
            if match:
                filename = match.group(1)
            else:
                filename = "отчёт"
        return {"intent": "search_file", "params": {"filename": filename}}
          
    # Неизвестно
    return {"intent": "unknown", "params": {"text": text}}