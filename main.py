"""
Tetris для Android
Полностью рабочий код для сборки APK
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
import random

# Настройки окна
Window.size = (400, 600)
Window.clearcolor = (0, 0, 0, 1)

# Константы игры
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Цвета фигур (RGB формат для Kivy - значения от 0 до 1)
COLORS = {
    0: (0.1, 0.1, 0.1, 1),   # пустота
    1: (0, 1, 1, 1),         # Cyan
    2: (1, 1, 0, 1),         # Yellow
    3: (0.6, 0, 0.8, 1),     # Purple
    4: (0, 1, 0, 1),         # Green
    5: (1, 0, 0, 1),         # Red
    6: (0, 0, 1, 1),         # Blue
    7: (1, 0.5, 0, 1),       # Orange
}

# Формы тетрамино
SHAPES = [
    [[1, 1, 1, 1]],                    # I
    [[1, 1], [1, 1]],                  # O
    [[0, 1, 0], [1, 1, 1]],            # T
    [[1, 0, 0], [1, 1, 1]],            # L
    [[0, 0, 1], [1, 1, 1]],            # J
    [[0, 1, 1], [1, 1, 0]],            # S
    [[1, 1, 0], [0, 1, 1]],            # Z
]

# Цвет каждой фигуры (по порядку SHAPES)
SHAPE_COLORS = [1, 2, 3, 4, 7, 6, 5]


class GameArea(Widget):
    """Игровое поле"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE)
        self.pos = (50, 50)
        
        # Сетка игры (0 - пусто, иначе номер цвета)
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        
        # Визуальные блоки
        self.blocks = {}
        
        # Игровые переменные
        self.current_piece = None
        self.current_color = None
        self.current_x = 0
        self.current_y = 0
        self.score = 0
        self.game_over = False
        
        # Следующая фигура
        self.next_piece = None
        self.next_color = None
        
        # Создаем сетку блоков
        self.create_grid()
        
        # Запускаем игру
        self.start_new_game()
        
        # Таймер падения
        Clock.schedule_interval(self.fall, 0.5)
    
    def create_grid(self):
        """Создает визуальную сетку из блоков"""
        with self.canvas:
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    color = COLORS[0]
                    Color(*color)
                    rect = Rectangle(
                        pos=(self.x + x * BLOCK_SIZE, self.y + y * BLOCK_SIZE),
                        size=(BLOCK_SIZE - 1, BLOCK_SIZE - 1)
                    )
                    self.blocks[(x, y)] = rect
    
    def start_new_game(self):
        """Начинает новую игру"""
        # Очищаем сетку
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.game_over = False
        
        # Обновляем визуальные блоки
        self.update_grid_display()
        
        # Создаем первую фигуру
        self.next_piece = None
        self.create_new_piece()
    
    def create_new_piece(self):
        """Создает новую фигуру"""
        if self.next_piece is None:
            # Первая фигура
            idx = random.randint(0, len(SHAPES) - 1)
            self.next_piece = SHAPES[idx]
            self.next_color = SHAPE_COLORS[idx]
        
        # Текущая фигура = следующая
        self.current_piece = [row[:] for row in self.next_piece]
        self.current_color = self.next_color
        
        # Создаем следующую фигуру
        idx = random.randint(0, len(SHAPES) - 1)
        self.next_piece = SHAPES[idx]
        self.next_color = SHAPE_COLORS[idx]
        
        # Начальная позиция
        self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0
        
        # Проверяем, не проиграли ли
        if not self.can_move(0, 0, self.current_piece):
            self.game_over = True
            return False
        
        self.update_display()
        return True
    
    def can_move(self, dx, dy, piece=None):
        """Проверяет, может ли фигура двигаться"""
        if piece is None:
            piece = self.current_piece
        
        for i, row in enumerate(piece):
            for j, val in enumerate(row):
                if val:
                    new_x = self.current_x + j + dx
                    new_y = self.current_y + i + dy
                    
                    if new_x < 0 or new_x >= GRID_WIDTH:
                        return False
                    if new_y >= GRID_HEIGHT:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x] != 0:
                        return False
        return True
    
    def fall(self, dt):
        """Автоматическое падение"""
        if not self.game_over:
            if self.can_move(0, 1):
                self.current_y += 1
                self.update_display()
            else:
                self.merge_piece()
    
    def merge_piece(self):
        """Закрепляет фигуру на поле"""
        for i, row in enumerate(self.current_piece):
            for j, val in enumerate(row):
                if val:
                    x = self.current_x + j
                    y = self.current_y + i
                    if y >= 0:
                        self.grid[y][x] = self.current_color
        
        # Проверяем заполненные линии
        self.clear_lines()
        
        # Создаем новую фигуру
        success = self.create_new_piece()
        
        if not success:
            self.game_over = True
        
        self.update_grid_display()
    
    def clear_lines(self):
        """Удаляет заполненные строки и начисляет очки"""
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        
        while y >= 0:
            if all(self.grid[y]):
                # Удаляем строку
                del self.grid[y]
                self.grid.insert(0, [0] * GRID_WIDTH)
                lines_cleared += 1
                # Проверяем ту же позицию снова
            else:
                y -= 1
        
        # Начисляем очки
        if lines_cleared > 0:
            points = [0, 100, 300, 500, 800]
            self.score += points[min(lines_cleared, 4)]
        
        if self.parent:
            self.parent.update_score(self.score)
    
    def update_grid_display(self):
        """Обновляет цвета всех блоков на поле"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color_id = self.grid[y][x]
                color = COLORS[color_id]
                self.blocks[(x, y)].color = color
    
    def update_display(self):
        """Обновляет отображение (поле + текущая фигура)"""
        # Сначала обновляем поле
        self.update_grid_display()
        
        # Рисуем текущую фигуру поверх
        if not self.game_over and self.current_piece:
            for i, row in enumerate(self.current_piece):
                for j, val in enumerate(row):
                    if val:
                        x = self.current_x + j
                        y = self.current_y + i
                        if y >= 0 and y < GRID_HEIGHT and x >= 0 and x < GRID_WIDTH:
                            color = COLORS[self.current_color]
                            self.blocks[(x, y)].color = color
    
    def move_left(self):
        """Движение влево"""
        if not self.game_over:
            if self.can_move(-1, 0):
                self.current_x -= 1
                self.update_display()
    
    def move_right(self):
        """Движение вправо"""
        if not self.game_over:
            if self.can_move(1, 0):
                self.current_x += 1
                self.update_display()
    
    def rotate(self):
        """Поворот фигуры"""
        if not self.game_over:
            rotated = [list(row) for row in zip(*self.current_piece[::-1])]
            if self.can_move(0, 0, rotated):
                self.current_piece = rotated
                self.update_display()
    
    def hard_drop(self):
        """Мгновенное падение"""
        if not self.game_over:
            while self.can_move(0, 1):
                self.current_y += 1
            self.merge_piece()
            self.update_display()
    
    def on_touch_down(self, touch):
        """Обработка касаний"""
        if self.game_over:
            self.start_new_game()
            return
        
        # Разделяем экран на зоны
        screen_center = self.parent.width / 2 if self.parent else 200
        
        if touch.x < screen_center - 100:
            # Левая часть - поворот
            self.rotate()
        elif touch.x > screen_center + 100:
            # Правая часть - хард дроп
            self.hard_drop()
        else:
            # Центр - пауза или движение вниз
            self.fall(0)


class NextPieceDisplay(Widget):
    """Отображение следующей фигуры"""
    
    def __init__(self, game_area, **kwargs):
        super().__init__(**kwargs)
        self.game_area = game_area
        self.size = (120, 120)
        self.pos = (280, 400)
        self.blocks = []
        
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(pos=self.pos, size=self.size)
    
    def update(self):
        """Обновляет отображение следующей фигуры"""
        # Очищаем старые блоки
        for rect in self.blocks:
            self.canvas.remove(rect)
        self.blocks.clear()
        
        if not self.game_area.next_piece:
            return
        
        piece = self.game_area.next_piece
        color = COLORS[self.game_area.next_color]
        block_size = 25
        
        # Вычисляем позицию для центрирования
        cols = len(piece[0])
        rows = len(piece)
        start_x = self.pos[0] + (120 - cols * block_size) // 2
        start_y = self.pos[1] + (120 - rows * block_size) // 2
        
        for i, row in enumerate(piece):
            for j, val in enumerate(row):
                if val:
                    with self.canvas:
                        Color(*color)
                        rect = Rectangle(
                            pos=(start_x + j * block_size, start_y + i * block_size),
                            size=(block_size - 1, block_size - 1)
                        )
                        self.blocks.append(rect)


class TetrisGame(BoxLayout):
    """Главный виджет игры"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        
        # Игровое поле
        self.game_area = GameArea()
        
        # Правая панель
        right_panel = BoxLayout(orientation='vertical', size_hint=(0.4, 1), spacing=10)
        
        # Заголовок
        right_panel.add_widget(Label(text="TETRIS", font_size=24, color=(0, 1, 1, 1)))
        
        # Счет
        self.score_label = Label(text="Score: 0", font_size=20, color=(1, 1, 1, 1))
        right_panel.add_widget(self.score_label)
        
        # Отображение следующей фигуры
        right_panel.add_widget(Label(text="Next:", font_size=16, color=(0.7, 0.7, 0.7, 1)))
        self.next_display = NextPieceDisplay(self.game_area)
        right_panel.add_widget(self.next_display)
        
        # Кнопки управления
        btn_layout = GridLayout(cols=2, spacing=5, size_hint=(1, None), height=200)
        
        btn_left = Button(text="←", background_color=(0.3, 0.3, 0.5, 1))
        btn_left.bind(on_press=lambda x: self.game_area.move_left())
        btn_layout.add_widget(btn_left)
        
        btn_right = Button(text="→", background_color=(0.3, 0.3, 0.5, 1))
        btn_right.bind(on_press=lambda x: self.game_area.move_right())
        btn_layout.add_widget(btn_right)
        
        btn_rotate = Button(text="↻", background_color=(0.5, 0.3, 0.5, 1))
        btn_rotate.bind(on_press=lambda x: self.game_area.rotate())
        btn_layout.add_widget(btn_rotate)
        
        btn_drop = Button(text="⬇⬇", background_color=(0.5, 0.3, 0.3, 1))
        btn_drop.bind(on_press=lambda x: self.game_area.hard_drop())
        btn_layout.add_widget(btn_drop)
        
        btn_new = Button(text="New", background_color=(0.2, 0.6, 0.2, 1))
        btn_new.bind(on_press=lambda x: self.game_area.start_new_game())
        btn_layout.add_widget(btn_new)
        
        right_panel.add_widget(btn_layout)
        
        # Добавляем всё на экран
        self.add_widget(self.game_area)
        self.add_widget(right_panel)
        
        # Запускаем обновление следующей фигуры
        Clock.schedule_interval(self.update_next_display, 0.1)
    
    def update_score(self, score):
        """Обновляет отображение счета"""
        self.score_label.text = f"Score: {score}"
    
    def update_next_display(self, dt):
        """Обновляет отображение следующей фигуры"""
        self.next_display.update()


class TetrisApp(App):
    """Главное приложение"""
    
    def build(self):
        self.title = "Tetris - Neon Blocks"
        return TetrisGame()


if __name__ == "__main__":
    TetrisApp().run()
