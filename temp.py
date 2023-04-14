import streamlit as st
import random

def random_from_list(lst):
    """
    Returns a random value from the input list.

    Parameters:
    lst (list): A list of values.

    Returns:
    A random value from the input list.
    """
    return random.choice(lst)

def move_towards_food(blob_x, blob_y, food_locations):
    # Find the closest food pellet
    closest_food_distance = float('inf')
    closest_food_location = None
    for food_location in food_locations:
        food_distance = ((blob_x - food_location[0]) ** 2 + (blob_y - food_location[1]) ** 2) ** 0.5
        if food_distance < closest_food_distance:
            closest_food_distance = food_distance
            closest_food_location = food_location

    # Move towards the closest food pellet
    dx = closest_food_location[0] - blob_x
    dy = closest_food_location[1] - blob_y
    if abs(dx) > abs(dy):
        if dx > 0:
            blob_x += blob_speed
        else:
            blob_x -= blob_speed
    else:
        if dy > 0:
            blob_y += blob_speed
        else:
            blob_y -= blob_speed

    # Return the new blob position
    return blob_x, blob_y



# make a blob class

# make a world class



#       Numbering Guide for GRID
#       _________________________
#      |    1   |   2   |   3   |
#      |--------+-------+-------|
#      |    4   |       |   5   |
#      |--------+-------+-------|
#      |    6   |   7   |   8   |
#      |________________________|
 




# world
# \__Tiles
#         \__ Nutrients (0-100)
#         \__ Occupied: Blob Type
#         \__ IsEdgeTile [sides 1-8]
# \__Blobs
#          \
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Blob Game")

# Set up the grid
GRID_SIZE = 1
NUM_ROWS = int(WINDOW_HEIGHT / GRID_SIZE)
NUM_COLS = int(WINDOW_WIDTH / GRID_SIZE)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define blob properties
blob_x = random.randint(0, NUM_COLS - 1) * GRID_SIZE
blob_y = random.randint(0, NUM_ROWS - 1) * GRID_SIZE
blob_size = 10
blob_speed = .05
blob_health = 10

# Define health bar properties
health_bar_width = 100
health_bar_height = 10
health_bar_x = 10
health_bar_y = 10

# Define food properties
food_size = 10
num_food = 10
food_list = []
for i in range(num_food):
    food_x = random.randint(0, NUM_COLS - 1) * GRID_SIZE
    food_y = random.randint(0, NUM_ROWS - 1) * GRID_SIZE
    food_list.append((food_x, food_y))

# Define game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the blob
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and blob_x > 0:
        blob_x -= blob_speed
    elif keys[pygame.K_RIGHT] and blob_x < WINDOW_WIDTH - blob_size:
        blob_x += blob_speed
    elif keys[pygame.K_UP] and blob_y > 0:
        blob_y -= blob_speed
    elif keys[pygame.K_DOWN] and blob_y < WINDOW_HEIGHT - blob_size:
        blob_y += blob_speed

    blob_x,blob_y = move_towards_food(blob_x,blob_y,food_list)

    # Check for collision with food particles
    for food in food_list:
        if blob_x < food[0] + food_size and blob_x + blob_size > food[0] and blob_y < food[1] + food_size and blob_y + blob_size > food[1]:
            blob_health += 10
            food_list.remove(food)

    # Draw the game window
    game_window.fill(WHITE)
    pygame.draw.rect(game_window, RED, (blob_x, blob_y, blob_size, blob_size))
    for food in food_list:
        pygame.draw.rect(game_window, GREEN, (food[0], food[1], food_size, food_size))
    pygame.draw.rect(game_window, BLACK, (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
    health_bar_fill = max(0, min(health_bar_width, health_bar_width * (blob_health / 100)))
    pygame.draw.rect(game_window, GREEN, (health_bar_x + 1, health_bar_y + 1, health_bar_fill - 1, health_bar_height - 1))
    pygame.display.update()

# Quit Pygame
pygame.quit()
