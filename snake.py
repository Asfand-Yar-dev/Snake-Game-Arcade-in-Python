import pygame
import random
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(pygame.font.match_font('arcadeclassic,arial'), 20)

# Game variables
snake = [(100, 100)]
direction = (CELL_SIZE, 0)
food = (300, 200)
power_up = None
score = 0
speed = 10
clock = pygame.time.Clock()

def draw_snake(screen):
    for i, segment in enumerate(snake):
        border_radius = 8 if i == 0 else 4  # Head has a larger border radius
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE), border_radius=border_radius)

def draw_food(screen):
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE), border_radius=6)

def draw_power_up(screen):
    if power_up:
        pygame.draw.rect(screen, YELLOW, (*power_up, CELL_SIZE, CELL_SIZE), border_radius=6)

def draw_score(screen):
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def move_snake():
    global snake
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, new_head)
    if new_head != food and new_head != power_up:
        snake.pop()
    return new_head

def spawn_food():
    while True:
        pos = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
               random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
        if pos not in snake:
            return pos

def spawn_power_up():
    if random.random() < 0.1:  # 10% chance to spawn a power-up
        return spawn_food()
    return None

def check_collision(new_head):
    return (new_head in snake[1:] or
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT)

def main():
    global direction, food, power_up, score, speed
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    running = True
    
    while running:
        screen.fill(BLACK)
        draw_snake(screen)
        draw_food(screen)
        draw_power_up(screen)
        draw_score(screen)
        pygame.display.flip()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)
        
        # Move snake
        new_head = move_snake()
        
        # Check collisions
        if check_collision(new_head):
            break  # Game over
        
        # Eat food
        if new_head == food:
            score += 10
            speed += 0.5  # Increase difficulty
            food = spawn_food()
            if power_up is None:
                power_up = spawn_power_up()
        
        # Eat power-up
        if power_up and new_head == power_up:
            score += 20
            speed += 1
            power_up = None
        
        clock.tick(speed)
    
    # Game over screen
    screen.fill(BLACK)
    game_over_text = FONT.render("GAME OVER", True, RED)
    score_text = FONT.render(f"Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH//2 - 50, HEIGHT//2 - 20))
    screen.blit(score_text, (WIDTH//2 - 50, HEIGHT//2 + 20))
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()

if __name__ == "__main__":
    main()
