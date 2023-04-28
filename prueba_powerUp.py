powerup_images = {}
powerup_images['laser_big'] = pygame.image.load(path.join(img_dir, 'power1.png')).convert()
powerup_images['target_stop'] = pygame.image.load(path.join(img_dir, 'power2.png')).convert()
powerup_images['target_fast'] = pygame.image.load(path.join(img_dir, 'power3.png')).convert()
powerup_images['target_slow'] = pygame.image.load(path.join(img_dir, 'power4.png')).convert()

'''
dentro de la clase Sword y la clase Target
self.power=1
self.power_time=pygame.time.get_ticks()
#dentro de update
if self.power>=2:
    if pygame.get_ticks()-self.power_time>POWER_TIME: #se acaba el powerUp, en el siguiente update todo normal
        self.power=1
        self.power_time=pygame.time.get_ticks()
        #vuelta a original
    else:
        #cambio tamaño
        #cambio de velocidad
        pass
else:
    #update original
    
def powerUp(self):
    self.power+=1
    self.power_time=pygame.time.get_ticks() 
    
'''

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['laser_big', 'target_stop', 'target_fast','target_slow'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
            
            
#dentro de refresh en playerf
if random.random()>0.9: #cada 10%
    pos=random
    pow=PowerUp(pos)
    all_sprites.add(pow)
    powerups.add(pow)
    
#dentro de analyse_events
hits = pygame.sprite.spritecollide(sword[side], powerups, True) 
for hit in hits:
        if hit.type == 'laser_big':
            sword.powerUp()
        else:
            target.powerUp()
            if hit.type == 'target_stop':
                target.speed=0 
            else:
                pass #otros cambios a la velocidad
        