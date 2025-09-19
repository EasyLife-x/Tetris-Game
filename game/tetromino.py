# tetromino.py - Класс для представления тетрамино (фигур в Тетрисе) с эффектами

# Импортируем модуль для генерации случайных чисел и константы
import random
import pygame
import math
from constants import SHAPES, COLORS_3D  # Импортируем формы и цвета из констант


class Tetromino:
    """Класс для представления тетрамино - игровых фигур в Тетрисе"""

    def __init__(self, x, y):
        """
        Инициализация тетрамино
        x: начальная координата X (горизонтальная позиция)
        y: начальная координата Y (вертикальная позиция)
        """
        self.x = x  # Текущая X-координата фигуры
        self.y = y  # Текущая Y-координата фигуры

        # Генерируем случайный индекс для выбора формы фигуры
        self.shape_idx = random.randint(0, len(SHAPES) - 1)

        # Выбираем форму фигуры по случайному индексу
        self.shape = SHAPES[self.shape_idx]

        # Выбираем цвет фигуры по тому же индексу
        self.color = COLORS_3D[self.shape_idx]

        self.rotation = 0  # Текущий угол поворота фигуры
        self.animation_time = 0  # Время для анимации блеска
        self.rotation_animation = 0  # Анимация поворота

    def rotate(self):
        """
        Поворот фигуры на 90 градусов по часовой стрелке
        Возвращает новую форму фигуры после поворота
        """
        # Получаем размеры текущей формы
        rows = len(self.shape)  # Количество строк в текущей форме
        cols = len(self.shape[0])  # Количество столбцов в текущей форме

        # Создаем новую матрицу для повернутой формы
        # После поворота строки становятся столбцами
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]

        # Выполняем поворот матрицы на 90 градусов по часовой стрелке
        for r in range(rows):  # Проходим по каждой строке
            for c in range(cols):  # Проходим по каждому столбцу
                # Формула поворота: новая позиция [c][rows-1-r] = старая позиция [r][c]
                rotated[c][rows - 1 - r] = self.shape[r][c]

        return rotated  # Возвращаем повернутую форму

    def start_rotation_animation(self):
        """Начало анимации поворота"""
        self.rotation_animation = 15  # Количество кадров для анимации

    def update_animation(self, dt):
        """Обновление анимаций"""
        self.animation_time += dt
        if self.rotation_animation > 0:
            self.rotation_animation -= 1

    def get_positions(self):
        """
        Получение всех позиций ячеек фигуры относительно игрового поля
        Возвращает список кортежей (x, y) с координатами занятых ячеек
        """
        positions = []  # Список для хранения позиций ячеек

        # Проходим по каждой строке формы фигуры
        for y, row in enumerate(self.shape):
            # Проходим по каждому элементу в строке
            for x, cell in enumerate(row):
                # Если ячейка занята (равна 1)
                if cell:
                    # Добавляем абсолютные координаты ячейки на игровом поле
                    positions.append((self.x + x, self.y + y))

        return positions  # Возвращаем список всех позиций занятых ячеек

    def draw_cell(self, screen, x, y, grid_size, animation_offset=0):
        """
        Отрисовка одной ячейки фигуры с эффектами
        """
        color, shadow = self.color

        # Создаем прямоугольник для отрисовки ячейки
        rect = pygame.Rect(x, y, grid_size, grid_size)

        # Основной цвет с учетом анимации блеска
        brightness = 1.0 + 0.3 * math.sin(self.animation_time * 5)  # Пульсация
        bright_color = (
            min(255, int(color[0] * brightness)),
            min(255, int(color[1] * brightness)),
            min(255, int(color[2] * brightness))
        )

        # Рисуем основной цвет ячейки
        pygame.draw.rect(screen, bright_color, rect)

        # Добавляем градиент для 3D эффекта
        gradient_surface = pygame.Surface((grid_size, grid_size), pygame.SRCALPHA)
        for i in range(grid_size):
            alpha = int(100 * (1 - i / grid_size))
            pygame.draw.line(gradient_surface, (*shadow, alpha), (0, i), (grid_size, i))
        screen.blit(gradient_surface, (x, y))

        # Рисуем тень для создания 3D-эффекта
        pygame.draw.rect(screen, shadow, rect, max(1, grid_size // 15))

        # Добавляем эффект блеска (БЕЗ БЕЛЫХ ТОЧЕК)
        if grid_size > 10:  # Только для достаточно больших ячеек
            # Позиция блеска плавает
            shine_x = int(grid_size * 0.3 + 2 * math.sin(self.animation_time * 3))
            shine_y = int(grid_size * 0.3 + 2 * math.cos(self.animation_time * 2))

            if 0 <= shine_x < grid_size - 2 and 0 <= shine_y < grid_size - 2:
                shine_size = max(1, grid_size // 8)
                # Используем светлый оттенок основного цвета вместо белого
                shine_color = (
                    min(255, bright_color[0] + 50),
                    min(255, bright_color[1] + 50),
                    min(255, bright_color[2] + 50),
                    180  # Прозрачность
                )
                # Создаем поверхность для блеска с прозрачностью
                shine_surface = pygame.Surface((shine_size * 2, shine_size * 2), pygame.SRCALPHA)
                pygame.draw.ellipse(shine_surface, shine_color,
                                    (0, 0, shine_size * 2, shine_size * 2))
                screen.blit(shine_surface, (x + shine_x - shine_size // 2, y + shine_y - shine_size // 2))