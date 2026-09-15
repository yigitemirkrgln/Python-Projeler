import pygame_ce as pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Shooting Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 22)

# Player
player_img = pygame.Surface((40, 40))
player_img.fill(BLUE)
player_x = WIDTH // 2
player_y = HEIGHT - 80
player_speed = 5
player_health = 100

# Weapons
current_weapon = "pistol"
weapon_stats = {
    "pistol": {"speed": 8, "cooldown": 300},
    "rifle": {"speed": 12, "cooldown": 120},
    "shotgun": {"speed": 10, "cooldown": 500},
}
last_shot_time = 0

# Bullets
bullets = []

# Enemies
enemies = []
ENEMY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMY_EVENT, 1000)

enemy_img = pygame.Surface((35, 35))
enemy_img.fill(RED)

# Power-ups
powerups = []
POWERUP_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(POWERUP_EVENT, 6000)

# Boss
boss_active = False
boss_img = pygame.Surface((150, 150))
boss_img.fill((128, 0, 128))
boss_x = WIDTH // 2 - 75
boss_y = 50
boss_health = 500
boss_bullets = []
boss_last_shot = 0


def draw_window():
    WIN.fill(BLACK)

    # Player
    WIN.blit(player_img, (player_x, player_y))

    # Player Health Bar
    pygame.draw.rect(WIN, RED, (10, 10, 200, 20))
    pygame.draw.rect(WIN, GREEN, (10, 10, player_health * 2, 20))

    # Bullets
    for b in bullets:
        pygame.draw.rect(WIN, WHITE, b)

    # Enemies
    for e in enemies:
        WIN.blit(enemy_img, (e[0], e[1]))

    # Powerups
    for p in powerups:
        pygame.draw.rect(WIN, (0, 255, 255), p)

    # Boss
    if boss_active:
        WIN.blit(boss_img, (boss_x, boss_y))
        pygame.draw.rect(WIN, RED, (boss_x, boss_y - 20, 150, 10))
        pygame.draw.rect(WIN, GREEN, (boss_x, boss_y - 20, (boss_health / 500) * 150, 10))
        for b in boss_bullets:
            pygame.draw.rect(WIN, RED, b)

    pygame.display.update()


def shoot():
    global last_shot_time
    now = pygame.time.get_ticks()
    if now - last_shot_time >= weapon_stats[current_weapon]["cooldown"]:
        last_shot_time = now
        if current_weapon == "shotgun":
            for i in range(-2, 3):
                bullets.append(pygame.Rect(player_x + 20, player_y, 8, 15))
        else:
            bullets.append(pygame.Rect(player_x + 20, player_y, 8, 15))


def main():
    global player_x, player_y, player_health
    global current_weapon, boss_active, boss_health, boss_last_shot

    run = True
    while run:
        clock.tick(60)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == ENEMY_EVENT:
                enemies.append([random.randint(20, WIDTH - 20), -40])

            if event.type == POWERUP_EVENT:
                powerups.append(pygame.Rect(random.randint(0, WIDTH - 30), -30, 30, 30))

        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 40:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < HEIGHT - 40:
            player_y += player_speed

        # Shooting
        if keys[pygame.K_SPACE]:
            shoot()

        # Weapon switch
        if keys[pygame.K_1]:
            current_weapon = "pistol"
        if keys[pygame.K_2]:
            current_weapon = "rifle"
        if keys[pygame.K_3]:
            current_weapon = "shotgun"

        # Update bullets
        for b in bullets[:]:
            b.y -= weapon_stats[current_weapon]["speed"]
            if b.y < -10:
                bullets.remove(b)

        # Update enemies
        for e in enemies[:]:
            e[1] += 2
            if e[1] > HEIGHT:
                enemies.remove(e)
            # Collision with bullets
            for b in bullets[:]:
                if pygame.Rect(e[0], e[1], 35, 35).colliderect(b):
                    bullets.remove(b)
                    enemies.remove(e)
                    break
            # Player collision
            if pygame.Rect(e[0], e[1], 35, 35).colliderect(pygame.Rect(player_x, player_y, 40, 40)):
                enemies.remove(e)
                player_health -= 10

        # Power-up collision
        for p in powerups[:]:
            p.y += 2
            if p.y > HEIGHT:
                powerups.remove(p)
            if p.colliderect(pygame.Rect(player_x, player_y, 40, 40)):
                current_weapon = random.choice(list(weapon_stats.keys()))
                powerups.remove(p)

        # Boss activation
        if not boss_active and len(enemies) > 20:
            boss_active = True

        # Boss logic
        if boss_active:
            # Boss shooting
            now = pygame.time.get_ticks()
            if now - boss_last_shot > 1000:
                boss_last_shot = now
                boss_bullets.append(pygame.Rect(boss_x + 75, boss_y + 140, 10, 20))

            for bb in boss_bullets[:]:
                bb.y += 5
                if bb.y > HEIGHT:
                    boss_bullets.remove(bb)
                if bb.colliderect(pygame.Rect(player_x, player_y, 40, 40)):
                    boss_bullets.remove(bb)
                    player_health -= 20

            # Hit boss
            for b in bullets[:]:
                if pygame.Rect(boss_x, boss_y, 150, 150).colliderect(b):
                    bullets.remove(b)
                    boss_health -= 5

            if boss_health <= 0:
                boss_active = False

        draw_window()

    pygame.quit()


if __name__ == "__main__":
    main()
