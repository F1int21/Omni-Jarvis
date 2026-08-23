# core/agent.py
import json
import os
import re
import requests
from dotenv import load_dotenv

# ===== Загрузка API-ключа =====
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY не найден в .env")

# Твой рабочий URL (прокси Cloudflare)
WORKER_URL = "https://gemini-proxy.e084kn.workers.dev/v1beta/models/gemini-3.6-flash:generateContent"

# ===== Импорты модулей Джарвиса =====
from core.web_search import search_web
from core.step_executor import execute_step
from core.intent import detect_intent
from core.planner import create_plan

# ===== Функция подтверждения Y/N =====
def confirm(prompt: str = "Подтвердить? (Y/N): ") -> bool:
    """
    Запрашивает у пользователя ввод Y (yes/да) или N (no/нет).
    Возвращает True только при явном согласии.
    """
    while True:
        ans = input(prompt).strip().lower()
        if ans in ('y', 'yes', 'да'):
            return True
        elif ans in ('n', 'no', 'нет'):
            return False
        else:
            print("⚠️ Введите Y (да) или N (нет).")

# ===== Основная функция агента =====
def ask_agent(query: str) -> str:
    print("🔍 Ищу информацию в интернете...")
    search_results = search_web(query, max_results=2)
    print("✅ Поиск завершён.")

    # ===== Обновлённый промпт с новыми инструментами =====
    prompt = f"""
Ты — интеллектуальный помощник. Пользователь дал задачу: "{query}"

Вот информация из интернета по запросу:
{search_results}

Составь план действий в формате JSON-массива.
Каждый шаг — объект с полями:
- "action": одно из действий:
   * download(url, dest) — скачать файл.
   * run_command(cmd) — выполнить команду.
   * install_exe(path, silent) — запустить установщик.
   * search_files(pattern, roots, max) — найти файлы.
   * click(target) — кликнуть по тексту на экране.
   * ask_user(question) — запросить уточнение у пользователя.
   * send_email(to, subject, body, attachment) — отправить письмо.
   * move_file(src, dst) — скопировать/переместить файл.
   * parse_ticket(image_path) — распознать наряд/табличку с изображения (возвращает JSON с данными: номер наряда, адрес, тип работ, IP, логин, пароль, SN, MAC, ФИО).
   * open_lanbilling() — открыть интерфейс LanBilling (в браузере или приложении).
   * fill_lanbilling_fields(fields) — заполнить поля учётной записи (передать словарь с данными: fio, login, tariff, ip, mac, sn, date_start, date_end и др.).
   * submit_lanbilling() — сохранить учётную запись.
   * verify_lanbilling() — проверить, что запись создалась (поиск по логину или адресу).
- "params": словарь с параметрами для действия.
- "requires_confirmation": true, если шаг критичный (например, установка, отправка письма, создание учётки).

Если задача не требует действий, верни пустой массив [].
Пример для задачи с нарядом:
[
  {{"action":"parse_ticket", "params":{{"image_path":"C:/Users/Work/Desktop/naryad.jpg"}}}},
  {{"action":"open_lanbilling", "params":{{}}}},
  {{"action":"fill_lanbilling_fields", "params":{{"fields":{{"fio":"Иванов И.И.", "login":"ivanov", "tariff":"Продвинутый", "ip":"192.168.1.1", "mac":"8C:AE:DB:91:76:14", "sn":"RT420F312511003869"}}}}, "requires_confirmation": true}},
  {{"action":"submit_lanbilling", "params":{{}}}},
  {{"action":"verify_lanbilling", "params":{{}}}}
]
Ответь ТОЛЬКО JSON-массивом, без пояснений.
"""

    print("🧠 Генерирую план через Gemini...")
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    plan = []
    try:
        response = requests.post(WORKER_URL, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            clean = re.sub(r'```json\s*|\s*```', '', text).strip()
            if clean.startswith('['):
                plan = json.loads(clean)
            else:
                match = re.search(r'\[\s*\{.*\}\s*\]', clean, re.DOTALL)
                if match:
                    plan = json.loads(match.group(0))
                else:
                    plan = []
        else:
            print(f"⚠️ Gemini ошибка: {response.status_code}, {response.text[:200]}")
    except Exception as e:
        print(f"⚠️ Ошибка при запросе к Gemini: {e}")

    # 2. Fallback на словарный детектор
    if not plan or len(plan) == 0:
        print("🔄 Использую словарный детектор...")
        intent_data = detect_intent(query)
        plan = create_plan(intent_data["intent"], intent_data["params"])

    if not plan or (len(plan) == 1 and plan[0].get("action") == "ask_user"):
        question = plan[0].get("params", {}).get("question", "Задача не распознана") if plan else "Задача не распознана"
        return f"❌ {question}"

    # 3. Показываем план и запрашиваем общее подтверждение
    print("\n=== 📋 ПЛАН ДЕЙСТВИЙ ===")
    for i, step in enumerate(plan, 1):
        action = step.get("action")
        params = step.get("params", {})
        need_confirm = step.get("requires_confirmation", False)
        marker = " 🔒" if need_confirm else ""
        print(f"{i}. {action}: {params}{marker}")

    if not confirm("\nВыполнить план? (Y/N): "):
        return "❌ План отменён пользователем."

    # 4. Выполняем шаги
    results = []
    for i, step in enumerate(plan, 1):
        action = step.get("action")
        params = step.get("params", {})
        need_confirm = step.get("requires_confirmation", False)

        # Подтверждение критического шага
        if need_confirm:
            print(f"\n⚠️ Подтвердите действие: {action} с параметрами {params}")
            if not confirm("Продолжить? (Y/N): "):
                results.append(f"Шаг {i} отменён пользователем.")
                break

        print(f"\n▶️ Шаг {i}: {action}...")
        try:
            result = execute_step(step)
            results.append(f"Шаг {i}: {result}")
        except Exception as e:
            results.append(f"Шаг {i} ❌ Ошибка: {e}")
            if not confirm("Продолжить выполнение? (Y/N): "):
                results.append("Выполнение прервано пользователем.")
                break

    return "\n".join(results) if results else "Ничего не выполнено."

if __name__ == "__main__":
    # Для быстрой отладки
    print(ask_agent("установи virtualbox на windows"))