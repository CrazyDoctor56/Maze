import pygame

pygame.init()
pygame.mixer.init()
pygame.font.init()

# SETTING
HEIGHT = 700
WIDTH = 1200
FPS = 60

# COLOR
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# FONT
f1 = pygame.font.Font(None, 70).render("Game Over", True, RED)
f2 = pygame.font.Font(None, 70).render("You Win", True, GREEN)

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze")

clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load("background.jpg"),
             (WIDTH, HEIGHT))

pygame.mixer.music.load("jungles.ogg")
pygame.mixer.music.play()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename: str, size: tuple[int, int], coords: tuple[int, int], speed: int):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(filename), size)
        self.rect = self.image.get_rect(center=coords)
        self.speed = speed

    def reset(self, sc: pygame.Surface):
        sc.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self, walls):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a] and self.rect.left > 0:
            dx = -self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            dx = self.speed
        if keys[pygame.K_w] and self.rect.top > 0:
            dy = -self.speed
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            dy = self.speed
        
        new_rect = self.rect.move(dx, dy)
        if not any(new_rect.colliderect(w.rect) for w in walls):
            self.rect = new_rect

class Enemy(GameSprite):
    def update(self, x1: int, x2: int):
        self.rect.x += self.speed
        if self.rect.x >= x1 or self.rect.x <= x2:
            self.speed *= -1

    def update_vertical(self, y1: int, y2: int):
        self.rect.y += self.speed
        if self.rect.y >= y1 or self.rect.y <= y2:
            self.speed *= -1

class Wall():
    def __init__(self, coords: tuple[int, int], size: tuple[int, int], color: tuple[int, int, int]):
        self.rect = pygame.Rect(coords, size)
        self.color = color

    def draw(self, sc: pygame.Surface):
        pygame.draw.rect(sc, self.color, self.rect)

# Create walls
walls = [
    Wall((0, 0), (WIDTH, 10), GREEN),
    Wall((0, 0), (10, HEIGHT), GREEN),
    Wall((0, HEIGHT - 10), (WIDTH, 10), GREEN),
    Wall((WIDTH - 10, 0), (10, HEIGHT), GREEN),
    Wall((100, 50), (200, 10), GREEN),
    Wall((300, 50), (10, 200), GREEN),
    Wall((500, 250), (200, 10), GREEN),
    Wall((700, 250), (10, 200), GREEN),
    Wall((900, 450), (200, 10), GREEN),
    Wall((1100, 450), (10, 200), GREEN),
    Wall((200, 150), (10, 300), GREEN),
    Wall((400, 350), (300, 10), GREEN),
    Wall((600, 50), (10, 400), GREEN),
    Wall((800, 150), (200, 10), GREEN),
    Wall((100, 300), (200, 10), GREEN),
    Wall((300, 400), (10, 200), GREEN),
    Wall((500, 500), (200, 10), GREEN),
    Wall((700, 600), (10, 100), GREEN), 
    Wall((900, 200), (200, 10), GREEN),
    Wall((1100, 300), (10, 200), GREEN),
]


player = Player("hero.png", (75, 75), (50, HEIGHT - 50), 5)
enemy = Enemy("cyborg.png", (75, 75), (WIDTH - 150, HEIGHT // 2), 5)
gold = GameSprite("treasure.png", (75, 75), (WIDTH - 150, HEIGHT - 150), 5)

game = True
finish = False

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    if not finish:
        sc.blit(background, (0, 0))
        
        for wall in walls:
            wall.draw(sc)

        player.reset(sc)
        enemy.reset(sc)
        gold.reset(sc)

        player.update(walls)
        enemy.update(1100, 900)
        #enemy.update_vertical(HEIGHT - 200, 200)
        
        if pygame.sprite.collide_rect(player, enemy):
            kick = pygame.mixer.Sound("kick.ogg")
            kick.play()
            sc.blit(f1, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
            finish = True

        if pygame.sprite.collide_rect(player, gold):
            money = pygame.mixer.Sound("money.ogg")
            money.play()

            sc.blit(f2, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
            finish = True

    pygame.display.update()
    clock.tick(FPS)