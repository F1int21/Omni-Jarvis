# core/planner.py
def create_plan(intent: str, params: dict) -> list:
    if intent == "search_file":
        return [{
            "action": "search_files",
            "params": {
                "pattern": params.get("filename", "отчёт"),
                "roots": ["C:\\Users\\Work\\Desktop", "C:\\Users\\Work\\Documents", "C:\\Users\\Work\\Desktop\\Omni-Jarvis"]
            }
        }]

    elif intent == "check_port":
        return [{"action": "run_command", "params": {"cmd": f"Test-NetConnection {params['ip']} -Port 443"}}]
    elif intent == "ping":
        return [{"action": "run_command", "params": {"cmd": f"ping {params['ip']} -n 4"}}]
    elif intent == "close_port":
        return [{"action": "run_command", "params": {"cmd": f"netsh advfirewall firewall add rule name='Block Port {params['port']}' dir=in action=block protocol=TCP localport={params['port']}"}}]
    elif intent == "create_user":
        return [{"action": "run_command", "params": {"cmd": f"net user {params['username']} P@ssw0rd /add"}}]
    elif intent == "click":
        return [{"action": "click", "params": {"target": params.get("target", "ОК")}}]
    else:
        return [{"action": "ask_user", "params": {"question": f"Задача не распознана: {params.get('text', '')}"}}]
    