import pygame

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (129, 167, 144)
DARK_GREEN = (36,130,72)
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

#load & scale background for the ending page
ending_bg_image = pygame.image.load('ending_background.png')
ending_bg_image = pygame.transform.scale(ending_bg_image, window_size)

# Button properties
button_color = GREEN
button_hover_color = (36, 130, 72)

# Define page states
PAGE_MAIN = 0
PAGE_SECOND = 1
PAGE_THIRD = 2
PAGE_FOURTH = 3
PAGE_ANS = 4
current_page = PAGE_MAIN

main_button_rect = pygame.Rect(450, 500, 200, 50)
next_button_rect = pygame.Rect(450, 400, 200, 50)
result_button_rect = pygame.Rect(450, 500, 200, 50)
back_button_rect = pygame.Rect(450, 400, 200, 50)
continue_button_rect = pygame.Rect(450, 600, 200, 50)


# GAMEPLAY VARIABLES
max_rounds = 5
turns = 0
score = 0
correct_ans = True
answer_processed = False

# PAGE DRAWING METHODS

def draw_task_bar():
    bar_end = 550 * ((score)/max_rounds) -10
    pygame.draw.rect(display, DARK_GREEN, (290, 20, 550, 35))
    pygame.draw.rect(display, GREEN, (297, 27, bar_end, 22))
    pygame.draw.rect(display, BLACK, ((297 + bar_end), 20, 6, 35))
    pygame.draw.rect(display, BLACK, ((297 + bar_end), 20, 17, 9))
    pygame.draw.ellipse(display, BLACK, ((280 + bar_end), 43, 25, 20))
    
def draw_singing_question():
    font = pygame.font.Font(None, 48)
    text = font.render("Sight-Singing Question Goes Here", True, BLACK)
    text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
    display.blit(text, text_rect)

def draw_hearing_question():
    font = pygame.font.Font(None, 48)
    text = font.render("Hearing Interval Question Goes Here", True, BLACK)
    text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
    display.blit(text, text_rect)

def draw_turns():
    font = pygame.font.Font(None, 36)
    turns_text = font.render(f"Turns: {turns}, Score: {score}", True, BLACK)
    display.blit(turns_text, (10, 10))  # Draw in the top-left corner

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
    draw_turns()


    font = pygame.font.Font(None, 48)
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
    draw_turns()
    font = pygame.font.Font(None, 48)

    if turns % 2 == 1:
        draw_hearing_question()

    else:
        draw_singing_question()
   
    # Draw back button
    if result_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(display, button_hover_color, result_button_rect)
    else:
        pygame.draw.rect(display, button_color, result_button_rect)
    if turns % 2 == 0:
        result_text = font.render("Sing!", True, WHITE)
    else:
        result_text = font.render("Answer Choice", True, WHITE)

    result_text_rect = result_text.get_rect(center=result_button_rect.center)
    display.blit(result_text, result_text_rect)

def draw_fourth_page():
    display.blit(ending_bg_image, (0, 0))
    draw_turns()

    font = pygame.font.Font(None, 48)
    if score >= 4:
        text = font.render("You escaped!", True, BLACK)
    else:
        text = font.render("You did not escape :(", True, BLACK)
    text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
    display.blit(text, text_rect)


   
    # Draw back button
    if back_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(display, button_hover_color, back_button_rect)
    else:
        pygame.draw.rect(display, button_color, back_button_rect)
    back_text = font.render("Play Again", True, WHITE)
    back_text_rect = back_text.get_rect(center=back_button_rect.center)
    display.blit(back_text, back_text_rect)

def draw_answer_result_page():
    display.blit(question_bg_image, (0, 0))
    draw_turns()

    font = pygame.font.Font(None, 48)
    if correct_ans:
        #global score
        #score += 1
        text = font.render("Correct!", True, BLACK)
    else:
        text = font.render("Incorrect", True, BLACK)
        #answer_processed = True
    text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
    display.blit(text, text_rect)


   
    # Draw back button
    if continue_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(display, button_hover_color, continue_button_rect)
    else:
        pygame.draw.rect(display, button_color, continue_button_rect)
    continue_text = font.render("Continue", True, WHITE)
    continue_text_rect = continue_text.get_rect(center=continue_button_rect.center)
    display.blit(continue_text, continue_text_rect)



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
                turns += 1
            if current_page == PAGE_THIRD and result_button_rect.collidepoint(event.pos):
                if correct_ans:
                    score += 1
                current_page = PAGE_ANS
            if current_page == PAGE_ANS and continue_button_rect.collidepoint(event.pos):
                if turns >= 5:
                    current_page = PAGE_FOURTH #go back to main page
                    turns = 0
                else:
                    current_page = PAGE_SECOND
            if current_page == PAGE_FOURTH and back_button_rect.collidepoint(event.pos):
                current_page = PAGE_MAIN

    if current_page == PAGE_MAIN:
        draw_main_page()
    elif current_page == PAGE_SECOND:
        draw_second_page()
        draw_task_bar()
    elif current_page == PAGE_THIRD:
        draw_third_page()
        draw_task_bar()
    elif current_page == PAGE_FOURTH:
        draw_fourth_page()
        draw_task_bar()
    elif current_page == PAGE_ANS:
        draw_answer_result_page()

    pygame.display.flip()

# Quit Pygame
pygame.quit()
