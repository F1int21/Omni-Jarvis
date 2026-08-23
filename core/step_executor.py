# core/step_executor.py
import subprocess
import os
import requests
import shutil

def execute_step(step: dict) -> str:
    """
    Выполняет один шаг плана.
    Поддерживаемые действия:
    - download: скачать файл по URL
    - run_command: выполнить команду в shell
    - install_exe: запустить установщик (тихо)
    - search_files: найти файлы по маске
    - move_file: переместить/скопировать файл
    - ask_user: запросить уточнение у пользователя (возвращает ввод)
    """
    action = step.get("action")
    params = step.get("params", {})

    if action == "download":
        url = params.get("url")
        dest_dir = params.get("dest", "C:\\Downloads")
        os.makedirs(dest_dir, exist_ok=True)
        filename = url.split("/")[-1]
        local_path = os.path.join(dest_dir, filename)
        print(f"  ⬇️ Скачиваю {url} -> {local_path}")
        try:
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return f"✅ Скачано: {local_path}"
        except Exception as e:
            return f"❌ Ошибка скачивания: {e}"

    elif action == "run_command":
        cmd = params.get("cmd")
        print(f"  ⚙️ Выполняю команду: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            output = result.stdout + result.stderr
            if result.returncode == 0:
                return f"✅ Команда выполнена:\n{output[:500]}"
            else:
                return f"⚠️ Команда завершилась с кодом {result.returncode}:\n{output[:500]}"
        except Exception as e:
            return f"❌ Ошибка выполнения: {e}"

    elif action == "install_exe":
        exe_path = params.get("path")
        silent = params.get("silent", True)
        args = params.get("args", "/S" if silent else "")
        print(f"  📦 Устанавливаю: {exe_path} {args}")
        try:
            cmd = f'"{exe_path}" {args}'
            subprocess.run(cmd, shell=True, check=True, timeout=300)
            return f"✅ Установка запущена (может занять время)."
        except Exception as e:
            return f"❌ Ошибка установки: {e}"

    elif action == "search_files":
        pattern = params.get("pattern", "")
        roots = params.get("roots", ["C:\\Users\\Work\\Desktop", "C:\\Users\\Work\\Documents"])
        max_results = params.get("max", 10)
        print(f"  🔍 Ищу файлы по шаблону: {pattern} в {roots}")
        try:
            from modules.file_finder import find_files_by_name
            found = find_files_by_name(roots, pattern, max_results=max_results)
            if found:
                return "Найдены файлы:\n" + "\n".join(f"  - {p}" for p in found)
            else:
                return "Файлы не найдены."
        except Exception as e:
            return f"❌ Ошибка поиска: {e}"

    elif action == "move_file":
        src = params.get("src")
        dst = params.get("dst")
        print(f"  📂 Копирую {src} -> {dst}")
        try:
            shutil.copy2(src, dst)
            return f"✅ Скопировано в {dst}"
        except Exception as e:
            return f"❌ Ошибка копирования: {e}"

    elif action == "ask_user":
        question = params.get("question", "Уточните, пожалуйста:")
        print(f"  ❓ {question}")
        answer = input(">> ").strip()
        return f"Ответ пользователя: {answer}"

    elif action == "click":
        target = params.get("target")
        if not target:
            return "❌ Не указан target для клика."
        print(f"  🖱️ Ищу текст '{target}' на экране...")
        try:
            from ai_vision import find_text_center
            import pyautogui
            # Делаем скриншот и ищем
            screenshot_path = "click_scan.png"
            import pyautogui as pg
            pg.screenshot(screenshot_path)
            result = find_text_center(screenshot_path, [target])
            if result:
                x, y = result['x'], result['y']
                print(f"  ✅ Найдено в ({x}, {y}), кликаю...")
                pyautogui.click(x, y)
                return f"✅ Клик по '{target}' выполнен в ({x}, {y})"
            else:
                return f"❌ Текст '{target}' не найден на экране."
        except Exception as e:
            return f"❌ Ошибка клика: {e}"

    elif action == "parse_ticket":
        image_path = params.get("image_path")
        if not image_path:
            return "❌ Не указан путь к изображению."
        from core.ticket_parser import parse_ticket_image
        data = parse_ticket_image(image_path)
        return f"Данные наряда: {json.dumps(data, ensure_ascii=False, indent=2)}"

    elif action == "open_lanbilling":
        # Пока заглушка — потом заменим на реальный клик/открытие браузера
        return "🔜 Открытие LanBilling (в разработке)"

    elif action == "fill_lanbilling_fields":
        # Принимает словарь с полями (ФИО, логин, тариф, IP, MAC, SN и т.д.)
        fields = params.get("fields", {})
        # Здесь будет логика заполнения через кликер/ввод текста
        return f"🔜 Заполнение полей: {fields}"

    elif action == "submit_lanbilling":
        # Нажать кнопку «Сохранить» или «Создать»
        return "🔜 Сохранение учётной записи"

    elif action == "verify_lanbilling":
        # Проверить, что запись создалась (поиск по логину или адресу)
        return "🔜 Проверка создания учётной записи"

    else:
        return f"❌ Неизвестное действие: {action}"