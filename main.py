import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

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
#score = 0
PAGE_MAIN = 0
PAGE_SECOND = 1
PAGE_THIRD = 2
PAGE_FOURTH = 3
PAGE_ANS = 4
current_page = PAGE_MAIN

main_button_rect = pygame.Rect(450, 500, 200, 50)
next_button_rect = pygame.Rect(450, 400, 200, 50)

mic_button_rect = pygame.Rect(450, 500, 200, 50)


result_button_rects = [
    pygame.Rect(450, 500, 200, 50),  # First button
    pygame.Rect(450, 570, 200, 50),  # Second button
    pygame.Rect(450, 640, 200, 50)   # Third button
]


back_button_rect = pygame.Rect(450, 400, 200, 50)
continue_button_rect = pygame.Rect(450, 600, 200, 50)

# Answer choice objects
class AnswerChoice:
    @property           
    def name(self): 
        return self._name
    #
    @name.setter   
    def name(self, value):   
        self._name = value  
    @property          
    def correct(self):
        return self._correct
    #
    @correct.setter   
    def correct(self, value):   
        self._correct = value   

    @property           
    def button(self): 
        return self._button
    #
    @button.setter    
    def button(self, value):   
        self._button = value  


# GAMEPLAY VARIABLES
choice_correct = AnswerChoice()
choice_wrong_1 = AnswerChoice()
choice_wrong_2 = AnswerChoice()
max_rounds = 5
turns = 0
global score
score = 0
correct_ans = True
answer_processed = False

intervals_sounds = ["fifth", "fourth", "maj2", "maj3", "maj6", "maj7", "min2", "min3", "min6", "min7",
                    "octave", "tritone", "unison"]

intervals_names = ["Perfect Fifth", "Perfect Fourth", "Major Second", "Major Third", "Major Sixth", "Major Seventh", "Minor Second", "Minor Third", "Minor Sixth", "Minor Seventh",
                    "Octave", "Tritone", "Unison"]

sound = pygame.mixer.Sound('intervalsounds/fifth.wav')

notes_png = pygame.image.load('notes.png')
notes_rect = notes_png.get_rect(topleft=(450, 220))

# PAGE DRAWING METHODS

def draw_task_bar():
    bar_end = 550 * ((score)/max_rounds) -10
    pygame.draw.rect(display, DARK_GREEN, (290, 20, 550, 35))
    pygame.draw.rect(display, GREEN, (297, 27, bar_end, 22))
    pygame.draw.rect(display, BLACK, ((297 + bar_end), 20, 6, 35))
    pygame.draw.rect(display, BLACK, ((297 + bar_end), 20, 17, 9))
    pygame.draw.ellipse(display, BLACK, ((280 + bar_end), 43, 25, 20))
    
def draw_singing_question():
    display.blit(question_bg_image, (0, 0))
    draw_turns()
    font = pygame.font.Font(None, 48)

    font = pygame.font.Font(None, 48)
    text = font.render("Sight-Singing Question Goes Here", True, BLACK)
    text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
    display.blit(text, text_rect)

    # Draw back button
    if mic_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(display, button_hover_color, mic_button_rect)
    else:
        pygame.draw.rect(display, button_color, mic_button_rect)
    
    mic_text = font.render("Sing!", True, WHITE)
  
    mic_text_rect = mic_text.get_rect(center=mic_button_rect.center)
    display.blit(mic_text, mic_text_rect)

def draw_hearing_question():
    display.blit(question_bg_image, (0, 0))
    draw_turns()
    font = pygame.font.Font(None, 48)

    global notes_png
    notes_png = pygame.transform.scale(notes_png, (200, 200))
    display.blit(notes_png, (450, 220))
  
    if result_button_rects[0].collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(display, button_hover_color, result_button_rects[0])
    else:
        pygame.draw.rect(display, button_color, result_button_rects[0])

    if result_button_rects[1].collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(display, button_hover_color, result_button_rects[1])
    else:
        pygame.draw.rect(display, button_color, result_button_rects[1])
    
    if result_button_rects[2].collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(display, button_hover_color, result_button_rects[2])
    else:
        pygame.draw.rect(display, button_color, result_button_rects[2])
  
    result_text1 = font.render(choice_correct.name, True, WHITE)
        #here instead we draw 3 buttons w "answer choice" as text

    result_text_rect1 = result_text1.get_rect(center=choice_correct.button.center)
    display.blit(result_text1, result_text_rect1)

    result_text2 = font.render(choice_wrong_1.name, True, WHITE)
        #here instead we draw 3 buttons w "answer choice" as text

    result_text_rect2 = result_text2.get_rect(center=choice_wrong_1.button.center)
    display.blit(result_text2, result_text_rect2)

    result_text3 = font.render(choice_wrong_2.name, True, WHITE)
        #here instead we draw 3 buttons w "answer choice" as text

    result_text_rect3 = result_text3.get_rect(center=choice_wrong_2.button.center)
    display.blit(result_text3, result_text_rect3)

    font = pygame.font.Font(None, 48)
    text = font.render("Click for music!", True, BLACK)
    text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2 - 180))
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

def draw_loading_page():
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

def draw_ending_page():
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
        #score +=1
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
                turns += 1
                num = random.randint(0, 12)
                interval = f'intervalsounds/{intervals_sounds[num]}.wav'
                sound = pygame.mixer.Sound(interval)

                #down here change the answer choices text
                num2 = random.randint(0, 2)
                num3 = random.randint(0, 12)
                num4 = random.randint(0, 12)
                while(1==1):
                    if((num4 != num3) and (num4 != num) and (num3 != num)):
                        break
                    num3 = random.randint(0, 12)
                    num4 = random.randint(0, 12)
                

                choice_correct.name = intervals_names[num]
                choice_correct.button = result_button_rects[num2]
                choice_wrong_1.name = intervals_names[num3]
                choice_wrong_1.button = result_button_rects[(num2+1)%3]
                choice_wrong_2.name = intervals_names[num4]
                choice_wrong_2.button = result_button_rects[(num2+2)%3]

                #and if correct button is clicked score + 1
                #draw_answer_choices(intervals_sounds[num])
                current_page = PAGE_THIRD  # Go to third page
            if ((current_page == PAGE_THIRD) and (choice_correct.button.collidepoint(event.pos))):
                correct_ans = True
                score += 1
                current_page = PAGE_ANS
            elif ((current_page == PAGE_THIRD) and (result_button_rects[0].collidepoint(event.pos)
                                               or result_button_rects[1].collidepoint(event.pos)
                                               or result_button_rects[2].collidepoint(event.pos))):
                
                correct_ans = False
                current_page = PAGE_ANS
            if current_page == PAGE_THIRD and notes_rect.collidepoint(event.pos):
                if turns % 2 == 1:
                    sound.play()

            if current_page == PAGE_THIRD and mic_button_rect.collidepoint(event.pos):
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
        draw_loading_page()
        draw_task_bar()
    elif current_page == PAGE_THIRD:
        if turns % 2 == 1:
            draw_hearing_question()
        else:
            draw_singing_question()
        draw_task_bar()
    elif current_page == PAGE_FOURTH:
        draw_ending_page()
    elif current_page == PAGE_ANS:
        draw_answer_result_page()
        draw_task_bar()

    pygame.display.flip()

# Quit Pygame
pygame.quit()
