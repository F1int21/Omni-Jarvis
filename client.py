import os
import requests
from PIL import ImageGrab

print("КЛИЕНТ: Снятие скриншота экрана...")
screenshot = ImageGrab.grab()
screenshot.save("screenshot.png")

#Направляем трафик на ваш локальный домашний сервер (порт 8000, эндпоинт /post)
server_url = "http://127.0.0.1:8000/post"

print(f" КЛИЕНТ: Отправка пакета на домашний сервер {server_url}...")

with open("screenshot.png", "rb") as file:
    network_payload = {"file": file}
    response = requests.post(server_url, files=network_payload)

if response.status_code == 200:
    print("КЛИЕНТ: Данные успешно доставлены на сервер! Сетевой мост стабилен!")
else:
    print(f"КЛИЕНТ ОШИБКА: Сервер ответил кодом {response.status_code}")