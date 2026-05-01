import pygame
import random
import os

pygame.init()

# ===== AUDIO SAFE INIT =====
audio_enabled = True
try:
    pygame.mixer.init()
except:
    audio_enabled = False

# ===== SCREEN =====
WIDTH, HEIGHT = 300, 600
BLOCK = 30
GRID_W = WIDTH // BLOCK
GRID_H = HEIGHT // BLOCK
SIDE = 180

BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (60,60,60)

COLORS = [
    (0,255,255),
    (255,255,0),
    (160,0,200),
    (0,255,0),
    (255,0,0),
    (0,0,255),
    (255,165,0)
]

SHAPES = [
    [[1,1,1,1]],
    [[1,1],[1,1]],
    [[0,1,0],[1,1,1]],
    [[1,0,0],[1,1,1]],
    [[0,0,1],[1,1,1]],
    [[0,1,1],[1,1,0]],
    [[1,1,0],[0,1,1]]
]


class Tetris:

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH+SIDE, HEIGHT))
        pygame.display.set_caption("Neon Blocks Mobile")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.big = pygame.font.SysFont("Arial", 40)

        self.load_audio()
        self.reset()

        # touch
        self.touch_start = None
        self.hold_time = 0

    # ===== AUDIO =====
    def load_audio(self):
        self.sounds = {}

        if not audio_enabled:
            return

        def load(name):
            path = os.path.join("sounds", name)
            return pygame.mixer.Sound(path) if os.path.exists(path) else None

        self.sounds = {
            "move": load("move.wav"),
            "rotate": load("rotate.wav"),
            "drop": load("drop.wav"),
            "line": load("line.wav"),
            "gameover": load("gameover.wav")
        }

        music = os.path.join("sounds", "music.mp3")
        if os.path.exists(music) and audio_enabled:
            pygame.mixer.music.load(music)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)

    def play(self, name):
        if audio_enabled and self.sounds.get(name):
            self.sounds[name].play()

    # ===== GAME =====
    def reset(self):
        self.grid = [[0]*GRID_W for _ in range(GRID_H)]
        self.cur = self.new_piece()
        self.next = self.new_piece()

        self.score = 0
        self.game_over = False

        self.fall_time = 0
        self.speed = 500

        if audio_enabled:
            pygame.mixer.music.play(-1)

    def new_piece(self):
        i = random.randint(0, len(SHAPES)-1)
        shape = [row[:] for row in SHAPES[i]]
        return {
            "shape": shape,
            "color": COLORS[i],
            "x": GRID_W//2 - len(shape[0])//2,
            "y": 0
        }

    def valid(self, p, dx, dy):
        for i,row in enumerate(p["shape"]):
            for j,v in enumerate(row):
                if v:
                    x = p["x"]+j+dx
                    y = p["y"]+i+dy
                    if x < 0 or x >= GRID_W or y >= GRID_H:
                        return False
                    if y >= 0 and self.grid[y][x]:
                        return False
        return True

    def rotate(self, p):
        return [list(row) for row in zip(*p["shape"][::-1])]

    def merge(self):
        for i,row in enumerate(self.cur["shape"]):
            for j,v in enumerate(row):
                if v:
                    x = self.cur["x"]+j
                    y = self.cur["y"]+i
                    if y >= 0:
                        self.grid[y][x] = self.cur["color"]

        self.clear_lines()

        self.cur = self.next
        self.next = self.new_piece()

        if not self.valid(self.cur,0,0):
            self.game_over = True
            self.play("gameover")
            pygame.mixer.music.stop()

    def clear_lines(self):
        new_grid = []
        lines = 0

        for row in self.grid:
            if all(row):
                lines += 1
            else:
                new_grid.append(row)

        for _ in range(lines):
            new_grid.insert(0, [0]*GRID_W)

        self.grid = new_grid
        self.score += lines * 100

    # ===== INPUT (MOBILE) =====
    def handle_touch(self, e):
        if e.type == pygame.FINGERDOWN:
            self.touch_start = (e.x, e.y)
            self.hold_time = pygame.time.get_ticks()

        elif e.type == pygame.FINGERUP and self.touch_start:
            x0,y0 = self.touch_start
            x1,y1 = e.x,e.y

            dx = x1 - x0
            dy = y1 - y0

            if self.game_over:
                return

            # TAP = rotate
            if abs(dx) < 0.05 and abs(dy) < 0.05:
                r = self.rotate(self.cur)
                old = self.cur["shape"]
                self.cur["shape"] = r
                if not self.valid(self.cur,0,0):
                    self.cur["shape"] = old
                else:
                    self.play("rotate")

            # LEFT
            elif dx < -0.1:
                if self.valid(self.cur,-1,0):
                    self.cur["x"] -= 1
                    self.play("move")

            # RIGHT
            elif dx > 0.1:
                if self.valid(self.cur,1,0):
                    self.cur["x"] += 1
                    self.play("move")

            # DOWN = drop
            elif dy > 0.1:
                while self.valid(self.cur,0,1):
                    self.cur["y"] += 1
                self.play("drop")
                self.merge()

            self.touch_start = None

    # ===== DRAW =====
    def draw(self):
        self.screen.fill(BLACK)

        for y in range(GRID_H):
            for x in range(GRID_W):
                if self.grid[y][x]:
                    pygame.draw.rect(
                        self.screen,
                        self.grid[y][x],
                        (x*BLOCK,y*BLOCK,BLOCK,BLOCK)
                    )

        for i,row in enumerate(self.cur["shape"]):
            for j,v in enumerate(row):
                if v:
                    x = (self.cur["x"]+j)*BLOCK
                    y = (self.cur["y"]+i)*BLOCK
                    pygame.draw.rect(self.screen,self.cur["color"],(x,y,BLOCK,BLOCK))

        txt = self.font.render(f"Score: {self.score}",True,WHITE)
        self.screen.blit(txt,(WIDTH+20,40))

        if self.game_over:
            t = self.big.render("GAME OVER",True,(255,0,0))
            self.screen.blit(t,t.get_rect(center=(WIDTH//2,HEIGHT//2)))

    # ===== LOOP =====
    def run(self):
        running = True

        while running:
            now = pygame.time.get_ticks()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

                self.handle_touch(e)

            # auto fall
            if not self.game_over:
                if now - self.fall_time > self.speed:
                    if self.valid(self.cur,0,1):
                        self.cur["y"] += 1
                    else:
                        self.merge()
                    self.fall_time = now

            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    Tetris().run()