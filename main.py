import pygame

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# DISPLAY SET UP
window_size = (1100, 700)
display = pygame.display.set_mode(window_size)

# Load and scale background image for the first page
bg_image = pygame.image.load('intro_background.png')
bg_image = pygame.transform.scale(bg_image, window_size)

# Load and scale background image for the second page
loading_image = pygame.image.load('loading_background.png')
loading_image = pygame.transform.scale(loading_image, window_size)

# load & scale background image for questions page
question_bg_image = pygame.image.load('question_bg.png')
question_bg_image = pygame.transform.scale(question_bg_image, window_size)

# Button properties
button_color = GREEN
button_hover_color = (0, 200, 0)

# Define page states
PAGE_MAIN = 0
PAGE_SECOND = 1
PAGE_THIRD = 2
current_page = PAGE_MAIN

main_button_rect = pygame.Rect(450, 500, 200, 50)
next_button_rect = pygame.Rect(450, 400, 200, 50)
back_button_rect = pygame.Rect(450, 500, 200, 50)

# GAMEPLAY VARIABLES

turns = 0
score = 0

# PAGE DRAWING METHODS

def draw_main_page():
    display.blit(bg_image, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    if main_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display, button_hover_color, main_button_rect)
    else:
        pygame.draw.rect(display, button_color, main_button_rect)
    
    # Draw button text
    font = pygame.font.Font(None, 36)
    text = font.render("Play", True, WHITE)
    text_rect = text.get_rect(center=main_button_rect.center)
    display.blit(text, text_rect)

def draw_second_page():
    display.blit(loading_image, (0, 0))  # Use the loading image here


    font = pygame.font.Font(None, 48)
    text = font.render("Welcome to the Second Page!", True, BLACK)
    text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
    display.blit(text, text_rect)

    mouse_pos = pygame.mouse.get_pos()
    # Draw back button
    if next_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display, button_hover_color, next_button_rect)
    else:
        pygame.draw.rect(display, button_color, next_button_rect)
    next_text = font.render("Continue", True, WHITE)
    next_text_rect = next_text.get_rect(center=next_button_rect.center)
    display.blit(next_text, next_text_rect)

def draw_third_page():
    display.blit(question_bg_image, (0, 0))

    font = pygame.font.Font(None, 48)
    text = font.render("Welcome to the Third Page!", True, BLACK)
    text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
    display.blit(text, text_rect)


   
    # Draw back button
    if back_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(display, button_hover_color, back_button_rect)
    else:
        pygame.draw.rect(display, button_color, back_button_rect)
    back_text = font.render("Continue", True, WHITE)
    back_text_rect = back_text.get_rect(center=back_button_rect.center)
    display.blit(back_text, back_text_rect)


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_page == PAGE_MAIN and main_button_rect.collidepoint(event.pos):
                current_page = PAGE_SECOND  # Go to second page
            if current_page == PAGE_SECOND and next_button_rect.collidepoint(event.pos):
                current_page = PAGE_THIRD  # Go to third page
            if current_page == PAGE_THIRD and back_button_rect.collidepoint(event.pos):
                current_page = PAGE_MAIN #go back to main page

    if current_page == PAGE_MAIN:
        draw_main_page()
    elif current_page == PAGE_SECOND:
        draw_second_page()
    elif current_page == PAGE_THIRD:
        draw_third_page()

    pygame.display.flip()

# Quit Pygame
pygame.quit()
