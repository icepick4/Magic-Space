import pygame
from pygame.locals import *
from random import choice,randint,random
pygame.init()

taille_fenetre = (600,600)
fenetreRect = pygame.Rect((35,500), (600,100))
screen = pygame.display.set_mode(taille_fenetre)
timer = pygame.time.Clock()
#création d'une entité possédant une vitesse, une position, et une taille
def usine_entite(rectangle):
    entite={'rect': rectangle,
            'vitesse': (0,0),
            'position': rectangle.topleft}
    return entite
#création d'une entité possédant une vitesse, une position, une taille et des pv
def usine_mob(rectangle,pv):
    entite={'rect': rectangle,
            'vitesse': (0,0),
            'position': rectangle.topleft,
            'pv': pv}
    return entite
#fonction qui modifie la vitesse d'une entite
def changer_vitesse(entite, acceleration):
    vx,vy = entite['vitesse']
    ax,ay = acceleration
    entite['vitesse'] = (vx + ax, vy + ay)
def changer_vitesseJoystick(entite, acceleration):
    ax,ay = acceleration
    entite['vitesse'] = (ax, ay)
#fonction qui modifie la position d'une entite
def changer_position(entite,dt):
    vx,vy = entite['vitesse']
    x,y = entite['position']
    x+= vx * dt
    y+= vy * dt
    entite['position'] = (x,y)
    entite['rect'].topleft = entite['position']
#fonction qui détecte la collision avec une zone donnée (bords gauche et droitsen l'occurence : zone du vaisseau)
def restreindre_position(vaisseau,zone):
    x,y = vaisseau['position']
    largeur,hauteur = vaisseau['rect'].size
    if x < zone.left:
        x = zone.left
    elif x + largeur > zone.right:
        x = zone.right - largeur
    vaisseau['position'] = (x,y)
    vaisseau['rect'].midtop = vaisseau['position']
#fonction qui détecte la collision avec une zone donnée (zone de tir)
def restreindre_fires(fire,zone):
    x,y = fire['position']
    largeur,hauteur = fire['rect'].size
    if y < zone.top:
        return True
#fonction qui détecte la collision avec une zone donnée (zone de mobs)
def restreindre_mobs(mob,zone):
    x,y = mob['position']
    largeur,hauteur = mob['rect'].size
    if y + hauteur > zone.bottom:
        return True
#vaisseau
vaisseauSurface = pygame.image.load("images/vaisseau purple.png").convert_alpha()
vaisseau = usine_entite(vaisseauSurface.get_rect(midbottom=(325,590)))
#mob
mobs = []
vert = pygame.image.load("images/mobs/mob1.png").convert_alpha()
rouge = pygame.image.load("images/mobs/mob2.png").convert_alpha()
bleu = pygame.image.load("images/mobs/mob3.png").convert_alpha()
jaune = pygame.image.load("images/mobs/mob4.png").convert_alpha()
#titre
font_title = pygame.font.SysFont("Trebuchet MS",45)
title = font_title.render("Magic Space", True, (127, 179, 213  ))
titleRect = title.get_rect(midtop=(300,5))
#score
score = 0
font_score = pygame.font.SysFont("Trebuchet MS",30)
scoreSurface = font_score.render("SCORE : {0}".format(score),True,(255,255,255 ))
scoreRect = scoreSurface.get_rect(topleft=(15,15))
#fps
font_fps = pygame.font.SysFont("Trebuchet MS", 30)
fpsSurface = font_fps.render("FPS : {}".format(int(timer.get_fps())),True,(255,255,255 ))
fpsRect = fpsSurface.get_rect(topright=(585,15))
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
lvlRect = lvlSurface.get_rect(midbottom = (415,315))
labelSurface = font_lvl.render("Wave :",True,(255,255,255,125))
labelRect = labelSurface.get_rect(midbottom = (180,315))
#positions
facile = [0,0,1,0,2,3,2,0,1,0,0]
normal = [0,1,1,2,1,3,1,2,1,1,0]
difficile = [1,2,1,3,1,1,3,1,2,1]
hard = [0,2,1,3,4,4,3,1,2,0]
hardcore = [1,2,0,4,4,4,4,0,2,1]
death = [1,1,1,1,4,4,1,1,1,1]
#zones
zoneTir = pygame.Rect((0,70),(600,500))
zoneMobs = pygame.Rect((0,70),(600,430))
#bolléens/variable
continuer = True
fin = False
j = 50
color = "purple"
joy = False
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
        #une touche est pressé
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
                    vaisseau = usine_entite(vaisseauSurface.get_rect(midbottom=(325,590)))
                    color = "blue"
                elif color == "blue":
                    vaisseauSurface = pygame.image.load("images/vaisseau purple.png").convert_alpha()
                    vaisseau = usine_entite(vaisseauSurface.get_rect(midbottom=(325,590)))
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
                labelRect = labelSurface.get_rect(midbottom = (180,315))
                lvlSurface = font_lvl.render("{}".format(lvl),True,(255,255,255,125))
                lvlRect = lvlSurface.get_rect(midbottom = (415,315))
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
            fpsSurface = font_fps.render("FPS : {}".format(int(timer.get_fps())),True,(255,255,255 ))
            fpsRect = fpsSurface.get_rect(topright=(585,15))
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
            j= 50
            if vague == 0:
                lvlSurface = font_lvl.render("{}".format("easy"),True,(255,255,255,125))
                lvlRect = lvlSurface.get_rect(midbottom=(415,315))
                for i in facile:
                    if i == 1:
                        mobs.append(usine_mob(bleu.get_rect(midtop=(j,70)),1))
                        j+=50
                    elif i == 2:
                        mobs.append(usine_mob(rouge.get_rect(midtop=(j,70)),2))
                        j+=50
                    elif i == 3:
                        mobs.append(usine_mob(vert.get_rect(midtop=(j,70)),3))
                        j+=50
                    else:
                        j+=50
            elif vague == 1:
                lvlSurface = font_lvl.render("{}".format("normal"),True,(255,255,255,125))
                lvlRect = lvlSurface.get_rect(midbottom=(415,315))
                for i in normal:
                    if i == 1:
                        mobs.append(usine_mob(bleu.get_rect(midtop=(j,70)),1))
                        j+=50
                    elif i == 2:
                        mobs.append(usine_mob(rouge.get_rect(midtop=(j,70)),2))
                        j+=50
                    elif i == 3:
                        mobs.append(usine_mob(rouge.get_rect(midtop=(j,70)),3))
                        j+=50
                    else:
                        j+=50
            elif vague == 2:
                lvlSurface = font_lvl.render("{}".format("medium"),True,(255,255,255,125))
                lvlRect = lvlSurface.get_rect(midbottom=(415,315))
                for i in difficile:
                    if i == 1:
                        mobs.append(usine_mob(bleu.get_rect(midtop=(j,70)),1))
                        j+=55
                    elif i == 2:
                        mobs.append(usine_mob(rouge.get_rect(midtop=(j,70)),2))
                        j+=55
                    elif i == 3:
                        mobs.append(usine_mob(rouge.get_rect(midtop=(j,70)),3))
                        j+=55
                    else:
                        j+=55
            elif vague == 3:
                lvlSurface = font_lvl.render("{}".format("hard"),True,(255,255,255,125))
                lvlRect = lvlSurface.get_rect(midbottom=(415,315))
                for i in hard:
                    if i == 1:
                        mobs.append(usine_mob(bleu.get_rect(midtop=(j,70)),1))
                        j+=55
                    elif i == 2:
                        mobs.append(usine_mob(rouge.get_rect(midtop=(j,70)),2))
                        j+=55
                    elif i == 3:
                        mobs.append(usine_mob(vert.get_rect(midtop=(j,70)),3))
                        j+=55
                    elif i == 4:
                        mobs.append(usine_mob(jaune.get_rect(midtop=(j,70)),4))
                        j+=55
                    else:
                        j+=55
            elif vague == 4:
                lvlSurface = font_lvl.render("{}".format("expert"),True,(255,255,255,125))
                lvlRect = lvlSurface.get_rect(midbottom=(405,315))
                for i in hardcore:
                    if i == 1:
                        mobs.append(usine_mob(bleu.get_rect(midtop=(j,70)),1))
                        j+=55
                    elif i == 2:
                        mobs.append(usine_mob(rouge.get_rect(midtop=(j,70)),2))
                        j+=55
                    elif i == 3:
                        mobs.append(usine_mob(vert.get_rect(midtop=(j,70)),3))
                        j+=55
                    elif i == 4:
                        mobs.append(usine_mob(jaune.get_rect(midtop=(j,70)),4))
                        j+=55
                    else:
                        j+=55
            elif vague == 5:
                lvlSurface = font_lvl.render("{}".format("DEATH"),True,(255,255,255,125))
                lvlRect = lvlSurface.get_rect(midbottom=(405,315))
                for i in death:
                    if i == 1:
                        mobs.append(usine_mob(bleu.get_rect(midtop=(j,70)),1))
                        j+=55
                    elif i == 2:
                        mobs.append(usine_mob(rouge.get_rect(midtop=(j,70)),2))
                        j+=55
                    elif i == 3:
                        mobs.append(usine_mob(vert.get_rect(midtop=(j,70)),3))
                        j+=55
                    elif i == 4:
                        mobs.append(usine_mob(jaune.get_rect(midtop=(j,70)),4))
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
                    vaisseau = usine_entite(vaisseauSurface.get_rect(midbottom=(325,590)))
                    color = "blue"
                elif color == "blue":
                    vaisseauSurface = pygame.image.load("images/vaisseau purple.png").convert_alpha()
                    vaisseau = usine_entite(vaisseauSurface.get_rect(midbottom=(325,590)))
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
    screen.blit(fpsSurface,fpsRect)
    screen.blit(lvlSurface,lvlRect)
    screen.blit(labelSurface, labelRect)

    # lignes délimitant "sol et plafond" --> zone de tir
    pygame.draw.line(screen, (255,255,255), (0,500),(600,500),3)
    pygame.draw.line(screen, (255,255,255), (0,70),(600,70),3)
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
