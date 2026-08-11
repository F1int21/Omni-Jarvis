# 1. ОПРЕДЕЛЯЕМ ФУНКЦИЮ (Создаем инструмент)
def run_guardrails(client, ports):
    print(f"СИСТЕМА: Запуск риск-фильтра для клиента {client}...]]")
    for port in ports:
        if port == 23:
            print(f"БЛОКИРОВКА! Порт {port} - критический магистральный аплинк!")
        else:
            print(f"Порт {port} проверен. Узел безопасен.")

# 2. ИСПОЛЬЗУЕМ ИНСТРУМЕНТ (Вызываем функцию для разных офисов)
office_a_ports = [21, 22, 23]
office_b_ports = [80, 443, 8080]

# Вызов первый
run_guardrails("Omega_Office_A", office_a_ports)

print("-" * 40) # Просто линия разделителя в консоли
# Вызов второй
run_guardrails("Alpha_Office_B", office_b_ports)