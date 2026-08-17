# core/planner.py
# Планировщик: превращает интент в последовательность шагов

def create_plan(intent: str, params: dict) -> list:
    """
    Возвращает список шагов для выполнения.
    Каждый шаг — словарь с action и параметрами.
    """
    if intent == "check_port":
        return [
            {"action": "run_command", "cmd": f"Test-NetConnection {params['ip']} -Port 443"}
        ]
    elif intent == "close_port":
        return [
            {"action": "run_command", "cmd": f"netsh advfirewall firewall add rule name='Block Port {params['port']}' dir=in action=block protocol=TCP localport={params['port']}"}
        ]
    elif intent == "ping":
        return [
            {"action": "run_command", "cmd": f"ping {params['ip']} -n 4"}
        ]
    elif intent == "create_user":
        return [
            {"action": "run_command", "cmd": f"net user {params['username']} P@ssw0rd /add"}
        ]
    else:
        return [{"action": "unknown", "cmd": f"Не знаю, как выполнить: {params.get('text', '')}"}]