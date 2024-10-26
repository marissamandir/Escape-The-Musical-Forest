import pygame

pygame.init()
display = pygame.display.set_mode((1100, 700)) 
bg_color = (129, 167, 144)
display.fill(bg_color)
pygame.display.flip()
pygame.draw.polygon(display, (36, 130, 72), 
                    [[100, 300], [200, 100],
                     [300, 300]])
pygame.display.update()
running = True
while running: 
    for event in pygame.event.get(): 
          

        if event.type == pygame.QUIT: 
            running = False