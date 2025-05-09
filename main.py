import pygame  
import random  
import os  
import math  

# Initialize Pygame  
pygame.init()  

# Set up the game window  
WIDTH = 800  
HEIGHT = 600  
window = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("Space Defender")  

# Colors  
WHITE = (255, 255, 255)  
BLACK = (0, 0, 0)  
RED = (255, 0, 0)  

# Player class  
class Player(pygame.sprite.Sprite):  
    def __init__(self):  
        super().__init__()  
        self.image = pygame.Surface((50, 40))  
        self.image.fill(WHITE)  
        self.rect = self.image.get_rect()  
        self.rect.centerx = WIDTH // 2  
        self.rect.bottom = HEIGHT - 10  
        self.speed_x = 0  
        self.health = 100  

    def update(self):  
        self.speed_x = 0  
        keystate = pygame.key.get_pressed()  
        if keystate[pygame.K_LEFT]:  
            self.speed_x = -8  
        if keystate[pygame.K_RIGHT]:  
            self.speed_x = 8  
        self.rect.x += self.speed_x  
        if self.rect.right > WIDTH:  
            self.rect.right = WIDTH  
        if self.rect.left < 0:  
            self.rect.left = 0  

    def shoot(self):  
        bullet = Bullet(self.rect.centerx, self.rect.top)  
        all_sprites.add(bullet)  
        bullets.add(bullet)  

# Enemy class  
class Enemy(pygame.sprite.Sprite):  
    def __init__(self):  
        super().__init__()  
        self.image = pygame.Surface((30, 30))  
        self.image.fill(RED)  
        self.rect = self.image.get_rect()  
        self.rect.x = random.randrange(WIDTH - self.rect.width)  
        self.rect.y = random.randrange(-100, -40)  
        self.speedy = random.randrange(1, 8)  
        self.speedx = random.randrange(-3, 3)  

    def update(self):  
        self.rect.y += self.speedy  
        self.rect.x += self.speedx  
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:  
            self.rect.x = random.randrange(WIDTH - self.rect.width)  
            self.rect.y = random.randrange(-100, -40)  
            self.speedy = random.randrange(1, 8)  

# Bullet class  
class Bullet(pygame.sprite.Sprite):  
    def __init__(self, x, y):  
        super().__init__()  
        self.image = pygame.Surface((5, 10))  
        self.image.fill(WHITE)  
        self.rect = self.image.get_rect()  
        self.rect.bottom = y  
        self.rect.centerx = x  
        self.speedy = -10  

    def update(self):  
        self.rect.y += self.speedy  
        if self.rect.bottom < 0:  
            self.kill()  

# Sprite groups  
all_sprites = pygame.sprite.Group()  
enemies = pygame.sprite.Group()  
bullets = pygame.sprite.Group()  

player = Player()  
all_sprites.add(player)  

for i in range(8):  
    enemy = Enemy()  
    all_sprites.add(enemy)  
    enemies.add(enemy)  

# Game loop  
score = 0  
running = True  
clock = pygame.time.Clock()  

while running:  
    # Keep loop running at the right speed  
    clock.tick(60)  

    # Process input (events)  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
        elif event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_SPACE:  
                player.shoot()  

    # Update  
    all_sprites.update()  

    # Check for bullet-enemy collisions  
    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)  
    for hit in hits:  
        score += 10  
        enemy = Enemy()  
        all_sprites.add(enemy)  
        enemies.add(enemy)  

    # Check for player-enemy collisions  
    hits = pygame.sprite.spritecollide(player, enemies, False)  
    if hits:  
        player.health -= 1  
        if player.health <= 0:  
            running = False  

    # Draw / render  
    window.fill(BLACK)  
    all_sprites.draw(window)  

    # Draw score  
    font = pygame.font.Font(None, 36)  
    score_text = font.render(f'Score: {score}', True, WHITE)  
    health_text = font.render(f'Health: {player.health}', True, WHITE)  
    window.blit(score_text, (10, 10))  
    window.blit(health_text, (10, 40))  

    # Flip the display  
    pygame.display.flip()  

pygame.quit()  

