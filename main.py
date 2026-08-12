import os
import requests
from PIL import ImageGrab

print("ДЖАРВИС: Делаю снимок экрана...")
#1. Делаем скриншот и сохраняем локально
screenshot = ImageGrab.grab()
screenshot.save("screenshot.png")

#2. Указываем адрес тестового сервера
server_url = "https://httpbin.org/post"

print(f"ДЖАРВИС: Отправляем файл screenshot.png на сервер {server_url}...")

#3. Открываем файл и упаковываем его в сетевой пакет
with open("screenshot.png", "rb") as file:
    network_payload = {"file": file}

    #4. Стреляем POST-запросом по сети
    response = requests.post(server_url, files=network_payload)

#5. Проверяем ответ сервера (Код 200 означает "Успешно долетело")
if response.status_code == 200:
    print("ДЖАРВИС: Сетевой мост работает! Файл успешно доставлен не сервер!")
else:
    print(f"ОШИБКА СЕТИ: Сервер вернул код {response.status_code}")