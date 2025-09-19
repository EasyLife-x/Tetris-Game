# ui.py - Класс для управления интерфейсом пользователя в игре Тетрис

# Импортируем необходимые модули
import pygame
from constants import *  # Импортируем все константы


class UI:
    """Класс для управления интерфейсом пользователя"""

    def __init__(self, screen, screen_width, screen_height):
        """
        Инициализация интерфейса пользователя
        screen: поверхность pygame для отрисовки
        screen_width: ширина экрана
        screen_height: высота экрана
        """
        self.screen = screen  # Поверхность для отрисовки
        self.screen_width = screen_width  # Ширина экрана
        self.screen_height = screen_height  # Высота экрана

        # Создаем шрифты разных размеров с учетом размера экрана
        # max() используется для предотвращения слишком маленьких шрифтов
        self.font = pygame.font.SysFont(None, max(12, int(screen_height * 0.033)))  # Основной шрифт
        self.small_font = pygame.font.SysFont(None, max(10, int(screen_height * 0.026)))  # Маленький шрифт
        self.large_font = pygame.font.SysFont(None, max(24, int(screen_height * 0.067)))  # Большой шрифт

    def update_fonts(self):
        """Обновление размеров шрифтов при изменении размера экрана"""
        # Пересоздаем шрифты с новыми размерами экрана
        self.font = pygame.font.SysFont(None, max(12, int(self.screen_height * 0.033)))
        self.small_font = pygame.font.SysFont(None, max(10, int(self.screen_height * 0.026)))
        self.large_font = pygame.font.SysFont(None, max(24, int(self.screen_height * 0.067)))

    def draw_menu(self):
        """Отрисовка главного меню игры"""
        # Создаем полупрозрачный оверлей для затемнения фона
        overlay = pygame.Surface((self.screen_width, self.screen_height))  # Создаем поверхность размером с экран
        overlay.set_alpha(200)  # Устанавливаем прозрачность (0-255, где 255 - непрозрачный)
        overlay.fill(BLACK)  # Заполняем черным цветом
        self.screen.blit(overlay, (0, 0))  # Отображаем оверлей на экране

        # Отрисовка заголовка игры
        title = self.large_font.render("ТЕТРИС", True, CYAN)  # Создаем текст заголовка синим цветом
        title_rect = title.get_rect(center=(self.screen_width // 2,
                                            self.screen_height // 3))  # Центрируем по горизонтали и размещаем на 1/3 высоты экрана
        self.screen.blit(title, title_rect)  # Отображаем заголовок на экране

        # Параметры кнопок меню
        button_width = 300  # Ширина кнопок
        button_height = 60  # Высота кнопок
        button_y_start = self.screen_height // 2  # Вертикальная позиция первой кнопки

        # Создание и отрисовка кнопки "ИГРАТЬ"
        play_button = pygame.Rect(self.screen_width // 2 - button_width // 2,  # Центрируем по горизонтали
                                  button_y_start,  # Вертикальная позиция
                                  button_width,  # Ширина
                                  button_height)  # Высота
        pygame.draw.rect(self.screen, GREEN, play_button,
                         border_radius=10)  # Рисуем зеленую кнопку с закругленными углами
        pygame.draw.rect(self.screen, WHITE, play_button, 3, border_radius=10)  # Рисуем белую рамку вокруг кнопки
        play_text = self.font.render("ИГРАТЬ", True, BLACK)  # Создаем текст на кнопке черным цветом
        play_text_rect = play_text.get_rect(center=play_button.center)  # Центрируем текст внутри кнопки
        self.screen.blit(play_text, play_text_rect)  # Отображаем текст на кнопке

        # Создание и отрисовка кнопки "ЗАКРЫТЬ"
        quit_button = pygame.Rect(self.screen_width // 2 - button_width // 2,  # Центрируем по горизонтали
                                  button_y_start + 100,  # Размещаем ниже первой кнопки
                                  button_width,  # Ширина
                                  button_height)  # Высота
        pygame.draw.rect(self.screen, RED, quit_button,
                         border_radius=10)  # Рисуем красную кнопку с закругленными углами
        pygame.draw.rect(self.screen, WHITE, quit_button, 3, border_radius=10)  # Рисуем белую рамку вокруг кнопки
        quit_text = self.font.render("ЗАКРЫТЬ", True, WHITE)  # Создаем текст на кнопке белым цветом
        quit_text_rect = quit_text.get_rect(center=quit_button.center)  # Центрируем текст внутри кнопки
        self.screen.blit(quit_text, quit_text_rect)  # Отображаем текст на кнопке

        return play_button, quit_button  # Возвращаем обе кнопки для обработки событий

    def draw_pause_menu(self):
        """Отрисовка меню паузы"""
        # Создаем полупрозрачный оверлей для затемнения фона
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Отрисовка надписи "ПАУЗА"
        pause_text = self.large_font.render("ПАУЗА", True, YELLOW)  # Создаем текст желтым цветом
        pause_rect = pause_text.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
        self.screen.blit(pause_text, pause_rect)

        # Параметры кнопок меню паузы
        button_width = 300
        button_height = 60
        button_y_start = self.screen_height // 2

        # Создание и отрисовка кнопки "ПРОДОЛЖИТЬ"
        resume_button = pygame.Rect(self.screen_width // 2 - button_width // 2,
                                    button_y_start,
                                    button_width,
                                    button_height)
        pygame.draw.rect(self.screen, GREEN, resume_button, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, resume_button, 3, border_radius=10)
        resume_text = self.font.render("ПРОДОЛЖИТЬ", True, BLACK)
        resume_text_rect = resume_text.get_rect(center=resume_button.center)
        self.screen.blit(resume_text, resume_text_rect)

        # Создание и отрисовка кнопки "В МЕНЮ"
        menu_button = pygame.Rect(self.screen_width // 2 - button_width // 2,
                                  button_y_start + 100,
                                  button_width,
                                  button_height)
        pygame.draw.rect(self.screen, BLUE, menu_button, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, menu_button, 3, border_radius=10)
        menu_text = self.font.render("В МЕНЮ", True, WHITE)
        menu_text_rect = menu_text.get_rect(center=menu_button.center)
        self.screen.blit(menu_text, menu_text_rect)

        return resume_button, menu_button  # Возвращаем кнопки для обработки событий

    def draw_game_over(self):
        """Отрисовка экрана окончания игры"""
        # Создаем полупрозрачный оверлей для затемнения фона
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Отрисовка надписи "ИГРА ОКОНЧЕНА"
        game_over_text = self.large_font.render("ИГРА ОКОНЧЕНА", True, RED)  # Создаем текст красным цветом
        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
        self.screen.blit(game_over_text, game_over_rect)

        # Отрисовка счета игрока
        # Проверяем наличие атрибута score, если его нет - используем 0
        score_text = self.font.render(f"Счет: {self.score if hasattr(self, 'score') else 0}", True, WHITE)
        score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(score_text, score_rect)

        # Параметры кнопок экрана окончания игры
        button_width = 300
        button_height = 60
        button_y_start = self.screen_height // 2 + 100

        # Создание и отрисовка кнопки "ИГРАТЬ СНОВА"
        restart_button = pygame.Rect(self.screen_width // 2 - button_width // 2,
                                     button_y_start,
                                     button_width,
                                     button_height)
        pygame.draw.rect(self.screen, GREEN, restart_button, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, restart_button, 3, border_radius=10)
        restart_text = self.font.render("ИГРАТЬ СНОВА", True, BLACK)
        restart_text_rect = restart_text.get_rect(center=restart_button.center)
        self.screen.blit(restart_text, restart_text_rect)

        # Создание и отрисовка кнопки "В МЕНЮ"
        menu_button = pygame.Rect(self.screen_width // 2 - button_width // 2,
                                  button_y_start + 100,
                                  button_width,
                                  button_height)
        pygame.draw.rect(self.screen, BLUE, menu_button, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, menu_button, 3, border_radius=10)
        menu_text = self.font.render("В МЕНЮ", True, WHITE)
        menu_text_rect = menu_text.get_rect(center=menu_button.center)
        self.screen.blit(menu_text, menu_text_rect)

        return restart_button, menu_button  # Возвращаем кнопки для обработки событий