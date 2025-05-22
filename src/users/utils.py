from PIL import Image, ImageDraw, ImageFont
import hashlib
import colorsys
import io
from django.core.files.base import ContentFile
import numpy as np

def generate_avatar(avatar_size: int, nickname: str) -> Image.Image:
    background_color = '#f2f1f2'
    s = nickname
    format = 'png'
    path = f'{s}.{format}'

    # Варианты генерации
    ## 12x12 - 144бит - 18байт
    ## 6*12 - 72бит - 9байт <- мне больше нравится
    ## Изображения получатся симметричными
    ## 6*6 - 36бит - 4.5байт

    ## Получаем набор псевдослучайных байт
    bytes = hashlib.md5(s.encode('utf-8')).digest()

    ## Получаем цвет из хеша
    main_color = bytes[:3]
    # rgb
    main_color = tuple(channel // 2 + 128 for channel in main_color)

    ## Генерируем матрицу заполнения блоков
    # массив 6 на 12
    need_color = np.array([bit == '1' for byte in bytes[3:3+9] for bit in bin(byte)[2:].zfill(8)]).reshape(6, 12)
    # получаем матрицу 12 на 12
    need_color = np.concatenate((need_color, need_color[::-1]), axis=0)

    # Добавляем рамку
    for i in range(12):
        need_color[0, i] = 0
        need_color[11, i] = 0
        need_color[i, 0] = 0
        need_color[i, 11] = 0

    ## Рисуем изображения по матрице заполнения
    img_size = (avatar_size, avatar_size)
    block_size = avatar_size // 12 # размер квадрата

    img = Image.new('RGB', img_size, background_color)
    draw = ImageDraw.Draw(img)

    for i in range(12):
        for j in range(12):
            if need_color[i, j]:
                # Рисуем квадрат
                x1 = j * block_size
                y1 = i * block_size
                x2 = x1 + block_size
                y2 = y1 + block_size
                draw.rectangle([x1, y1, x2, y2], fill=main_color)

    # Определяем угол поворота на основе хеша
    # Используем последний байт хеша для определения угла (0, 90, 180, 270)
    rotation_angle = (bytes[-1] % 4) * 45
    
    # Поворачиваем изображение
    if rotation_angle != 0:
        img = img.rotate(rotation_angle, expand=False, fillcolor=background_color)

    return img

def save_avatar_to_file(image, filename):
    """
    Save a PIL Image to a file-like object.
    Returns a ContentFile object.
    """
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=filename) 