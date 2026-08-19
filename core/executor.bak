# core/executor.py
# Исполнитель — выполняет шаги плана (СИМУЛЯЦИЯ, БЕЗ РЕАЛЬНЫХ ДЕЙСТВИЙ)

def execute_step(step: dict) -> str:
    """
    Выполняет один шаг плана.
    В безопасном режиме только выводит, что сделал бы, без реального выполнения.
    """
    action = step.get("action")
    cmd = step.get("cmd", "")
    
    if action == "run_command":
        # ⚠️ БЕЗОПАСНЫЙ РЕЖИМ: только симуляция
        return f"[СИМУЛЯЦИЯ] Выполнил бы команду: {cmd}"
        
        # 🚫 ОПАСНЫЙ КОД (реальное выполнение) — закомментирован
        # try:
        #     import subprocess
        #     result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        #     return f"✅ Выполнено:\n{result.stdout}\n{result.stderr}"
        # except Exception as e:
        #     return f"❌ Ошибка выполнения: {e}"
    
    elif action == "unknown":
        return f"⚠️ {cmd}"
    
    else:
        return f"❌ Неизвестное действие: {action}"

