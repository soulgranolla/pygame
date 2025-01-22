import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
GROUND_HEIGHT = 400
GROUND_COLOR = (139, 69, 19)  # Brown color for the ground
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 30
HIGH_SCORE_FILE = "high_score.txt"

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Alqaida Game (9/11 simuator)")

# Load assets
dino_img = pygame.image.load('plane.PNG')
cactus_img = pygame.image.load('tower.png')
f15_img = pygame.image.load('f15.png')

# Resize images
dino_img = pygame.transform.scale(dino_img, (100, 100))
cactus_img = pygame.transform.scale(cactus_img, (100, 100))
f15_img = pygame.transform.scale(f15_img, (100, 50))

# Dinosaur class
class Dinosaur:
    def __init__(self):
        self.image = dino_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = GROUND_HEIGHT - self.rect.height
        self.is_jumping = False
        self.is_crouching = False
        self.jump_speed = -30
        self.gravity = 2

    def update(self):
        if self.is_jumping:
            self.rect.y += self.jump_speed
            self.jump_speed += self.gravity
            if self.rect.y >= GROUND_HEIGHT - self.rect.height:
                self.rect.y = GROUND_HEIGHT - self.rect.height
                self.is_jumping = False
                self.is_crouching = False

        if self.is_crouching and not self.is_jumping:
            self.rect.height = dino_img.get_height()
            self.image = dino_img
        else:
            self.rect.height = dino_img.get_height()
            self.image = dino_img

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_speed = -30 if not self.is_crouching else -25  # Lower jump speed if crouching

    def crouch(self):
        if not self.is_jumping:
            self.is_crouching = True

    def stand_up(self):
        self.is_crouching = False

# Cactus class
class Cactus:
    def __init__(self, speed):
        self.image = cactus_img
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = GROUND_HEIGHT - self.rect.height
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
# F-15 class
class F15:
    def __init__(self, speed):
        self.image = f15_img
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(50, GROUND_HEIGHT - 150)
        self.speed = speed
        self.radar_range = 600

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -self.rect.width:
            self.rect.x = SCREEN_WIDTH
            self.rect.y = random.randint(50, GROUND_HEIGHT - 150)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def read_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    return 0

def write_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

def game_over_menu(score, high_score):
    font = pygame.font.SysFont(None, 48)
    while True:
        screen.fill(WHITE)
        game_over_text = font.render("Game Over", True, BLACK)
        score_text = font.render(f"Score: {score}", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        replay_text = font.render("Press R to Replay or Q to Quit", True, BLACK)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(replay_text, (SCREEN_WIDTH // 2 - replay_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    return False

# Main game loop
def main():
    clock = pygame.time.Clock()
    dino = Dinosaur()
    cacti = []
    f15s = []
    spawn_timer = 0
    score = 0
    speed = 10
    running = True

    font = pygame.font.SysFont(None, 36)
    high_score = read_high_score()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()
                if event.key == pygame.K_DOWN:
                    dino.crouch()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dino.stand_up()

        dino.update()

        # Spawn cacti less frequently and more randomly
        spawn_timer += 1
        if spawn_timer > random.randint(50, 150):
            if len(cacti) == 0 or cacti[-1].rect.x < SCREEN_WIDTH - 200:
                cacti.append(Cactus(speed))
                spawn_timer = 0

        # Spawn F-15s based on score
        if score % 500 == 0 and score != 0:
            if len(f15s) == 0 or f15s[-1].rect.x < SCREEN_WIDTH - 200:
                f15s.append(F15(speed))

        for cactus in cacti:
            cactus.update()
            if cactus.rect.x < -cactus.rect.width:
                cacti.remove(cactus)

        for f15 in f15s:
            f15.update()
            if f15.rect.x < -f15.rect.width:
                f15s.remove(f15)

        # Check for collision with cacti
        for cactus in cacti:
            if dino.rect.colliderect(cactus.rect):
                if score > high_score:
                    high_score = score
                    write_high_score(high_score)
                if not game_over_menu(score, high_score):
                    running = False
                else:
                    main()
                    return

        # Check for collision with F-15
        for f15 in f15s:
            if dino.rect.colliderect(f15.rect):
                if score > high_score:
                    high_score = score
                    write_high_score(high_score)
                if not game_over_menu(score, high_score):
                    running = False
                else:
                    main()
                    return

        # Increase score and speed
        score += 1
        if score % 100 == 0:
            speed += 1

        # Draw everything
        screen.fill(WHITE)
        
        # Draw ground
        pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
        
        dino.draw(screen)
        for cactus in cacti:
            cactus.draw(screen)
        for f15 in f15s:
            f15.draw(screen)

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 40))

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()