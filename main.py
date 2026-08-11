import os
from PIL import ImageGrab

print("ДЖАРВИС: Активирую модуль скрытых глаз клиента...")


# 1. Делаем снимок всего экрана прямо сейчас
screenshot = ImageGrab.grab()

# 2. Сохраняем получившуюся картинку в папку нашего проекта под именем screenshot.png
screenshot.save("screenshot.png")

print("ДЖАРВИС: Скриншот экрана успешно сделан и сохранен в папку проекта!")