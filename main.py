"""
Tetris for Android - Kivy Version
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

Window.size = (360, 640)
Window.clearcolor = (0, 0, 0, 1)

BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

COLORS = {
    0: (0.1, 0.1, 0.1, 1),
    1: (0, 1, 1, 1),      # Cyan
    2: (1, 1, 0, 1),      # Yellow
    3: (0.6, 0, 0.8, 1),  # Purple
    4: (0, 1, 0, 1),      # Green
    5: (1, 0, 0, 1),      # Red
    6: (0, 0, 1, 1),      # Blue
    7: (1, 0.5, 0, 1),    # Orange
}

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
]

SHAPE_COLORS = [1, 2, 3, 4, 7, 6, 5]


class GameArea(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE)
        self.pos = (20, 50)
        
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.blocks = {}
        
        self.current_piece = None
        self.current_color = None
        self.current_x = 0
        self.current_y = 0
        self.score = 0
        self.game_over = False
        self.next_piece = None
        self.next_color = None
        
        self.create_grid()
        self.start_new_game()
        Clock.schedule_interval(self.fall, 0.5)
    
    def create_grid(self):
        with self.canvas:
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    self.blocks[(x, y)] = Rectangle(
                        pos=(self.x + x * BLOCK_SIZE, self.y + y * BLOCK_SIZE),
                        size=(BLOCK_SIZE - 1, BLOCK_SIZE - 1)
                    )
                    self.blocks[(x, y)].color = COLORS[0]
    
    def start_new_game(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.game_over = False
        self.next_piece = None
        self.update_grid_display()
        self.create_new_piece()
    
    def create_new_piece(self):
        if self.next_piece is None:
            idx = random.randint(0, len(SHAPES) - 1)
            self.next_piece = SHAPES[idx]
            self.next_color = SHAPE_COLORS[idx]
        
        self.current_piece = [row[:] for row in self.next_piece]
        self.current_color = self.next_color
        
        idx = random.randint(0, len(SHAPES) - 1)
        self.next_piece = SHAPES[idx]
        self.next_color = SHAPE_COLORS[idx]
        
        self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0
        
        if not self.can_move(0, 0):
            self.game_over = True
            return False
        
        self.update_display()
        return True
    
    def can_move(self, dx, dy, piece=None):
        if piece is None:
            piece = self.current_piece
        for i, row in enumerate(piece):
            for j, val in enumerate(row):
                if val:
                    new_x = self.current_x + j + dx
                    new_y = self.current_y + i + dy
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x] != 0:
                        return False
        return True
    
    def fall(self, dt):
        if not self.game_over:
            if self.can_move(0, 1):
                self.current_y += 1
                self.update_display()
            else:
                self.merge_piece()
    
    def merge_piece(self):
        for i, row in enumerate(self.current_piece):
            for j, val in enumerate(row):
                if val:
                    x = self.current_x + j
                    y = self.current_y + i
                    if y >= 0:
                        self.grid[y][x] = self.current_color
        
        self.clear_lines()
        self.create_new_piece()
        self.update_grid_display()
    
    def clear_lines(self):
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0] * GRID_WIDTH)
                lines_cleared += 1
            else:
                y -= 1
        
        if lines_cleared > 0:
            points = [0, 100, 300, 500, 800]
            self.score += points[min(lines_cleared, 4)]
        
        if self.parent:
            self.parent.update_score(self.score)
    
    def update_grid_display(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color_id = self.grid[y][x]
                self.blocks[(x, y)].color = COLORS[color_id]
    
    def update_display(self):
        self.update_grid_display()
        if not self.game_over and self.current_piece:
            for i, row in enumerate(self.current_piece):
                for j, val in enumerate(row):
                    if val:
                        x = self.current_x + j
                        y = self.current_y + i
                        if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
                            self.blocks[(x, y)].color = COLORS[self.current_color]
    
    def move_left(self):
        if not self.game_over and self.can_move(-1, 0):
            self.current_x -= 1
            self.update_display()
    
    def move_right(self):
        if not self.game_over and self.can_move(1, 0):
            self.current_x += 1
            self.update_display()
    
    def rotate(self):
        if not self.game_over:
            rotated = [list(row) for row in zip(*self.current_piece[::-1])]
            if self.can_move(0, 0, rotated):
                self.current_piece = rotated
                self.update_display()
    
    def hard_drop(self):
        if not self.game_over:
            while self.can_move(0, 1):
                self.current_y += 1
            self.merge_piece()
            self.update_display()


class TetrisGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        
        self.game_area = GameArea()
        
        right_panel = BoxLayout(orientation='vertical', size_hint=(0.35, 1))
        
        right_panel.add_widget(Label(text="TETRIS", font_size=28, color=(0, 1, 1, 1)))
        
        self.score_label = Label(text="Score: 0", font_size=20, color=(1, 1, 1, 1))
        right_panel.add_widget(self.score_label)
        
        btn_layout = GridLayout(cols=2, spacing=5, size_hint=(1, None), height=250, pos_hint={'top': 0.5})
        
        btn_left = Button(text="←", background_color=(0.3, 0.3, 0.5, 1))
        btn_left.bind(on_press=lambda x: self.game_area.move_left())
        btn_layout.add_widget(btn_left)
        
        btn_right = Button(text="→", background_color=(0.3, 0.3, 0.5, 1))
        btn_right.bind(on_press=lambda x: self.game_area.move_right())
        btn_layout.add_widget(btn_right)
        
        btn_rotate = Button(text="↻", background_color=(0.5, 0.3, 0.5, 1))
        btn_rotate.bind(on_press=lambda x: self.game_area.rotate())
        btn_layout.add_widget(btn_rotate)
        
        btn_drop = Button(text="⬇", background_color=(0.5, 0.3, 0.3, 1))
        btn_drop.bind(on_press=lambda x: self.game_area.hard_drop())
        btn_layout.add_widget(btn_drop)
        
        btn_new = Button(text="New", background_color=(0.2, 0.6, 0.2, 1))
        btn_new.bind(on_press=lambda x: self.game_area.start_new_game())
        btn_layout.add_widget(btn_new)
        
        right_panel.add_widget(btn_layout)
        
        self.add_widget(self.game_area)
        self.add_widget(right_panel)
    
    def update_score(self, score):
        self.score_label.text = f"Score: {score}"


class TetrisApp(App):
    def build(self):
        self.title = "Tetris"
        return TetrisGame()


if __name__ == "__main__":
    TetrisApp().run()
