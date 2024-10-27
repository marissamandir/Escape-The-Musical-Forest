import pygame
import random
import pyaudio
import librosa
import wave

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
bg_image = pygame.image.load('intro_background_2.png')
bg_image = pygame.transform.scale(bg_image, window_size)

# Load and scale background image for the second page
loading_image = pygame.image.load('loading_background_2.png')
loading_image = pygame.transform.scale(loading_image, window_size)

# load & scale background image for questions page
question_bg_image = pygame.image.load('question_bg_2.png')
question_bg_image = pygame.transform.scale(question_bg_image, window_size)

#load & scale background for the ending page
ending_bg_image = pygame.image.load('ending_background_2.png')
ending_bg_image = pygame.transform.scale(ending_bg_image, window_size)

intro_text_image = pygame.image.load('intro_text.png')
intro_text_image = pygame.transform.scale(intro_text_image, (500, 500))

# Button properties
button_color = GREEN
button_hover_color = (36, 130, 72)

# Define page states
#score = 0
PAGE_MAIN = 0
PAGE_SECOND = 1
PAGE_SINGING_QUESTION = 2
PAGE_HEARING_QUESTION = 3
PAGE_FOURTH = 4
PAGE_ANS = 5
INFO_PAGE = 6
current_page = PAGE_MAIN

main_button_rect = pygame.Rect(450, 500, 200, 50)
next_button_rect = pygame.Rect(450, 400, 200, 50)

first_pitch_button_rect = pygame.Rect(450, 430, 200, 50)
mic_button_rect = pygame.Rect(450, 500, 200, 50)


result_button_rects = [
    pygame.Rect(450, 500, 200, 50),  # First button
    pygame.Rect(450, 570, 200, 50),  # Second button
    pygame.Rect(450, 640, 200, 50)   # Third button
]


back_button_rect = pygame.Rect(450, 400, 200, 50)
continue_button_rect = pygame.Rect(450, 600, 200, 50)
info_button_rect = pygame.Rect(450, 575, 200, 50)
close_button_rect = pygame.Rect(450, 625, 200, 50)

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

intervals_photos = ["fifth.png", "fourth.png", "maj2.png", "maj3.png", "maj6.png", "maj7.png",
                    "min2.png", "min3.png", "min6.png", "min7.png", "octave.png", "Tritone.png", "unison.png"]

sound = pygame.mixer.Sound('intervalsounds/fifth.wav')
c_note = pygame.mixer.Sound('middle c.wav')
background_track = pygame.mixer.Sound('Rainstorms.wav')

notes_png = pygame.image.load('notes.png')
notes_rect = notes_png.get_rect(topleft=(450, 220))

lines = ["You stand at the edge of a dark, tangled forest. \nLegend has it that those who survive the journey \nthrough will find great fortune. \nYour first step crunches the fallen leaves.",
        "The sun is blocked out by thick canopy. \nDespite its name, the forest is silent. \nShadows loom. Still, you press onwards.",
        "You think that night has fallen. \nSomething has awakened, and a strange shape \nrustles through the foliage in the corner of \nyour vision. Watching. Waiting.",
        "You are being chased. \nPointed claws grasp at your back. \nRun! There - in the distance - is that light?",
        "Something awaits..."]

# PITCH DETECTION
def detect_pitch(note_answer):
    note_values = [130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185, 196, 207.65, 220, 233.08, 246.94]
    note_names = ["Unison", "Minor Second", "Major Second", "Minor Third", "Major Third", "Perfect Fourth", "Tritone", "Perfect Fifth", "Minor Sixth", "Major Sixth", "Minor Seventh", "Major Seventh"]
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5  
    WAVE_OUTPUT_FILENAME = "file.wav"
  
    audio = pyaudio.PyAudio()
  
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
    print ("recording...")
    frames = []
  
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print ("finished recording")
  
  
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    #for debugging -- save recorded input as file

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    x, sr = librosa.load(WAVE_OUTPUT_FILENAME)
    #x, sr = librosa.load("intervalsounds/unison.wav")

    r = librosa.autocorrelate(x, max_size=5000)
    hi_sample = 200.0
    lo_sample = 12.0
    t_lo = sr/hi_sample
    t_hi = sr/lo_sample

    r[:int(t_lo)] = 0
    r[int(t_hi):] = 0

    t_max = r.argmax()
    my_freq = float(sr)/t_max
    print(my_freq)
    note_values2 = note_values

    if(my_freq > 126):

        while (not(my_freq >= note_values2[0]-7 and my_freq <= note_values2[11]+7 )):
            for i in range (12):
                note_values2[i] = 2 * note_values2[i]
      
        minValue = 999999
        noteIdentified = 0
        for i in range (12):
    
            if(minValue > abs(my_freq-note_values2[i])):
                minValue = abs(my_freq-note_values2[i])
                noteIdentified = i
                #print(noteIdentified)
      
        return(note_names[noteIdentified]==note_answer)
    
    else:
        return(False)


# PAGE DRAWING METHODS

def render_multiline_text(text, font, color, x, y, line_spacing=5):
    lines = text.split('\n')  # Split the text into lines
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)  # Render each line
        display.blit(text_surface, (x, y + i * (text_surface.get_height() + line_spacing)))  # Blit each line


def draw_task_bar():
    bar_end = 550 * ((score)/max_rounds) -10
    pygame.draw.rect(display, DARK_GREEN, (290, 20, 550, 35))
    pygame.draw.rect(display, GREEN, (297, 27, bar_end, 22))
    pygame.draw.rect(display, BLACK, ((297 + bar_end), 20, 6, 35))
    pygame.draw.rect(display, BLACK, ((297 + bar_end), 20, 17, 9))
    pygame.draw.ellipse(display, BLACK, ((280 + bar_end), 43, 25, 20))
    
def draw_singing_question(singing_num):
    display.blit(question_bg_image, (0, 0))
    draw_turns()
    font = pygame.font.Font(None, 48)

    solfege_img = pygame.image.load(f'intervalimages/{intervals_photos[singing_num]}')
    solfege_img = pygame.transform.scale(solfege_img, (200, 200))
    display.blit(solfege_img, (450, 220))

    

    font = pygame.font.Font(None, 48)
    text = font.render(f"Sing a {intervals_names[singing_num]} - Only sing the second note!", True, BLACK)
    text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2 - 200))
    display.blit(text, text_rect)

    # Draw back button
    if mic_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(display, button_hover_color, mic_button_rect)
    else:
        pygame.draw.rect(display, button_color, mic_button_rect)
    
    mic_text = font.render("Sing!", True, WHITE)
  
    mic_text_rect = mic_text.get_rect(center=mic_button_rect.center)
    display.blit(mic_text, mic_text_rect)

    if first_pitch_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(display, button_hover_color, first_pitch_button_rect)
    else:
        pygame.draw.rect(display, (217, 217, 217), first_pitch_button_rect)
    
    first_pitch_text = font.render("First Pitch", True, BLACK)
  
    first_pitch_text_rect = first_pitch_text.get_rect(center=first_pitch_button_rect.center)
    display.blit(first_pitch_text, first_pitch_text_rect)

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

    if info_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display, button_hover_color, info_button_rect)
    else:
        pygame.draw.rect(display, (217, 217, 217), info_button_rect)
    
    # Draw button text
    text_info = font.render("Info", True, BLACK)
    text_info_rect = text_info.get_rect(center=info_button_rect.center)
    display.blit(text_info, text_info_rect)

def draw_info_page():
    display.blit(bg_image, (0, 0))
    display.blit(intro_text_image, (300, 100))

    mouse_pos = pygame.mouse.get_pos()
    if close_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display, button_hover_color, close_button_rect)
    else:
        pygame.draw.rect(display, RED, close_button_rect)
    
    # Draw button text
    font = pygame.font.Font(None, 36)
    close_text = font.render("Close", True, WHITE)
    text_rect = close_text.get_rect(center=close_button_rect.center)
    display.blit(close_text, text_rect)

   


def draw_loading_page():
    display.blit(loading_image, (0, 0))  # Use the loading image here
    draw_turns()


    font = pygame.font.Font(None, 48)
    render_multiline_text(lines[turns], font, BLACK, 200, 150)
    
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
            if current_page == PAGE_MAIN and info_button_rect.collidepoint(event.pos):
                current_page = INFO_PAGE
            if current_page == INFO_PAGE and close_button_rect.collidepoint(event.pos):
                current_page = PAGE_MAIN
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
                if turns % 2 == 1:
                    current_page = PAGE_HEARING_QUESTION  # Go to third page
                else:
                    current_page = PAGE_SINGING_QUESTION
                    singing_num = random.randint(0, 12)
                    

            if ((current_page == PAGE_HEARING_QUESTION) and (choice_correct.button.collidepoint(event.pos))):
                correct_ans = True
                score += 1
                current_page = PAGE_ANS
            elif ((current_page == PAGE_HEARING_QUESTION) and (result_button_rects[0].collidepoint(event.pos)
                                               or result_button_rects[1].collidepoint(event.pos)
                                               or result_button_rects[2].collidepoint(event.pos))):
                
                correct_ans = False
                current_page = PAGE_ANS
            if current_page == PAGE_HEARING_QUESTION and notes_rect.collidepoint(event.pos):
                if turns % 2 == 1:
                    sound.play()
            
            if current_page == PAGE_SINGING_QUESTION and first_pitch_button_rect.collidepoint(event.pos):
                c_note.play()

            if current_page == PAGE_SINGING_QUESTION and mic_button_rect.collidepoint(event.pos):
                correct_ans = detect_pitch(intervals_names[singing_num])
                if correct_ans:
                    score += 1
                current_page = PAGE_ANS
            if current_page == PAGE_ANS and continue_button_rect.collidepoint(event.pos):
                if score >= 5 or turns >= 5:
                    current_page = PAGE_FOURTH #go back to main page
                    turns = 0
                    score = 0
                else:
                    current_page = PAGE_SECOND
            if current_page == PAGE_FOURTH and back_button_rect.collidepoint(event.pos):
                current_page = PAGE_MAIN

    if current_page == PAGE_MAIN:
        background_track.play()
        draw_main_page()
    elif current_page == PAGE_SECOND:
        background_track.play()
        draw_loading_page()
        draw_task_bar()
    elif current_page == PAGE_SINGING_QUESTION:
        background_track.stop()
        draw_singing_question(singing_num)
        draw_task_bar()
    elif current_page == PAGE_HEARING_QUESTION:
        background_track.stop()
        draw_hearing_question()
        draw_task_bar()
    elif current_page == PAGE_FOURTH:
        background_track.play()
        draw_ending_page()
    elif current_page == PAGE_ANS:
        background_track.play()
        draw_answer_result_page()
        draw_task_bar()
    elif current_page == INFO_PAGE:
        background_track.play()
        draw_info_page()

    pygame.display.flip()

# Quit Pygame
pygame.quit()

