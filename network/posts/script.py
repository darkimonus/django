from PIL import Image
import os

# Папка, содержащая эмодзи
emoji_dir = 'E:\learning\django\static_cdn\media_root\emojis'

# Желаемый размер эмодзи
desired_size = (25, 25)  # Ширина x Высота

# Проход по всем файлам в папке с эмодзи
for filename in os.listdir(emoji_dir):
    if filename.endswith('.png'):
        # Открытие изображения
        img = Image.open(os.path.join(emoji_dir, filename))
        # Изменение размера
        img_resized = img.resize(desired_size)
        # Сохранение измененного изображения
        img_resized.save(os.path.join(emoji_dir, filename))
