# particle.py - Система частиц для эффектов

import pygame
import random
import math


class Particle:
    """Класс для одной частицы"""

    def __init__(self, x, y, color):
        """Инициализация частицы"""
        self.x = x
        self.y = y
        # Убедимся, что цвет в правильном формате (RGB)
        if isinstance(color, tuple) and len(color) >= 3:
            self.color = color[:3]  # Берем только RGB компоненты
        else:
            self.color = (255, 255, 255)  # Белый по умолчанию
        self.size = random.randint(2, 6)
        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-3, 3)
        self.life = random.randint(20, 40)  # Время жизни в кадрах
        self.max_life = self.life
        self.gravity = 0.1

    def update(self):
        """Обновление частицы"""
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += self.gravity
        self.life -= 1

        # Замедление
        self.speed_x *= 0.98
        self.speed_y *= 0.98

    def draw(self, screen):
        """Отрисовка частицы"""
        if self.life > 0:
            # Изменяем прозрачность в зависимости от времени жизни
            alpha = int(255 * (self.life / self.max_life))

            # Создаем цвет с альфа-каналом правильно
            if len(self.color) >= 3:
                color_with_alpha = (self.color[0], self.color[1], self.color[2], alpha)
            else:
                color_with_alpha = (255, 255, 255, alpha)

            # Создаем временную поверхность для частицы с прозрачностью
            temp_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)

            # Рисуем круг на временной поверхности (без альфа-канала в цвете)
            pygame.draw.circle(temp_surface, self.color, (self.size, self.size), self.size)

            # Устанавливаем прозрачность всей поверхности
            temp_surface.set_alpha(alpha)

            # Отображаем поверхность на экране
            screen.blit(temp_surface, (int(self.x - self.size), int(self.y - self.size)))

    def is_alive(self):
        """Проверка, жива ли частица"""
        return self.life > 0


class ParticleSystem:
    """Система частиц для создания эффектов"""

    def __init__(self):
        """Инициализация системы частиц"""
        self.particles = []

    def add_particles(self, x, y, color, count=10):
        """Добавление частиц в систему"""
        # Извлекаем основной цвет из цветовой схемы тетрамино
        if isinstance(color, tuple) and len(color) == 2:
            main_color = color[0]  # Берем основной цвет
        elif isinstance(color, tuple):
            main_color = color
        else:
            main_color = (255, 255, 255)

        for _ in range(count):
            self.particles.append(Particle(x, y, main_color))

    def add_line_clear_effect(self, x, y, color):
        """Добавление эффекта очистки линии"""
        # Извлекаем основной цвет из цветовой схемы тетрамино
        if isinstance(color, tuple) and len(color) == 2:
            main_color = color[0]  # Берем основной цвет
        elif isinstance(color, tuple):
            main_color = color
        else:
            main_color = (255, 255, 255)

        # Создаем больше частиц для эффекта очистки линии
        for _ in range(30):
            particle = Particle(x + random.randint(-50, 50), y, main_color)
            # Частицы разлетаются в стороны
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 5)
            particle.speed_x = math.cos(angle) * speed
            particle.speed_y = math.sin(angle) * speed
            particle.life = random.randint(30, 60)
            self.particles.append(particle)

    def update(self):
        """Обновление всех частиц"""
        # Обновляем все частицы
        for particle in self.particles:
            particle.update()

        # Удаляем мертвые частицы
        self.particles = [p for p in self.particles if p.is_alive()]

    def draw(self, screen):
        """Отрисовка всех частиц"""
        for particle in self.particles:
            particle.draw(screen)