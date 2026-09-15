import pygame
import random
import sys
import os
import math

pygame.init()
pygame.mixer.init()

# --- EKRAN ---
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SCP: Betrayal - Beta Edition")

# --- PLACEHOLDER ---
def create_placeholder(size, color, text=""):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill((*color, 200))
    pygame.draw.rect(surf, color, (0, 0, size[0], size[1]), border_radius=10)
    if text:
        font = pygame.font.SysFont("Arial", 16, bold=True)
        txt = font.render(text, True, (255, 255, 255))
        surf.blit(txt, (size[0]//2 - txt.get_width()//2, size[1]//2 - txt.get_height()//2))
    return surf

def load_or_create(filename, size, color, text=""):
    path = os.path.join("assets", filename)
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        except Exception as e:
            print(f"Resim yüklenemedi: {filename} → {e}")
    print(f"{filename} bulunamadı → placeholder")
    return create_placeholder(size, color, text)

# --- ASSETLER ---
PLAYER_IMG = load_or_create("player.png", (60, 90), (0, 120, 255), "Alpha-1")
PLAYER2_IMG = load_or_create("player2.png", (70, 100), (255, 200, 0), "GOD")
BULLET_IMG = load_or_create("bullet.png", (14, 38), (255, 255, 100))
BULLET2_IMG = load_or_create("bullet2.png", (20, 52), (0, 255, 255))
POWERUP_IMG = load_or_create("powerup.png", (50, 50), (0, 255, 100), "PWR")
SCP173_IMG = load_or_create("scp173.png", (70, 90), (180, 180, 180), "SCP-173")
SCP939_IMG = load_or_create("scp939.png", (90, 80), (200, 0, 50), "SCP-939")
BOSS_IMG = load_or_create("scp_682.png", (180, 150), (80, 150, 50), "SCP-682")
BG = load_or_create("background.png", (WIDTH, HEIGHT), (15, 15, 40))
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

FLOOR_Y = HEIGHT - 50
GRAVITY = 0.8
JUMP_FORCE = 14

# --- MARKET ---
SHOP_BUTTONS = [
    {"name": "Rapid Fire", "cost": 150, "desc": "Ates hizi +40%", "color": (0, 255, 0)},
    {"name": "Shield", "cost": 250, "desc": "10s kalkan", "color": (0, 100, 255)},
    {"name": "Speed Boost", "cost": 200, "desc": "15s hiz artisi", "color": (255, 255, 0)},
    {"name": "Health +50", "cost": 100, "desc": "Max can +50", "color": (255, 0, 0)},
]

class Market:
    def __init__(self):
        self.open = False
        self.panel_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 180, 400, 360)
        self.buttons = []

    def toggle(self):
        self.open = not self.open
        if self.open:
            self.create_buttons()

    def create_buttons(self):
        self.buttons = []
        start_y = self.panel_rect.y + 100
        for i, item in enumerate(SHOP_BUTTONS):
            rect = pygame.Rect(self.panel_rect.x + 25, start_y + i*70, 350, 55)
            self.buttons.append({"rect": rect, "item": item})

    def handle_click(self, pos, score, player):
        if not self.open: return score
        for btn in self.buttons:
            if btn["rect"].collidepoint(pos):
                if score >= btn["item"]["cost"]:
                    self.apply_item(btn["item"], player)
                    return score - btn["item"]["cost"]
        return score

    def apply_item(self, item, player):
        name = item["name"]
        if name == "Rapid Fire":
            player.weapon_type = "rapid"
        elif name == "Shield":
            player.shield_timer = pygame.time.get_ticks() + 10000
        elif name == "Speed Boost":
            player.speed_boost_timer = pygame.time.get_ticks() + 15000
        elif name == "Health +50":
            player.max_health += 50
            player.health = min(player.health + 50, player.max_health)

    def draw(self, win, score):
        if not self.open: return

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(140)
        overlay.fill((0, 0, 0))
        win.blit(overlay, (0, 0))

        pygame.draw.rect(win, (40, 40, 60), self.panel_rect, border_radius=20)
        pygame.draw.rect(win, (100, 200, 255), self.panel_rect, 5, border_radius=20)

        title = pygame.font.SysFont("Impact", 40, bold=True).render("MARKET", True, (255, 255, 255))
        score_txt = pygame.font.SysFont("Arial", 28, bold=True).render(f"SCORE: {score}", True, (255, 255, 0))
        win.blit(title, (self.panel_rect.centerx - title.get_width()//2, self.panel_rect.y + 20))
        win.blit(score_txt, (self.panel_rect.centerx - score_txt.get_width()//2, self.panel_rect.y + 65))

        for btn in self.buttons:
            rect = btn["rect"]
            color = btn["item"]["color"]
            pygame.draw.rect(win, color, rect, border_radius=12)
            pygame.draw.rect(win, (255, 255, 255), rect, 3, border_radius=12)

            name = pygame.font.SysFont("Arial", 22, bold=True).render(btn["item"]["name"], True, (255, 255, 255))
            cost = pygame.font.SysFont("Arial", 20).render(f"{btn['item']['cost']} puan", True, (255, 255, 0))
            desc = pygame.font.SysFont("Arial", 16).render(btn["item"]["desc"], True, (200, 200, 200))

            win.blit(name, (rect.x + 15, rect.y + 8))
            win.blit(cost, (rect.x + rect.width - cost.get_width() - 15, rect.y + 8))
            win.blit(desc, (rect.x + 15, rect.y + 32))

        close_rect = pygame.Rect(self.panel_rect.x + 340, self.panel_rect.y + 10, 50, 40)
        pygame.draw.rect(win, (200, 0, 0), close_rect, border_radius=10)
        close_txt = pygame.font.SysFont("Arial", 30, bold=True).render("X", True, (255, 255, 255))
        win.blit(close_txt, (close_rect.centerx - 10, close_rect.y + 5))

# --- PLAYER ---
class Player:
    def __init__(self):
        self.rect = PLAYER_IMG.get_rect(midbottom=(WIDTH//2, FLOOR_Y))
        self.vel_y = 0
        self.on_ground = True
        self.powered = False
        self.power_timer = 0
        self.health = 100
        self.max_health = 100
        self.shield_timer = 0
        self.speed_boost_timer = 0
        self.weapon_type = "MTF E11-SR"
        self.image = PLAYER_IMG
        self.base_speed = 7

    def update(self, keys, market_open):
        if market_open: return

        speed = self.base_speed * 1.6 if pygame.time.get_ticks() < self.speed_boost_timer else self.base_speed

        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += speed

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -JUMP_FORCE
            self.on_ground = False

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        if self.rect.bottom >= FLOOR_Y:
            self.rect.bottom = FLOOR_Y
            self.on_ground = True
            self.vel_y = 0

        if self.powered and pygame.time.get_ticks() > self.power_timer:
            self.powered = False
            self.image = PLAYER_IMG
        elif self.powered:
            self.image = PLAYER2_IMG

    def shoot(self, mouse_pos):
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        angle = math.atan2(dy, dx)
        base_speed = 22 if self.powered else 16
        img = BULLET2_IMG if self.powered else BULLET_IMG
        damage_mult = 1.5 if self.weapon_type == "rapid" else 1.0
        return Bullet(self.rect.centerx, self.rect.centery, angle, base_speed, img, damage_mult)

    def take_damage(self, dmg):
        if pygame.time.get_ticks() < self.shield_timer:
            return 0
        self.health -= dmg
        return dmg

    def draw(self, win):
        win.blit(self.image, self.rect)
        if pygame.time.get_ticks() < self.shield_timer:
            pygame.draw.circle(win, (0, 200, 255, 100), self.rect.center, 45, 5)

    def get_cooldown(self):
        cd = 5 if self.powered else 10
        if self.weapon_type == "rapid":
            cd = max(2, int(cd * 0.55))
        return cd

# --- DİĞER SINIFLAR (Bullet, Enemy, Boss, PowerUp) aynı kaldı ---
class Bullet:
    def __init__(self, x, y, angle, speed, img, damage_mult=1.0):
        self.x = float(x)
        self.y = float(y)
        self.angle = angle
        self.speed = speed
        self.image = img
        self.rect = self.image.get_rect(center=(int(x), int(y)))
        self.damage_mult = damage_mult

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, win):
        win.blit(self.image, self.rect)

    def off_screen(self):
        return not (-200 < self.x < WIDTH + 200 and -200 < self.y < HEIGHT + 200)

class Enemy:
    def __init__(self):
        self.image = random.choice([SCP173_IMG, SCP939_IMG])
        side = random.choice(["left", "right"])
        x = -100 if side == "left" else WIDTH + 100
        self.rect = self.image.get_rect(midbottom=(x, FLOOR_Y))
        self.vel_y = 0
        self.on_ground = True
        self.health = random.randint(40, 60)
        self.jump_timer = random.randint(80, 200)

    def update(self, player_rect, market_open):
        if market_open: return
        if player_rect.centerx < self.rect.centerx:
            self.rect.x -= 2.4
        else:
            self.rect.x += 2.4

        self.jump_timer -= 1
        if self.jump_timer <= 0 and self.on_ground:
            self.vel_y = -JUMP_FORCE * random.uniform(0.8, 1.2)
            self.on_ground = False
            self.jump_timer = random.randint(120, 300)

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        if self.rect.bottom >= FLOOR_Y:
            self.rect.bottom = FLOOR_Y
            self.on_ground = True
            self.vel_y = 0

    def draw(self, win):
        win.blit(self.image, self.rect)

class Boss:
    def __init__(self):
        side = random.choice([0, WIDTH])
        self.image = BOSS_IMG
        self.rect = self.image.get_rect(midbottom=(side, FLOOR_Y))
        self.health = 1600
        self.alive = True
        self.vel_y = 0
        self.on_ground = True

    def update(self, player_rect, market_open):
        if not self.alive or market_open: return
        if player_rect.centerx < self.rect.centerx:
            self.rect.x -= 1.7
        else:
            self.rect.x += 1.7

        if random.random() < 0.02 and self.on_ground:
            self.vel_y = -JUMP_FORCE * 1.4

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        if self.rect.bottom >= FLOOR_Y:
            self.rect.bottom = FLOOR_Y
            self.on_ground = True
            self.vel_y = 0

    def draw(self, win):
        if self.alive:
            win.blit(self.image, self.rect)

class PowerUp:
    def __init__(self):
        self.rect = POWERUP_IMG.get_rect(center=(random.randint(100, WIDTH-100), -60))

    def update(self, market_open):
        if not market_open:
            self.rect.y += 4

    def draw(self, win):
        win.blit(POWERUP_IMG, self.rect)

# --- MENÜ VE ANA OYUN ---
def main_menu():
    font_big = pygame.font.SysFont("Impact", 80, bold=True)
    font_small = pygame.font.SysFont("Arial", 34)
    while True:
        WIN.blit(BG, (0, 0))
        title = font_big.render("SCP: BETRAYAL", True, (200, 20, 20))
        start = font_small.render("SPACE ile basla", True, (255, 255, 255))
        info = font_small.render("A/D = Hareket • SPACE = Ziplama • M = MARKET • Fare = Nişan • Sol Tik = Ates", True, (100, 200, 225))
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 140))
        WIN.blit(start, (WIDTH//2 - start.get_width()//2, 260))
        WIN.blit(info, (WIDTH//2 - info.get_width()//2, 310))
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                return

def main():
    clock = pygame.time.Clock()
    player = Player()
    market = Market()
    bullets = []
    enemies = []
    powerups = []
    boss = None
    score = 0
    font = pygame.font.SysFont("Arial", 32, bold=True)
    shoot_cooldown = 0

    pygame.time.set_timer(pygame.USEREVENT + 1, 3200)
    pygame.time.set_timer(pygame.USEREVENT + 2, 18000)
    pygame.time.set_timer(pygame.USEREVENT + 3, 80000)

    while True:
        clock.tick(60)
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # BURASI DÜZELTİLDİ!
                    market.toggle()

            if event.type == pygame.MOUSEBUTTONDOWN and mouse_pressed and market.open:
                score = market.handle_click(mouse_pos, score, player)

            if event.type == pygame.USEREVENT + 1 and not market.open:
                enemies.append(Enemy())
            if event.type == pygame.USEREVENT + 2 and not market.open:
                powerups.append(PowerUp())
            if event.type == pygame.USEREVENT + 3 and boss is None and not market.open:
                boss = Boss()

        # Ateş
        if mouse_pressed and shoot_cooldown == 0 and not market.open:
            bullets.append(player.shoot(mouse_pos))
            shoot_cooldown = player.get_cooldown()
        if shoot_cooldown > 0:
            shoot_cooldown -= 1

        player.update(keys, market.open)

        # Diğer güncellemeler...
        for b in bullets[:]:
            b.update()
            if b.off_screen():
                bullets.remove(b)

        for e in enemies[:]:
            e.update(player.rect, market.open)

        for p in powerups[:]:
            p.update(market.open)
            if p.rect.top > HEIGHT:
                powerups.remove(p)

        if boss:
            boss.update(player.rect, market.open)

        # Çarpışmalar (kısaltılmış ama çalışıyor)
        for e in enemies[:]:
            for b in bullets[:]:
                if e.rect.colliderect(b.rect):
                    e.health -= int(45 * b.damage_mult) if player.powered else int(22 * b.damage_mult)
                    bullets.remove(b)
                    if e.health <= 0:
                        enemies.remove(e)
                        score += 50
                    break
            if e.rect.colliderect(player.rect):
                player.take_damage(random.randint(8, 13))
                enemies.remove(e)

        if boss and boss.alive:
            for b in bullets[:]:
                if boss.rect.colliderect(b.rect):
                    boss.health -= int(55 * b.damage_mult) if player.powered else int(28 * b.damage_mult)
                    bullets.remove(b)
                    if boss.health <= 0:
                        score += 3000
                        boss.alive = False
            if boss.rect.colliderect(player.rect):
                player.take_damage(22)

        for p in powerups[:]:
            if player.rect.colliderect(p.rect):
                player.powered = True
                player.power_timer = pygame.time.get_ticks() + 12000
                powerups.remove(p)

        if player.health <= 0:
            break

        # ÇİZİM
        WIN.blit(BG, (0, 0))
        player.draw(WIN)
        for obj in bullets + enemies + powerups:
            obj.draw(WIN)
        if boss and boss.alive:
            boss.draw(WIN)

        market.draw(WIN, score)

        # UI
        score_txt = font.render(f"SCORE: {score}", True, (255, 255, 0))
        WIN.blit(score_txt, (10, 10))
        pygame.draw.rect(WIN, (80, 0, 0), (10, 50, 200, 25))
        pygame.draw.rect(WIN, (0, 255, 0), (10, 50, (player.health / player.max_health) * 200, 25))
        hp_txt = font.render(f"HP: {player.health}/{player.max_health}", True, (255, 255, 255))
        WIN.blit(hp_txt, (220, 45))
        weapon_txt = font.render(f"Silah: {player.weapon_type.upper()}", True, (255, 255, 255))
        WIN.blit(weapon_txt, (10, HEIGHT - 40))

        m_key = pygame.font.SysFont("Arial", 26).render("M = MARKET", True, (0, 255, 0))
        WIN.blit(m_key, (WIDTH - 160, 10))

        pygame.display.update()

    # GAME OVER
    while True:
        WIN.fill((10, 0, 20))
        go = pygame.font.SysFont("Impact", 100, bold=True).render("GAME OVER", True, (200, 0, 0))
        final = font.render(f"Final Score: {score}", True, (255, 255, 100))
        again = pygame.font.SysFont("Arial", 36).render("Tekrar icin SPACE", True, (200, 200, 255))
        WIN.blit(go, (WIDTH//2 - go.get_width()//2, 160))
        WIN.blit(final, (WIDTH//2 - final.get_width()//2, 280))
        WIN.blit(again, (WIDTH//2 - again.get_width()//2, 340))
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                main()

if __name__ == "__main__":
    main_menu()
    main()