# core/ticket_parser.py
import os
import json
import re
import requests
import base64
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WORKER_URL = "https://gemini-proxy.e084kn.workers.dev/v1beta/models/gemini-3.6-flash:generateContent"  # Поддерживает изображения

def encode_image(image_path: str) -> str:
    """Кодирует изображение в base64."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def parse_ticket_images(image_paths: list) -> dict:
    """
    Отправляет изображения в Gemini Vision и возвращает структурированные данные.
    """
    # Кодируем все изображения в base64
    images_base64 = [encode_image(path) for path in image_paths if os.path.exists(path)]
    if not images_base64:
        return {"error": "Ни одно изображение не найдено."}

    # Формируем промпт с инструкцией
    prompt = """
Ты — интеллектуальный помощник. На изображениях — наряд-заявка и табличка с параметрами оборудования.
Извлеки следующие данные в формате JSON:
- "номер_наряда" (например, "8949/26")
- "адрес" (улица, дом, квартира)
- "тип_работ" (подключение/отключение/ремонт)
- "ip_адрес" (например, "192.168.1.1")
- "логин" (например, "Admin")
- "пароль" (например, "Admin")
- "серийный_номер" (SN, например, "RT420F312511003869")
- "mac_адрес" (например, "8C:AE:DB:91:76:14")
- "фио_ответственного" (ФИО)

Обрати внимание на рукописный текст в наряде: ищи номер наряда, адрес, ФИО. Если поле не найдено, укажи null.
Верни ТОЛЬКО JSON-объект.
"""

    # Собираем содержимое запроса: текстовый промпт + изображения
    parts = [{"text": prompt}]
    for img_b64 in images_base64:
        parts.append({
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": img_b64
            }
        })

    payload = {
        "contents": [{"parts": parts}]
    }

    headers = {"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY}

    try:
        response = requests.post(WORKER_URL, json=payload, headers=headers, timeout=60)
        if response.status_code == 200:
            data = response.json()
            text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            clean = re.sub(r'```json\s*|\s*```', '', text).strip()
            return json.loads(clean)
        else:
            return {"error": f"Gemini ошибка: {response.status_code}, {response.text[:200]}"}
    except Exception as e:
        return {"error": str(e)}