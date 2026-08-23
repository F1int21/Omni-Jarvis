# test_ticket.py
from core.ticket_parser import parse_ticket_images

image_paths = [
    r"C:\Users\Work\Downloads\1000138736.jpg",
    r"C:\Users\Work\Downloads\1000138737.jpg"
]

data = parse_ticket_images(image_paths)
print("Распознанные данные:")
print(data)