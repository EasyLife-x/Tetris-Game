# game.py - Основной класс игры Тетрис с всей игровой логикой

# Импортируем необходимые модули
import pygame
import sys
import random
from tetromino import Tetromino  # Импортируем класс тетрамино
from constants import *  # Импортируем все константы
from ui import UI  # Импортируем класс интерфейса


class TetrisGame:
    """Основной класс игры Тетрис"""

    def __init__(self):
        """Инициализация игры Тетрис"""
        # Получаем информацию о текущем экране для определения его размеров
        info = pygame.display.Info()
        self.screen_width = info.current_w  # Ширина текущего экрана
        self.screen_height = info.current_h  # Высота текущего экрана

        # Создаем окно игры с возможностью изменения размера
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Тетрис")  # Устанавливаем заголовок окна

        # Создаем объект для управления временем
        self.clock = pygame.time.Clock()

        # Создаем объект интерфейса пользователя
        self.ui = UI(self.screen, self.screen_width, self.screen_height)

        # Инициализируем игровое состояние
        self.reset_game()  # Сбрасываем игру к начальному состоянию
        self.game_state = "menu"  # Устанавливаем начальное состояние - главное меню
        self.next_piece = self.new_piece()  # Создаем первую следующую фигуру

        # Переменные для масштабирования игрового поля
        self.grid_size = 30  # Размер одной ячейки сетки
        self.play_area_x = 0  # Горизонтальная позиция игрового поля
        self.play_area_y = 0  # Вертикальная позиция игрового поля
        self.sidebar_x = 0  # Горизонтальная позиция боковой панели

    def reset_game(self):
        """Сброс игры к начальному состоянию"""
        # Создаем пустую игровую сетку (20 строк по 10 столбцов)
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

        # Создаем первую игровую фигуру
        self.current_piece = self.new_piece()

        # Сбрасываем игровую статистику
        self.score = 0  # Счет игрока
        self.level = 1  # Уровень сложности
        self.lines_cleared = 0  # Количество очищенных линий

        # Параметры падения фигур
        self.fall_speed = 0.5  # Скорость падения в секундах
        self.fall_time = 0  # Время с последнего падения

        # Состояние паузы
        self.paused = False

    def new_piece(self):
        """Создание новой фигуры"""
        # Создаем новую фигуру в центре верхней части игрового поля
        return Tetromino(GRID_WIDTH // 2 - 1, 0)

    def valid_position(self, piece=None):
        """
        Проверка, является ли позиция фигуры допустимой (не выходит за границы и не пересекается с другими фигурами)
        piece: фигура для проверки (если None, проверяется текущая фигура)
        Возвращает True, если позиция допустима, иначе False
        """
        # Если фигура не указана, используем текущую фигуру
        if piece is None:
            piece = self.current_piece

        # Получаем все позиции ячеек фигуры
        for x, y in piece.get_positions():
            # Проверяем, не выходит ли фигура за границы игрового поля по горизонтали
            if x < 0 or x >= GRID_WIDTH:
                return False  # Вышла за левую или правую границу

            # Проверяем, не выходит ли фигура за нижнюю границу
            if y >= GRID_HEIGHT:
                return False  # Вышла за нижнюю границу

            # Проверяем, не пересекается ли фигура с уже упавшими фигурами
            # (только для ячеек внутри игрового поля)
            if y >= 0 and self.grid[y][x]:
                return False  # Пересекается с другой фигурой

        return True  # Позиция допустима

    def merge_piece(self):
        """Объединение фигуры с игровым полем (фиксация фигуры на поле)"""
        # Получаем все позиции ячеек текущей фигуры
        for x, y in self.current_piece.get_positions():
            # Проверяем, что ячейка находится внутри игрового поля
            if y >= 0:
                # Помещаем цвет фигуры в соответствующую ячейку игрового поля
                self.grid[y][x] = self.current_piece.color

    def clear_lines(self):
        """Очистка заполненных линий"""
        lines_to_clear = []  # Список для хранения индексов заполненных линий

        # Проходим по каждой строке игрового поля
        for i, row in enumerate(self.grid):
            # Проверяем, заполнена ли строка (все ячейки не равны 0)
            if all(cell != 0 for cell in row):
                lines_to_clear.append(i)  # Добавляем индекс заполненной строки

        # Если есть заполненные строки для очистки
        for line in lines_to_clear:
            # Удаляем заполненную строку
            del self.grid[line]
            # Добавляем новую пустую строку в начало поля
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])

        # Обновление счета, если были очищены линии
        if lines_to_clear:
            # Увеличиваем счетчик очищенных линий
            self.lines_cleared += len(lines_to_clear)

            # Начисляем очки в зависимости от количества одновременно очищенных линий
            # 1 линия - 100 очков, 2 линии - 300 очков, 3 линии - 500 очков, 4 линии - 800 очков
            # Умножаем на текущий уровень для увеличения сложности
            self.score += [100, 300, 500, 800][min(len(lines_to_clear) - 1, 3)] * self.level

            # Увеличиваем уровень каждые 10 очищенных линий
            self.level = self.lines_cleared // 10 + 1

            # Увеличиваем скорость падения с каждым уровнем (но не меньше 0.05 секунд)
            self.fall_speed = max(0.05, 0.5 - (self.level - 1) * 0.05)

    def move(self, dx, dy):
        """
        Перемещение текущей фигуры
        dx: смещение по горизонтали (-1 - влево, 1 - вправо, 0 - без смещения)
        dy: смещение по вертикали (1 - вниз, 0 - без смещения)
        """
        # Изменяем координаты фигуры
        self.current_piece.x += dx
        self.current_piece.y += dy

        # Проверяем, допустима ли новая позиция
        if not self.valid_position():
            # Если позиция недопустима, возвращаем фигуру в предыдущее положение
            self.current_piece.x -= dx
            self.current_piece.y -= dy

            # Если перемещение было вниз (падение)
            if dy > 0:
                # Фиксируем фигуру на игровом поле
                self.merge_piece()
                # Проверяем и очищаем заполненные линии
                self.clear_lines()
                # Создаем новую текущую фигуру из следующей
                self.current_piece = self.next_piece
                # Генерируем новую следующую фигуру
                self.next_piece = self.new_piece()
                # Проверяем, может ли новая фигура появиться на поле
                if not self.valid_position():
                    # Если не может - игра окончена
                    self.game_state = "game_over"

    def rotate_piece(self):
        """Поворот текущей фигуры"""
        # Сохраняем оригинальную форму на случай, если поворот будет недопустим
        original_shape = self.current_piece.shape
        # Применяем поворот к фигуре
        self.current_piece.shape = self.current_piece.rotate()
        # Проверяем, допустима ли новая форма
        if not self.valid_position():
            # Если недопустима, возвращаем оригинальную форму
            self.current_piece.shape = original_shape

    def hard_drop(self):
        """Мгновенное падение фигуры вниз до первого препятствия"""
        # Падаем вниз, пока позиция допустима
        while self.valid_position():
            self.current_piece.y += 1  # Перемещаем фигуру вниз

        # Возвращаем фигуру на одну позицию вверх (последняя допустимая позиция)
        self.current_piece.y -= 1

        # Фиксируем фигуру на игровом поле
        self.merge_piece()
        # Проверяем и очищаем заполненные линии
        self.clear_lines()
        # Создаем новую текущую фигуру из следующей
        self.current_piece = self.next_piece
        # Генерируем новую следующую фигуру
        self.next_piece = self.new_piece()
        # Проверяем, может ли новая фигура появиться на поле
        if not self.valid_position():
            # Если не может - игра окончена
            self.game_state = "game_over"

    def calculate_dimensions(self):
        """Пересчет размеров элементов для заполнения всего экрана по высоте"""
        # Вычисляем размер ячейки так, чтобы игровое поле заполнило всю высоту экрана
        self.grid_size = self.screen_height // GRID_HEIGHT

        # Вычисляем размеры игрового поля в пикселях
        self.play_area_width = GRID_WIDTH * self.grid_size  # Ширина игрового поля
        self.play_area_height = GRID_HEIGHT * self.grid_size  # Высота игрового поля

        # Вычисляем позиции элементов (центрируем по горизонтали)
        # Игровое поле размещается по центру, боковая панель справа
        self.play_area_x = (self.screen_width - SIDEBAR_WIDTH - self.play_area_width) // 2
        self.play_area_y = 0  # Начинаем с верха экрана
        self.sidebar_x = self.play_area_x + self.play_area_width  # Боковая панель справа от игрового поля

    def draw_grid(self):
        """Отрисовка игрового поля"""
        # Отрисовка фона игрового поля (с небольшим отступом для создания рамки)
        pygame.draw.rect(self.screen, DARK_GRAY,
                         (self.play_area_x - 5,  # X-координата с отступом
                          self.play_area_y - 5,  # Y-координата с отступом
                          self.play_area_width + 10,  # Ширина с учетом отступов
                          self.play_area_height + 10))  # Высота с учетом отступов

        # Отрисовка сетки игрового поля
        for x in range(GRID_WIDTH):  # Проходим по всем столбцам
            for y in range(GRID_HEIGHT):  # Проходим по всем строкам
                # Рисуем границы ячейки
                pygame.draw.rect(self.screen, GRID_COLOR,
                                 (self.play_area_x + x * self.grid_size,  # X-координата ячейки
                                  self.play_area_y + y * self.grid_size,  # Y-координата ячейки
                                  self.grid_size,  # Ширина ячейки
                                  self.grid_size),  # Высота ячейки
                                 1)  # Толщина линии границы = 1 пиксель

                # Отрисовка заполненных ячеек (уже упавших фигур)
                if self.grid[y][x]:  # Если ячейка заполнена
                    color, shadow = self.grid[y][x]  # Получаем цвет и тень

                    # Создаем прямоугольник для отрисовки ячейки
                    rect = pygame.Rect(self.play_area_x + x * self.grid_size,  # X-координата
                                       self.play_area_y + y * self.grid_size,  # Y-координата
                                       self.grid_size,  # Ширина
                                       self.grid_size)  # Высота

                    # Рисуем основной цвет ячейки
                    pygame.draw.rect(self.screen, color, rect)
                    # Рисуем тень для создания 3D-эффекта
                    pygame.draw.rect(self.screen, shadow, rect, max(1, self.grid_size // 15))

    def draw_current_piece(self):
        """Отрисовка текущей фигуры"""
        # Рисуем текущую фигуру только во время игры или паузы
        if self.game_state == "playing" or self.game_state == "paused":
            # Получаем все позиции ячеек текущей фигуры
            for x, y in self.current_piece.get_positions():
                # Рисуем только ячейки, которые находятся внутри игрового поля
                if y >= 0:
                    color, shadow = self.current_piece.color  # Получаем цвет фигуры

                    # Создаем прямоугольник для отрисовки ячейки фигуры
                    rect = pygame.Rect(self.play_area_x + x * self.grid_size,  # X-координата
                                       self.play_area_y + y * self.grid_size,  # Y-координата
                                       self.grid_size,  # Ширина
                                       self.grid_size)  # Высота

                    # Рисуем основной цвет ячейки фигуры
                    pygame.draw.rect(self.screen, color, rect)
                    # Рисуем тень для создания 3D-эффекта
                    pygame.draw.rect(self.screen, shadow, rect, max(1, self.grid_size // 15))

    def draw_next_piece(self):
        """Отрисовка следующей фигуры в сайдбаре"""
        # Вычисляем высоту области для отображения следующей фигуры (20% от высоты экрана)
        next_piece_height = int(self.screen_height * 0.2)

        # Отрисовка фона области следующей фигуры
        pygame.draw.rect(self.screen, DARK_GRAY,
                         (self.sidebar_x + 10,  # X-координата (с отступом от края сайдбара)
                          20,  # Y-координата (отступ сверху)
                          SIDEBAR_WIDTH - 20,  # Ширина (с отступами по краям)
                          next_piece_height))  # Высота области

        # Отрисовка рамки вокруг области следующей фигуры
        pygame.draw.rect(self.screen, GRAY,
                         (self.sidebar_x + 10,
                          20,
                          SIDEBAR_WIDTH - 20,
                          next_piece_height),
                         2)  # Толщина рамки = 2 пикселя

        # Отрисовка заголовка "Следующая:"
        next_text = self.ui.font.render("Следующая:", True, WHITE)  # Создаем белый текст
        self.screen.blit(next_text, (self.sidebar_x + 20, 40))  # Отображаем текст с отступами

        # Отрисовка следующей фигуры
        shape = self.next_piece.shape  # Получаем форму следующей фигуры
        color, shadow = self.next_piece.color  # Получаем цвет следующей фигуры

        # Вычисляем размеры фигуры в пикселях
        piece_width = len(shape[0]) * self.grid_size  # Ширина фигуры
        piece_height = len(shape) * self.grid_size  # Высота фигуры

        # Вычисляем позицию для центрирования фигуры в области
        start_x = self.sidebar_x + 20 + (SIDEBAR_WIDTH - 40 - piece_width) // 2  # Центрируем по горизонтали
        start_y = 80 + (next_piece_height - 100 - piece_height) // 2  # Центрируем по вертикали

        # Отрисовываем каждую ячейку фигуры
        for y, row in enumerate(shape):  # Проходим по строкам фигуры
            for x, cell in enumerate(row):  # Проходим по ячейкам строки
                if cell:  # Если ячейка занята
                    # Создаем прямоугольник для отрисовки ячейки
                    rect = pygame.Rect(start_x + x * self.grid_size,  # X-координата
                                       start_y + y * self.grid_size,  # Y-координата
                                       self.grid_size,  # Ширина
                                       self.grid_size)  # Высота

                    # Рисуем основной цвет ячейки
                    pygame.draw.rect(self.screen, color, rect)
                    # Рисуем тень для создания 3D-эффекта
                    pygame.draw.rect(self.screen, shadow, rect, max(1, self.grid_size // 15))

    def draw_sidebar(self):
        """Отрисовка сайдбара с информацией"""
        # Вычисляем позицию и размеры сайдбара
        sidebar_top = int(self.screen_height * 0.25)  # Верхняя граница сайдбара (25% от высоты экрана)
        sidebar_height = self.screen_height - sidebar_top - 20  # Высота сайдбара (до нижнего края с отступом)

        # Отрисовка фона сайдбара
        pygame.draw.rect(self.screen, DARK_GRAY,
                         (self.sidebar_x + 10,  # X-координата с отступом
                          sidebar_top,  # Верхняя граница
                          SIDEBAR_WIDTH - 20,  # Ширина с отступами
                          sidebar_height))  # Высота

        # Отрисовка рамки вокруг сайдбара
        pygame.draw.rect(self.screen, GRAY,
                         (self.sidebar_x + 10,
                          sidebar_top,
                          SIDEBAR_WIDTH - 20,
                          sidebar_height),
                         2)  # Толщина рамки

        # Отрисовка счета игрока
        score_text = self.ui.font.render(f"Счет: {self.score}", True, WHITE)  # Создаем текст со счетом
        self.screen.blit(score_text, (self.sidebar_x + 20, sidebar_top + 20))  # Отображаем с отступом

        # Отрисовка текущего уровня
        level_text = self.ui.font.render(f"Уровень: {self.level}", True, WHITE)  # Создаем текст с уровнем
        self.screen.blit(level_text, (self.sidebar_x + 20, sidebar_top + 70))  # Отображаем ниже счета

        # Отрисовка количества очищенных линий
        lines_text = self.ui.font.render(f"Линии: {self.lines_cleared}", True, WHITE)  # Создаем текст с линиями
        self.screen.blit(lines_text, (self.sidebar_x + 20, sidebar_top + 120))  # Отображаем ниже уровня

        # Отрисовка инструкции управления
        controls_y = sidebar_top + 180  # Вертикальная позиция для инструкции
        # Список элементов управления
        controls = [
            "Управление:",  # Заголовок
            "A - Влево",  # Движение влево
            "D - Вправо",  # Движение вправо
            "S - Вниз",  # Ускоренное падение
            "W - Поворот",  # Поворот фигуры
            "Пробел - Сброс",  # Мгновенное падение
            "ESC - Меню"  # Открытие меню паузы
        ]

        # Отрисовываем каждый элемент управления
        for i, text in enumerate(controls):
            ctrl_text = self.ui.small_font.render(text, True, WHITE)  # Создаем текст белым цветом
            # Отображаем с вертикальным отступом между элементами
            self.screen.blit(ctrl_text, (self.sidebar_x + 20, controls_y + i * 35))

    def handle_menu_events(self, play_button, quit_button):
        """Обработка событий в главном меню"""
        # Обрабатываем все события в очереди
        for event in pygame.event.get():
            # Закрытие окна игры
            if event.type == pygame.QUIT:
                pygame.quit()  # Завершаем pygame
                sys.exit()  # Завершаем программу

            # Нажатие клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()  # Закрываем игру по ESC
                    sys.exit()

            # Нажатие кнопок мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    # Проверяем, попал ли клик по кнопке "ИГРАТЬ"
                    if play_button.collidepoint(event.pos):
                        self.game_state = "playing"  # Переходим в игровой режим
                        self.reset_game()  # Сбрасываем игру
                        return True  # Возвращаем True, чтобы указать, что событие обработано
                    # Проверяем, попал ли клик по кнопке "ЗАКРЫТЬ"
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()  # Закрываем игру
                        sys.exit()
                        return True  # Возвращаем True, чтобы указать, что событие обработано

            # Изменение размера окна
            if event.type == pygame.VIDEORESIZE:
                # Обновляем размеры экрана
                self.screen_width, self.screen_height = event.size
                # Изменяем размер окна
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
                # Пересчитываем размеры элементов
                self.calculate_dimensions()
                # Обновляем размеры экрана в UI
                self.ui.screen_width = self.screen_width
                self.ui.screen_height = self.screen_height
                # Обновляем шрифты
                self.ui.update_fonts()

        return False  # Возвращаем False, если событие не обработано

    def handle_game_events(self):
        """Обработка игровых событий"""
        # Обрабатываем все события в очереди
        for event in pygame.event.get():
            # Закрытие окна игры
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Нажатие клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # При нажатии ESC переходим в меню паузы
                    self.game_state = "paused"
                    return True  # Возвращаем True, чтобы указать, что событие обработано

                # Обработка управления во время игры
                if self.game_state == "playing":
                    if event.key == pygame.K_a:
                        self.move(-1, 0)  # Движение влево
                        return True
                    elif event.key == pygame.K_d:
                        self.move(1, 0)  # Движение вправо
                        return True
                    elif event.key == pygame.K_s:
                        self.move(0, 1)  # Ускоренное падение вниз
                        return True
                    elif event.key == pygame.K_w:
                        self.rotate_piece()  # Поворот фигуры
                        return True
                    elif event.key == pygame.K_SPACE:
                        self.hard_drop()  # Мгновенное падение
                        return True

            # Нажатие кнопок мыши
            if event.type == pygame.MOUSEBUTTONDOWN and self.game_state == "paused":
                if event.button == 1:  # Левая кнопка мыши
                    return True  # Возвращаем True, чтобы указать, что событие обработано

            # Изменение размера окна
            if event.type == pygame.VIDEORESIZE:
                # Обновляем размеры экрана
                self.screen_width, self.screen_height = event.size
                # Изменяем размер окна
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
                # Пересчитываем размеры элементов
                self.calculate_dimensions()
                # Обновляем размеры экрана в UI
                self.ui.screen_width = self.screen_width
                self.ui.screen_height = self.screen_height
                # Обновляем шрифты
                self.ui.update_fonts()

        return False  # Возвращаем False, если событие не обработано

    def handle_pause_events(self, resume_button, menu_button):
        """Обработка событий в меню паузы"""
        # Обрабатываем все события в очереди
        for event in pygame.event.get():
            # Закрытие окна игры
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Нажатие клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # При нажатии ESC возвращаемся к игре
                    self.game_state = "playing"
                    return True  # Возвращаем True, чтобы указать, что событие обработано

            # Нажатие кнопок мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    # Проверяем, попал ли клик по кнопке "ПРОДОЛЖИТЬ"
                    if resume_button.collidepoint(event.pos):
                        self.game_state = "playing"  # Возвращаемся к игре
                        return True  # Возвращаем True, чтобы указать, что событие обработано
                    # Проверяем, попал ли клик по кнопке "В МЕНЮ"
                    elif menu_button.collidepoint(event.pos):
                        self.game_state = "menu"  # Переходим в главное меню
                        return True  # Возвращаем True, чтобы указать, что событие обработано

            # Изменение размера окна
            if event.type == pygame.VIDEORESIZE:
                # Обновляем размеры экрана
                self.screen_width, self.screen_height = event.size
                # Изменяем размер окна
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
                # Пересчитываем размеры элементов
                self.calculate_dimensions()
                # Обновляем размеры экрана в UI
                self.ui.screen_width = self.screen_width
                self.ui.screen_height = self.screen_height
                # Обновляем шрифты
                self.ui.update_fonts()

        return False  # Возвращаем False, если событие не обработано

    def handle_game_over_events(self, restart_button, menu_button):
        """Обработка событий на экране окончания игры"""
        # Обрабатываем все события в очереди
        for event in pygame.event.get():
            # Закрытие окна игры
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Нажатие клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = "menu"  # Переход в главное меню по ESC
                    return True  # Возвращаем True, чтобы указать, что событие обработано

            # Нажатие кнопок мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    # Проверяем, попал ли клик по кнопке "ИГРАТЬ СНОВА"
                    if restart_button.collidepoint(event.pos):
                        self.game_state = "playing"  # Новая игра
                        self.reset_game()  # Сброс игры
                        return True  # Возвращаем True, чтобы указать, что событие обработано
                    # Проверяем, попал ли клик по кнопке "В МЕНЮ"
                    elif menu_button.collidepoint(event.pos):
                        self.game_state = "menu"  # Переход в главное меню
                        return True  # Возвращаем True, чтобы указать, что событие обработано

            # Изменение размера окна
            if event.type == pygame.VIDEORESIZE:
                # Обновляем размеры экрана
                self.screen_width, self.screen_height = event.size
                # Изменяем размер окна
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
                # Пересчитываем размеры элементов
                self.calculate_dimensions()
                # Обновляем размеры экрана в UI
                self.ui.screen_width = self.screen_width
                self.ui.screen_height = self.screen_height
                # Обновляем шрифты
                self.ui.update_fonts()

        return False  # Возвращаем False, если событие не обработано

    def update(self):
        """Обновление игровой логики"""
        # Обновляем только во время активной игры
        if self.game_state == "playing":
            # Добавляем время, прошедшее с последнего обновления
            self.fall_time += self.clock.get_time() / 1000  # Преобразуем миллисекунды в секунды

            # Если прошло достаточно времени для падения фигуры
            if self.fall_time >= self.fall_speed:
                self.move(0, 1)  # Перемещаем фигуру вниз
                self.fall_time = 0  # Сбрасываем таймер

    def draw(self):
        """Отрисовка всего экрана"""
        # Заполняем экран черным цветом
        self.screen.fill(BLACK)

        # Отрисовка в зависимости от текущего состояния игры
        if self.game_state == "menu":
            # Отображаем главное меню
            play_button, quit_button = self.ui.draw_menu(self.score)
            pygame.display.flip()  # Обновляем экран
            self.handle_menu_events(play_button, quit_button)  # Обрабатываем события меню

        elif self.game_state == "playing":
            # Отображаем игровой процесс
            self.draw_grid()  # Рисуем игровое поле
            self.draw_current_piece()  # Рисуем текущую фигуру
            self.draw_next_piece()  # Рисуем следующую фигуру
            self.draw_sidebar()  # Рисуем боковую панель
            pygame.display.flip()  # Обновляем экран

        elif self.game_state == "paused":
            # Отображаем меню паузы
            self.draw_grid()  # Рисуем игровое поле
            self.draw_current_piece()  # Рисуем текущую фигуру
            self.draw_next_piece()  # Рисуем следующую фигуру
            self.draw_sidebar()  # Рисуем боковую панель
            resume_button, menu_button = self.ui.draw_pause_menu()  # Рисуем меню паузы
            pygame.display.flip()  # Обновляем экран
            self.handle_pause_events(resume_button, menu_button)  # Обрабатываем события паузы

        elif self.game_state == "game_over":
            # Отображаем экран окончания игры
            self.draw_grid()  # Рисуем игровое поле
            self.draw_current_piece()  # Рисуем текущую фигуру
            self.draw_next_piece()  # Рисуем следующую фигуру
            self.draw_sidebar()  # Рисуем боковую панель
            restart_button, menu_button = self.ui.draw_game_over(
                self.score)  # Рисуем экран окончания игры с текущим счетом
            pygame.display.flip()  # Обновляем экран
            self.handle_game_over_events(restart_button, menu_button)  # Обрабатываем события окончания игры

    def run(self):
        """Основной игровой цикл"""
        # Бесконечный цикл игры
        while True:
            # Пересчитываем размеры элементов при каждом кадре
            self.calculate_dimensions()
            # Обрабатываем игровые события
            self.handle_game_events()
            # Обновляем игровую логику
            self.update()
            # Отрисовываем экран
            self.draw()
            # Ограничиваем частоту кадров до 60 FPS
            self.clock.tick(60)