import pygame
from pygame.locals import *
from random import choice
from functions import *
pygame.init()

windowSize = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode(windowSize)
fenetreRect = pygame.Rect((35,500), (windowSize[0],windowSize[1]-150))
timer = pygame.time.Clock()

#vaisseau
vaisseauSurface = pygame.image.load("images/vaisseau purple.png").convert_alpha()
vaisseau = usine_entite(vaisseauSurface.get_rect(midbottom=(windowSize[0]/2,windowSize[1]-20)))

#mob
mobs = []
vert = pygame.image.load("images/mobs/mob1.png").convert_alpha()
rouge = pygame.image.load("images/mobs/mob2.png").convert_alpha()
bleu = pygame.image.load("images/mobs/mob3.png").convert_alpha()
jaune = pygame.image.load("images/mobs/mob4.png").convert_alpha()

#titre
font_title = pygame.font.SysFont("Trebuchet MS",45)
title = font_title.render("Magic Space", True, (127, 179, 213  ))
titleRect = title.get_rect(midtop=(windowSize[0]/2,10))

#score
score = 0
font_score = pygame.font.SysFont("Trebuchet MS",30)
scoreSurface = font_score.render("SCORE : {0}".format(score),True,(255,255,255 ))
scoreRect = scoreSurface.get_rect(topleft=(30,30))

pygame.time.set_timer(USEREVENT,250)
pygame.time.set_timer(USEREVENT + 1,5775)

#fire
fireSurface = pygame.image.load("images/fire.png").convert_alpha()
fires = []

#explosion
explosionSurface = pygame.image.load("images/explosion3.png").convert_alpha()
explosions=[]

#lvl
lvl = "?"
font_lvl = pygame.font.SysFont("Trebuchet MS", 70)
font_style = pygame.font.SysFont("Trebuchet MS",25)
lvlSurface = font_lvl.render("{}".format(lvl),True,(255,255,255,125))
lvlRect = lvlSurface.get_rect(midbottom = (windowSize[0]/2 + 150,windowSize[1]/2))
labelSurface = font_lvl.render("Wave :",True,(255,255,255,125))
labelRect = labelSurface.get_rect(midbottom = (windowSize[0]/2,windowSize[1]/2))

#positions
facile = [0,0,1,0,2,3,2,0,1,0,0]
normal = [0,1,1,2,1,3,1,2,1,1,0]
difficile = [1,2,1,3,1,1,3,1,2,1]
hard = [0,2,1,3,4,4,3,1,2,0]
hardcore = [1,2,0,4,4,4,4,0,2,1]
death = [1,1,1,1,4,4,1,1,1,1]

#zones
zoneTir = pygame.Rect((0,70),(windowSize[0],windowSize[1] - 150))
zoneMobs = pygame.Rect((0,70),(windowSize[0],windowSize[1] - 300))

#bolléens/variable
continuer = True
fin = False
j = 50
color = "purple"
joy = False

#bouton end
finFont = pygame.font.SysFont("Trebuchet MS", 50)
finSurface = finFont.render("CLOSE", True, (255,255,255))
finRect = finSurface.get_rect(topright=(windowSize[0]-10,10))

#définition de la musique
pygame.mixer.music.load("sons/music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.04)

while continuer:
    try:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        joy = joystick.get_init()
    except:
        pass
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        #si on appuie sur le bouton close
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
            if windowSize[0]-120 < event.pos[0] < windowSize[0] and 10 < event.pos[1] < 40:
                continuer = False
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                    changer_vitesse(vaisseau, (700,0))
            elif event.key == K_LEFT:
                    changer_vitesse(vaisseau, (-700,0))
            elif event.key == K_SPACE and fin == False:
                    if len(fires) < 3:
                        pygame.mixer.init()
                        tir = pygame.mixer.Sound('sons/tir.mp3')
                        tir.play()
                        tir.set_volume(0.03)
                        fires.append(usine_entite(fireSurface.get_rect(midbottom=vaisseau['position'])))
                    for i in range(len(fires)):
                        if fires[i]['vitesse'] == (0,0):
                            changer_vitesse(fires[i],(0,-350))
            elif event.key == K_TAB and fin == True:
                if color == "purple":
                    vaisseauSurface = pygame.image.load("images/vaisseau.png").convert_alpha()
                    vaisseau = usine_entite(vaisseauSurface.get_rect(midbottom=(windowSize[0]/2,windowSize[1]-20)))
                    color = "blue"
                elif color == "blue":
                    vaisseauSurface = pygame.image.load("images/vaisseau purple.png").convert_alpha()
                    vaisseau = usine_entite(vaisseauSurface.get_rect(midbottom=(windowSize[0]/2,windowSize[1]-20)))
                    color = "purple"
            elif event.key == K_RETURN and fin == True:
                endSurface = font_lvl.render("",True,(255,255,255))
                endRect = endSurface.get_rect(midbottom=(300,375))
                styleSurface = font_style.render("",True,(255,255,255))
                styleRect = styleSurface.get_rect(midbottom=(300,80))
                pygame.mixer.music.unload()
                pygame.mixer.music.load("sons/music.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.04)
                score = 0
                fires = []
                explosions = []
                labelSurface = font_lvl.render("Wave :",True,(255,255,255,125))
                labelRect = labelSurface.get_rect(midbottom = (windowSize[0]/2,windowSize[1]/2))
                lvlSurface = font_lvl.render("{}".format(lvl),True,(255,255,255,125))
                lvlRect = lvlSurface.get_rect(midbottom = (windowSize[0]/2 + 20,windowSize[1]/2 + 20))
                pygame.event.set_allowed(pygame.USEREVENT+1)
                pygame.event.set_allowed(pygame.USEREVENT)
                fin = False

        #une touche est relaché
        elif event.type == KEYUP:
            if event.key == K_RIGHT:
                    changer_vitesse(vaisseau, (-700,0))
            elif event.key == K_LEFT:
                    changer_vitesse(vaisseau, (700,0))
        #event d'affichage des labels
        elif event.type == USEREVENT and fin == False:
            explosions=[]
            scoreSurface = font_score.render("SCORE : {0}".format(score),True,(255,255,255 ))
            scoreRect = scoreSurface.get_rect(topleft=(15,15))
        #event d'affichage des mobs
        elif event.type == USEREVENT + 1 and fin == False:
            if score < 50:
                vague = choice([0,1,2,3])
            elif score >= 50 and score < 100:
                vague = choice([0,1,2,3,4])
            elif score >= 100 and score < 200:
                vague = choice([1,2,3,4,5])
            elif score >= 200:
                vague= choice([1,3,4,5])
            ecart = windowSize[0] // len(facile)
            j = ecart
            if vague == 0:
                lvlSurface = font_lvl.render("{}".format("easy"),True,(255,255,255,125))
                lvlRect = lvlSurface.get_rect(midbottom=(windowSize[0]/2 + 20,windowSize[1]/2 + 20))
                for i in facile:
                    if i == 1:
                        mobs.append(usine_mob(bleu.get_rect(midtop=(j,100)),1))
                        j+=ecart
                    elif i == 2:
                        mobs.append(usine_mob(rouge.get_rect(midtop=(j,100)),2))
                        j+=ecart
                    elif i == 3:
                        mobs.append(usine_mob(vert.get_rect(midtop=(j,100)),3))
                        j+=ecart
                    else:
                        j+=ecart
            elif vague == 1:
                lvlSurface = font_lvl.render("{}".format("normal"),True,(255,255,255,125))
                lvlRect = lvlSurface.get_rect(midbottom=(windowSize[0]/2 + 20,windowSize[1]/2 + 20))
                for i in normal:
                    if i == 1:
                        mobs.append(usine_mob(bleu.get_rect(midtop=(j,100)),1))
                        j+=ecart
                    elif i == 2:
                        mobs.append(usine_mob(rouge.get_rect(midtop=(j,100)),2))
                        j+=ecart
                    elif i == 3:
                        mobs.append(usine_mob(rouge.get_rect(midtop=(j,100)),3))
                        j+=ecart
                    else:
                        j+=ecart
            elif vague == 2:
                lvlSurface = font_lvl.render("{}".format("medium"),True,(255,255,255,125))
                lvlRect = lvlSurface.get_rect(midbottom=(windowSize[0]/2 + 20,windowSize[1]/2 + 20))
                for i in difficile:
                    if i == 1:
                        mobs.append(usine_mob(bleu.get_rect(midtop=(j,100)),1))
                        j+=ecart
                    elif i == 2:
                        mobs.append(usine_mob(rouge.get_rect(midtop=(j,100)),2))
                        j+=ecart
                    elif i == 3:
                        mobs.append(usine_mob(rouge.get_rect(midtop=(j,100)),3))
                        j+=ecart
                    else:
                        j+=ecart
            elif vague == 3:
                lvlSurface = font_lvl.render("{}".format("hard"),True,(255,255,255,125))
                lvlRect = lvlSurface.get_rect(midbottom=(415,315))
                for i in hard:
                    if i == 1:
                        mobs.append(usine_mob(bleu.get_rect(midtop=(j,100)),1))
                        j+=90
                    elif i == 2:
                        mobs.append(usine_mob(rouge.get_rect(midtop=(j,100)),2))
                        j+=90
                    elif i == 3:
                        mobs.append(usine_mob(vert.get_rect(midtop=(j,100)),3))
                        j+=90
                    elif i == 4:
                        mobs.append(usine_mob(jaune.get_rect(midtop=(j,100)),4))
                        j+=90
                    else:
                        j+=90
            elif vague == 4:
                lvlSurface = font_lvl.render("{}".format("expert"),True,(255,255,255,125))
                lvlRect = lvlSurface.get_rect(midbottom=(405,315))
                for i in hardcore:
                    if i == 1:
                        mobs.append(usine_mob(bleu.get_rect(midtop=(j,100)),1))
                        j+=55
                    elif i == 2:
                        mobs.append(usine_mob(rouge.get_rect(midtop=(j,100)),2))
                        j+=55
                    elif i == 3:
                        mobs.append(usine_mob(vert.get_rect(midtop=(j,100)),3))
                        j+=55
                    elif i == 4:
                        mobs.append(usine_mob(jaune.get_rect(midtop=(j,100)),4))
                        j+=55
                    else:
                        j+=55
            elif vague == 5:
                lvlSurface = font_lvl.render("{}".format("DEATH"),True,(255,255,255,125))
                lvlRect = lvlSurface.get_rect(midbottom=(windowSize[0]/2 + 20,windowSize[1]/2 + 20))
                for i in death:
                    if i == 1:
                        mobs.append(usine_mob(bleu.get_rect(midtop=(j,100)),1))
                        j+=55
                    elif i == 2:
                        mobs.append(usine_mob(rouge.get_rect(midtop=(j,100)),2))
                        j+=55
                    elif i == 3:
                        mobs.append(usine_mob(vert.get_rect(midtop=(j,100)),3))
                        j+=55
                    elif i == 4:
                        mobs.append(usine_mob(jaune.get_rect(midtop=(j,100)),4))
                        j+=55
                    else:
                        j+=55
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0 or event.button == 1 or event.button == 2 or event.button == 3 and fin == False:
                if len(fires) < 3:
                    pygame.mixer.init()
                    tir = pygame.mixer.Sound('sons/tir.mp3')
                    tir.play()
                    tir.set_volume(0.03)
                    fires.append(usine_entite(fireSurface.get_rect(midbottom=vaisseau['position'])))
                    for i in range(len(fires)):
                        if fires[i]['vitesse'] == (0,0):
                            changer_vitesse(fires[i],(0,-350))
            elif event.button == 6 and fin == True:
                if color == "purple":
                    vaisseauSurface = pygame.image.load("images/vaisseau.png").convert_alpha()
                    vaisseau = usine_entite(vaisseauSurface.get_rect(midbottom=(windowSize[0]/2,windowSize[1]-20)))
                    color = "blue"
                elif color == "blue":
                    vaisseauSurface = pygame.image.load("images/vaisseau purple.png").convert_alpha()
                    vaisseau = usine_entite(vaisseauSurface.get_rect(midbottom=(windowSize[0]/2,windowSize[1]-20)))
                    color = "purple"
            elif event.button == 7 and fin == True:
                endSurface = font_lvl.render("",True,(255,255,255))
                endRect = endSurface.get_rect(midbottom=(300,375))
                styleSurface = font_style.render("",True,(255,255,255))
                styleRect = styleSurface.get_rect(midbottom=(300,80))
                pygame.mixer.music.load("sons/music.mp3")
                pygame.mixer.music.play(-1)
                score = 0
                fires = []
                explosions = []
                labelSurface = font_lvl.render("Wave :",True,(255,255,255,125))
                labelRect = labelSurface.get_rect(midbottom = (180,315))
                lvlSurface = font_lvl.render("{}".format(lvl),True,(255,255,255,125))
                lvlRect = lvlSurface.get_rect(midbottom = (415,315))
                pygame.mixer.music.set_volume(0.01)
                pygame.event.set_allowed(pygame.USEREVENT+1)
                pygame.event.set_allowed(pygame.USEREVENT)
                fin = False
        elif joy == True:
            direc = 0
            direcNow = joystick.get_axis(0)
            speed = 625
            if -0.1 < direcNow < 0.1:
                vaisseau['vitesse'] = (0,0)
            elif direc < joystick.get_axis(0):
                    changer_vitesseJoystick(vaisseau, (speed*direcNow,0))
            elif direc > joystick.get_axis(0):
                    changer_vitesseJoystick(vaisseau, (speed*direcNow,0))

            direc = joystick.get_axis(0)

#jeu en lui même, gestion des événements et des éléments
    dt = timer.tick(120) / 1000
    #mouvement du vaisseau
    changer_position(vaisseau,dt)
    restreindre_position(vaisseau,fenetreRect)
    for i in range(len(fires)):
        try:
            changer_position(fires[i],dt)
            #détection de collision avec le plafond
            if restreindre_fires(fires[i],zoneTir) == True:
                fires.pop(i)
            for j in range(len(mobs)):
                #détection de collision avec un mob
                if fires[i]['rect'].colliderect(mobs[j]['rect'])== True:

                    mobs[j]['pv']-=1
                    fires.pop(i)
                    if mobs[j]['pv'] == 1:
                        changer_vitesse(mobs[j],(0,55))
                    elif mobs[j]['pv'] == 2:
                        changer_vitesse(mobs[j],(0,50))
                    elif mobs[j]['pv'] == 3:
                        changer_vitesse(mobs[j],(0,30))
                    elif mobs[j]['pv'] == 4:
                        changer_vitesse(mobs[j],(0,25))
                    else:
                        explosionRect=explosions.append(usine_entite(explosionSurface.get_rect(topleft=mobs[j]['position'])))
                        pygame.mixer.init()
                        kill = pygame.mixer.Sound('sons/explosion.mp3')
                        kill.set_volume(0.3)
                        kill.play()

                        mobs.pop(j)
                        score+=1
        except:
            pass
    for i in range(len(mobs)):
        try:
            #déplacement des mobs
            if mobs[i]['vitesse'] == (0,0):
                if mobs[i]['pv'] == 4:
                    if vague == 5:
                        changer_vitesse(mobs[i],(0,55))
                    else:
                        changer_vitesse(mobs[i],(0,25))
                elif mobs[i]['pv'] == 3:
                    changer_vitesse(mobs[i],(0,30))
                elif mobs[i]['pv'] == 2:
                    changer_vitesse(mobs[i],(0,50))
                elif mobs[i]['pv'] == 1:
                    if vague == 5:
                        changer_vitesse(mobs[i],(0,90))
                    else:
                        changer_vitesse(mobs[i],(0,80))
            changer_position(mobs[i],dt)
            #détection de collision avec le sol --> fin de partie
            if restreindre_mobs(mobs[i],zoneMobs) == True:
                #GAME OVER
                fin = True
                pygame.mixer.music.load("sons/son_end.mp3")
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(0.1)
                lvlSurface = font_lvl.render("{}".format(""),True,(255,255,255,125))
                if joy == True:
                    labelSurface = font_lvl.render("Press START",True,(255,255,255,125))
                    styleSurface = font_style.render("Press SELECT to change style",True, (170, 183, 184))
                else:
                    labelSurface = font_lvl.render("Press RETURN",True,(255,255,255,125))
                    styleSurface = font_style.render("Press TAB to change style",True, (170, 183, 184))
                labelRect = lvlSurface.get_rect(midbottom=(120,315))
                styleRect = styleSurface.get_rect(midbottom=(300,120))
                endSurface = font_lvl.render("to restart",True,(255,255,255))
                endRect = endSurface.get_rect(midbottom=(300,375))
                explosions=[]
                mobs = []
                fires=[]
                pygame.event.set_blocked(pygame.USEREVENT+1)
                pygame.event.set_blocked(pygame.USEREVENT)
                pygame.event.clear()
        except:
            pass
#affichage du jeu
    #remplissage fond
    screen.fill((5, 5, 75 ))
    #affichages des labels
    screen.blit(title, titleRect)
    screen.blit(scoreSurface,scoreRect)
    screen.blit(lvlSurface,lvlRect)
    screen.blit(labelSurface, labelRect)
    screen.blit(finSurface,finRect)
    # lignes délimitant "sol et plafond" --> zone de tir
    pygame.draw.line(screen, (255,255,255), (0,windowSize[1]-150),(windowSize[0],windowSize[1]-150),3)
    pygame.draw.line(screen, (255,255,255), (0,100),(windowSize[0],100),3)
    #affichages des tirs

    for i in range(len(fires)):
        screen.blit(pygame.transform.smoothscale(fireSurface, (35,35)),fires[i]['rect'])
    #affichages des mobs
    for i in range(len(mobs)):
        try:
            if mobs[i]['pv'] == 1:
                screen.blit(bleu,mobs[i]['rect'])
            elif mobs[i]['pv'] == 2:
                screen.blit(rouge,mobs[i]['rect'])
            elif mobs[i]['pv'] == 3:
                screen.blit(vert,mobs[i]['rect'])
            elif mobs[i]['pv'] == 4:
                screen.blit(jaune,mobs[i]['rect'])
            else:
                pass
        except:
            pass
    try:
        screen.blit(endSurface,endRect)
        screen.blit(styleSurface,styleRect)
    except:
        pass
    for i in range(len(explosions)):
        screen.blit(explosionSurface,explosions[i]['rect'])
    #affichage du vaisseau
    screen.blit(vaisseauSurface,vaisseau['rect'])
    pygame.display.flip()
pygame.quit()
