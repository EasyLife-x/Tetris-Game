# sound_manager.py - Менеджер звуков для игры

import pygame
import math


class SoundManager:
    """Класс для управления звуками в игре"""

    def __init__(self):
        """Инициализация менеджера звуков"""
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        """Загрузка звуков"""
        try:
            # Создаем простые синтезированные звуки
            self.sounds['line_clear'] = self.create_tone_sound(440, 0.3)  # Звук очистки линии
            self.sounds['rotate'] = self.create_tone_sound(880, 0.1)  # Звук поворота
            self.sounds['move'] = self.create_click_sound()  # Звук перемещения
            self.sounds['drop'] = self.create_bass_sound()  # Звук падения
        except Exception as e:
            print(f"Ошибка при создании звуков: {e}")

    def create_tone_sound(self, frequency: int, duration: float) -> pygame.mixer.Sound:
        """Создание тона заданной частоты и длительности"""
        try:
            sample_rate = 22050
            frames = int(duration * sample_rate)
            samples = []
            for i in range(frames):
                # Создаем синусоидальную волну
                t = i / sample_rate
                value = int(4096 * math.sin(2 * math.pi * frequency * t))
                # Стерео звук - повторяем значение для левого и правого канала
                samples.append(value)
                samples.append(value)

            # Преобразуем в байты
            sound_bytes = b''.join(
                [value.to_bytes(2, byteorder='little', signed=True) for value in samples]
            )

            # Создаем звук из байтов
            return pygame.mixer.Sound(buffer=sound_bytes)
        except Exception as e:
            print(f"Ошибка создания тона: {e}")
            # Если не удалось создать звук, возвращаем пустой звук
            return pygame.mixer.Sound(buffer=bytes([0] * 44))

    def create_click_sound(self) -> pygame.mixer.Sound:
        """Создание звука щелчка"""
        try:
            sample_rate = 22050
            duration = 0.05
            frames = int(duration * sample_rate)
            samples = []
            for i in range(frames):
                value = int(8192 * (1 - i / frames))  # Затухающий звук
                # Стерео звук
                samples.append(value)
                samples.append(value)

            # Преобразуем в байты
            sound_bytes = b''.join(
                [value.to_bytes(2, byteorder='little', signed=True) for value in samples]
            )

            return pygame.mixer.Sound(buffer=sound_bytes)
        except Exception as e:
            print(f"Ошибка создания щелчка: {e}")
            return pygame.mixer.Sound(buffer=bytes([0] * 44))

    def create_bass_sound(self) -> pygame.mixer.Sound:
        """Создание басового звука"""
        try:
            sample_rate = 22050
            duration = 0.2
            frames = int(duration * sample_rate)
            samples = []
            for i in range(frames):
                # Комбинированный звук
                t = i / sample_rate
                # Используем math для тригонометрических функций
                sin_value1 = math.sin(110 * 2 * math.pi * t)
                exp_value1 = math.exp(-t * 8) if t * 8 < 100 else 0  # Защита от переполнения
                sin_value2 = math.sin(220 * 2 * math.pi * t)
                exp_value2 = math.exp(-t * 5) if t * 5 < 100 else 0  # Защита от переполнения

                value = int(4096 * (
                        sin_value1 * exp_value1 +
                        0.5 * sin_value2 * exp_value2
                ))
                # Стерео звук
                samples.append(value)
                samples.append(value)

            # Преобразуем в байты
            sound_bytes = b''.join(
                [value.to_bytes(2, byteorder='little', signed=True) for value in samples]
            )

            return pygame.mixer.Sound(buffer=sound_bytes)
        except Exception as e:
            print(f"Ошибка создания баса: {e}")
            return pygame.mixer.Sound(buffer=bytes([0] * 44))

    def play_sound(self, sound_name: str):
        """Воспроизведение звука"""
        try:
            if sound_name in self.sounds:
                # Проверяем, что звук существует и не None
                if self.sounds[sound_name] is not None:
                    self.sounds[sound_name].play()
        except Exception as e:
            print(f"Ошибка воспроизведения звука {sound_name}: {e}")