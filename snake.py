import pygame
import random
import time

# --- Setup & Constants ---
pygame.init()
pygame.mixer.init() # For sounds

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
GREEN  = (50, 205, 50)
RED    = (213, 50, 80)
BLACK  = (30, 30, 30)

# Screen Dimensions
WIDTH, HEIGHT = 800, 600
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snack Attack 2026')

clock = pygame.time.Clock()
snake_block = 20
initial_speed = 10

# --- Creative Assets ---
# Note: In a real folder, you'd use pygame.image.load('pizza.png')
# Here we use Emojis/Text to keep it "Real Snack" themed
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
emoji_font = pygame.font.SysFont("segoeuiemoji", 30)

SNACKS = ["🍕", "🍔", "🌮", "🍩", "🥨"]
POISON = "🥦" # The "Healthy" enemy

def display_score(score):
    value = score_font.render(f"Calories Gained: {score}", True, YELLOW)
    dis.blit(value, [10, 10])

def draw_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        # Head is an open mouth, body is circles
        content = "😋" if i == len(snake_list)-1 else "🟢"
        char = emoji_font.render(content, True, WHITE)
        dis.blit(char, [x[0], x[1]])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [WIDTH / 6, HEIGHT / 3])

# --- Main Game Loop ---
def gameLoop():
    game_over = False
    game_close = False

    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0

    snake_List = []
    Length_of_snake = 1
    current_speed = initial_speed

    # Randomly place the first snack
    snack_type = random.choice(SNACKS)
    foodx = round(random.randrange(0, WIDTH - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, HEIGHT - snake_block) / 20.0) * 20.0

    while not game_over:

        while game_close == True:
            dis.fill(BLACK)
            message("Ugh, Food Coma! Press C-Play Again or Q-Quit", RED)
            display_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Boundary Check
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True
        
        x1 += x1_change
        y1 += y1_change
        dis.fill(BLACK)

        # Draw Snack
        snack_txt = emoji_font.render(snack_type, True, WHITE)
        dis.blit(snack_txt, [foodx, foody])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Self-collision Check
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(snake_block, snake_List)
        display_score(Length_of_snake - 1)

        pygame.display.update()

        # Check if snack eaten
        if x1 == foodx and y1 == foody:
            # SOUND SIMULATION (Since I can't send .wav files, use beep)
            print("\a") # System Beep!
            
            foodx = round(random.randrange(0, WIDTH - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, HEIGHT - snake_block) / 20.0) * 20.0
            
            # Creative Mechanic: Sugar Rush!
            if snack_type == "🍩":
                current_speed += 2 # Donuts make you hyper
            
            snack_type = random.choice(SNACKS)
            Length_of_snake += 1

        clock.tick(current_speed)

    pygame.quit()
    quit()

gameLoop()
