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

#fonction qui détecte la collision avec une zone donnée (bords gauche et droits en l'occurence : zone du vaisseau)
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