import time,pygame,random
from pygame import mixer
snake_speed=10

#window size
window_x= 720
window_y= 480

mixer.init()
mixer.music.set_volume(1)
mixer.Sound("Ilmari Hakkola - Bad Piggies Theme.mp3").play(-1)


#colors
black=pygame.Color(0,0,0) # capital C for pygame.Color(0,0,0)
white=pygame.Color(255,255,255)
red=pygame.Color(255,0,0)
green=pygame.Color(0,255,0)
blue=pygame.Color(0,0,255)

#initialising pygame
pygame.init()

#init game window
pygame.display.set_caption("SNAkES")
game_window=pygame.display.set_mode((window_x, window_y))

#FPS (frames per second) controller
fps=pygame.time.Clock()

#snake default position
snake_position=[100,50]
snake_body=[[100,50],[90,50],[80,50],[70,50]]


#fruit pos
fruit_position = [random.randint(1, (window_x//10)) * 10, random.randint(1, (window_y//10)) * 10]

fruit_spawn= True

#setting default direction for snake
direction="RIGHT"
change_to=direction


# initial score
score = 0
 
# displaying Score function
def show_score(choice, color, font, size):
   
    # creating font object score_font
    score_font = pygame.font.SysFont(font, size)
     
    # create the display surface object
    # score_surface
    score_surface = score_font.render('Score : ' + str(score), True, color)
     
    # create a rectangular object for the
    # text surface object
    score_rect = score_surface.get_rect()
     
    # displaying text
    game_window.blit(score_surface, score_rect)

# game over function
def game_over():
   
    # creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 50)
     
    # creating a text surface on which text
    # will be drawn
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
     
    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect()
     
    # setting position of the text
    game_over_rect.midtop = (window_x/2, window_y/4)
     
    # blit will draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
     
    # after 2 seconds we will quit the (now 1 sec)
    # program
    time.sleep(1)
     
    # deactivating pygame library
    pygame.quit()
    """
    mixer.music.pause()
    mixer.music.unpause()
    mixer.music.pause()
    mixer.music.play()
    mixer.music.pause()
    mixer.music.stop()
    """
    # quit the program
    quit()

# Main Function
while True:
   
    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == pygame.K_ESCAPE:
                #myfont=pygame.font.SysFont('times new roman', 50)
                #pause_text = myfont.render("Paused for 5s",True,blue)
                #rectangle_for_text = pause_text.get_rect()
                #game_window.blit(pause_text,rectangle_for_text)
                time.sleep(5)
 
    # If two keys pressed simultaneously
    # we don't want snake to move into two directions
    # simultaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
 
    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10
 
    # Snake body growing mechanism
    # if fruits and snakes collide then scores will be
    # incremented by 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 1
        mixer.Sound("pop final.mp3").play(0)

        
        #my edit cool for increase
        if snake_speed==100:
            snake_speed+=0.5
        else:
            snake_speed+=1
        #endofedit

        fruit_spawn = False
    else:
        snake_body.pop()
         
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10)) * 10,
                          random.randrange(1, (window_y//10)) * 10]
         
    fruit_spawn = True
    game_window.fill(black)
     
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(
          pos[0], pos[1], 10, 10))
         
    pygame.draw.rect(game_window, white, pygame.Rect(
      fruit_position[0], fruit_position[1], 10, 10))
 
    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x-10:

        if snake_position[0] < 0:
            snake_position[0]=window_x
        else:
            snake_position[0]=0
        #game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y-10:

        if snake_position[1] < 0:
            snake_position[1]=window_y
        else:
            snake_position[1]=0
        #game_over()
     
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()
     
    # displaying score countinuously
    show_score(1, white, 'times new roman', 20)
     
    # Refresh game screen
    pygame.display.update()
 
    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)



