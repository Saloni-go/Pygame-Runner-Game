import pygame
from sys import exit  #equivalent to return in functions, just used as is a pygame functionality
from random import randint 

def display_score():
    current_time=int((pygame.time.get_ticks()-start_time)/1000) #gets the current time in milliseconds
    score_surface=test_font.render(f'Score:{current_time}',False,(64,64,64))
    score_rect=score_surface.get_rect(center=(400,50))
    screen.blit(score_surface, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x-=5 

            if obstacle_rect.bottom==250:
                screen.blit(snail_surface,obstacle_rect)
            else:
                screen.blit(fly_surface,obstacle_rect)

        obstacle_list=[obstacle for obstacle in obstacle_list if obstacle.x>-100]  #if obstacle moves and goes to very left, we wont add it in the obstacle _list after wards. 
    else:
        obstacle_list=[]
    return obstacle_list 

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True 
 
def player_animation():
    #walking animation if player is on floor, otherwise the jump surfae when they are not on the floor
    global player_surface, player_index

    if player_rect.bottom<250:
        player_surface=player_jump
    else:
        player_index+=0.1
        if player_index>=len(player_walk):
            player_index=0
        player_surface=player_walk[int(player_index)]

pygame.init() #baiscally initializing our game
screen=pygame.display.set_mode((800,400))
#screen=pygame.display.set_mode((width,height))
#the screen will be created for aplit seconds because after this line the function reaches to the end of the page and by default the function ends
#hence we will create a while(true) loop which will loop forever unless explicitly ended.

pygame.display.set_caption('My_game')

clock=pygame.time.Clock() #very imp as major concern of game makers is how many frame per seconds can that generation pc's can handle, either too fast or too slow both are not feasible.

test_font=pygame.font.Font('font/Pixeltype.ttf',50)
# test_font=pygame.font.Font(None,50)
#test_font=pygame.font.Font(font type, font size)

game_active=False
start_time=0
score=0 #will store current score
obstacle_rect_list=[]

#SKY_SURFACE
sky_surface=pygame.image.load('graphics/Sky.png').convert()
sky_surface=pygame.transform.scale(sky_surface,(800,400))  #bcz sky surface wasnt the same size as that of the display surface, so we need to scale it to fit the screen

#GROUND SURFACE
ground_surface=pygame.image.load('graphics/ground.png').convert()
# ground_surface=pygame.transform.scale(ground_surface, ())

#TEXT SURFACE
# text_surface=test_font.render('My Game', False, (64,64,64))
# #text_surface=test_font.render(text,AA(anti-aliasing),color)
# text_rect=text_surface.get_rect(center=(400,50))

#SNAIL SURFACE
snail_frame_1=pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2=pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames=[snail_frame_1,snail_frame_2]
snail_frame_index=0
snail_surface=snail_frames[snail_frame_index]
# snail_x_pos=700
# snail_rect=snail_surface.get_rect(midbottom=(snail_x_pos,250))

#FLY SURFACE
fly_frame_1=pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2=pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames=[fly_frame_1,fly_frame_2]
fly_frame_index=0
fly_surface=fly_frames[fly_frame_index]
# fly_surface_rect=fly_surface.get_rect(midbottom=(700,100))

#PLAYER SURFACE
player_walk_1=pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2=pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk=[player_walk_1,player_walk_2]
player_jump=pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_index=0

player_surface=player_walk[player_index]

player_rect=player_surface.get_rect(midbottom=(150,250))
player_gravity=0  #we dont wan to do anything before, only when we are pressing the space bar

#PLAYER STAND SURFACE
player_stand=pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand=pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect=player_stand.get_rect(center=(400,200))

#GAME NAME SURFACE
game_name=test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect=game_name.get_rect(center=(400,80))

#GAME MESSAGE
game_message=test_font.render('Press space to run',False,(111,196,169))
game_message_rect=game_message.get_rect(center=(400,340))

#TIMERS
obstacle_timer=pygame.USEREVENT+1  #some events are already reserved for pygame, to reduce conflict we do this

snail_animation_timer=pygame.USEREVENT+2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer=pygame.USEREVENT+3
pygame.time.set_timer(fly_animation_timer,200)

pygame.time.set_timer(obstacle_timer,1500) #trigger this every 900 ms, i.e. less than a second

#SOUND
jump_sound=pygame.mixer.Sound('audio/jump.mp3')
jump_sound.set_volume(0.3)

bg_music=pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops=-1)
bg_music.set_volume(0.1  )

while True:
    for event in pygame.event.get():  #gets us all the events
        if event.type==pygame.QUIT: #quit is a constant in pygame that is snonymous to the cross
            pygame.quit()
            exit()

        if game_active:
            if event.type==pygame.MOUSEBUTTONDOWN :  #only be triggered when mouse is in motion, if mouse click on player happens then also we want the player to jump
                # print(event.pos)

                if player_rect.collidepoint(event.pos) and player_rect.bottom>=250:
                    player_gravity=-20
            # if event.type==pygame.MOUSEBUTTONUP:  #only be triggered when mouse is in motion
            #     print('mouse up')
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and player_rect.bottom>=250:
                    player_gravity=-20
                    jump_sound.play()

            # if event.type==pygame.KEYUP:
                # print('key up')
                    
      
        else:
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                game_active=True 
                # snail_rect.left=800
                start_time=pygame.time.get_ticks()
                
        if game_active:
            if event.type==obstacle_timer:
                if(randint(0,2)):  #will output either 1 : true, or 0 (false)
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900,1100),250)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900,1100),150)))

            if event.type==snail_animation_timer:
                if snail_animation_timer==0:
                    snail_animation_timer=1
                else:
                    snail_animation_timer=0
                snail_surface=snail_frames[snail_frame_index]

            if event.type==fly_animation_timer:
                if fly_frame_index==0:
                    fly_frame_index=1
                else:
                    fly_frame_index=0
                fly_surface=fly_frames[fly_frame_index]

    if game_active:
        screen.blit(sky_surface,(0,0)) #block image transfer
        screen.blit(ground_surface,(0,250))

        # pygame.draw.rect(screen,'#c0e8ec',text_rect)
        # pygame.draw.rect(screen,'#c0e8ec',text_rect,10)

        # screen.blit(text_surface,text_rect)
        score=display_score()
        # screen.blit(snail_surface,snail_rect)

        # snail_rect.x-=4
        # if snail_rect.left<0:
        #     snail_rect.left=800
        
        #PLAYER
        player_gravity+=1
        player_rect.y+=player_gravity 
        if player_rect.bottom >= 250:  # Prevent player from falling through the ground
            player_rect.bottom = 250
            player_gravity = 0  # Reset gravity when on the ground
        player_animation()
        screen.blit(player_surface,player_rect)

        # keys=pygame.key.get_pressed() #will print if something is pressed on not in keyboard

        #ONSTACLE MOVEMENT:
        obstacle_rect_list=obstacle_movement(obstacle_rect_list)
        game_active=collisions(player_rect,obstacle_rect_list)

        #COLLISION
        # if snail_rect.colliderect(player_rect):
            # game_active=False
            # pygame.quit()
            # exit()



    else:
        obstacle_rect_list.clear()
        screen.fill((94,129,162))  #bluish color
        screen.blit(player_stand,player_stand_rect)
        screen.blit(game_name,game_name_rect)
        
        score_message=test_font.render(f'Your score: {score}', False, (111,196,169))
        score_message_rect=score_message.get_rect(center=(400,330))

        if score==0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)

    pygame.display.update()  #updates every change done till now
    clock.tick(60)   #tells that the while loop will run every 60 miliseconds