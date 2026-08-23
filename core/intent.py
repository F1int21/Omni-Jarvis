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
    
    # ПОИСК ФАЙЛОВ
    if "найди" in text_lower and ("файл" in text_lower or "файлы" in text_lower):
        match = re.search(r'(?:файл|файлы)\s*(.+)', text)
        if match:
            raw = match.group(1).strip()
            filename = re.sub(r'^(с|на|по|для)\s+', '', raw)
            if not filename:
                filename = "отчёт"
        else:
            filename = "отчёт"
        return {"intent": "search_file", "params": {"filename": filename}}
    
    # УСТАНОВКА ПРОГРАММЫ (исправленное извлечение)
    if "установи" in text_lower or "установить" in text_lower:
        # Убираем "на windows" и другие уточнения
        cleaned = re.sub(r'\s+(на|для|под)\s+windows', '', text_lower)
        match = re.search(r'(?:установи|установить)\s+([a-zа-яё0-9\-_]+)', cleaned, re.IGNORECASE)
        program = match.group(1) if match else "программу"
        return {"intent": "install_program", "params": {"program": program}}
    
    # Неизвестно
    return {"intent": "unknown", "params": {"text": text}}