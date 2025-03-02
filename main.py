import pygame

pygame.init()
pygame.mixer.init()

#SETTING
HEIGHT = 700
WIDTH = 1200
FPS = 60

#COLOR
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze")

clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load("background.jpg"),
             (WIDTH, HEIGHT))

pygame.mixer.music.load("jungles.ogg")
pygame.mixer.music.play()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename: str,
                  size: tuple[int, int],
                    coords: tuple[int, int], speed: int):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(filename), size)
        self.rect = self.image.get_rect(center = coords)
        self.speed = speed

    def reset(self, sc: pygame.Surface):
        sc.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < WIDTH - 80:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < HEIGHT - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def update(self, x1: int, x2: int):
        self.rect.x += self.speed

        if self.rect.x >= x1 or self.rect.x <= x2:
            self.speed *= -1

    def update_vertical(self, y1: int, y2: int):
        self.rect.y += self.speed

        if self.rect.y >= y1 or self.rect.y <= y2:
            self.speed *= -1

player = Player("hero.png", (75, 75), (50, HEIGHT - 50), 5)
enemy = Enemy("cyborg.png", (75, 75), (WIDTH - 150, HEIGHT // 2), 5)
gold = GameSprite("treasure.png", (75, 75), (WIDTH  - 150, HEIGHT - 150), 5)

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    sc.blit(background, (0, 0))

    player.reset(sc)
    enemy.reset(sc)
    gold.reset(sc)

    player.update()
    enemy.update(1100, 900)
    enemy.update_vertical(HEIGHT - 200, 200)

    pygame.display.update()
    clock.tick(FPS)