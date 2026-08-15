import requests
from PIL import ImageGrab
SERVER_URL = "http://127.0.0.1:8000/post"
SCREENSHOT_FILE = "client_snap.png"
SEARCH_TARGET = "File" 
def make_screenshot(save_path: str):
    """ Сделать полный скриншот экрана на клиенте, сохранить в файл """
    snap = ImageGrab.grab()
    snap.save(save_path)
def send_screenshot(path_img: str, search_text: str):
    """ Отправить скриншот на сервер, получить ответ с координатами """
    with open(path_img, "rb") as f:
        resp = requests.post(
            SERVER_URL,
            params={"target_text": search_text},
            files={"file": f}
        )
    data = resp.json()
    print(f"Статус сервера: {data['status']}")
    vis = data["vision"]
    if vis["found"]:
        print(f"Найдено: {vis['text']} | X={vis['center_x']}, Y={vis['center_y']} | conf={vis['confidence']}")
    else:
        print(f" Не найдено текст: {search_text}, ошибка={vis.get('error')}")
    return data
if __name__ == "__main__":
    make_screenshot(SCREENSHOT_FILE)
    send_screenshot(SCREENSHOT_FILE, SEARCH_TARGET)