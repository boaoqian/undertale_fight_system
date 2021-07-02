import pygame

class Heart(pygame.sprite.Sprite):
    def __init__(self, imgfile, hp, pos=[]):
        super().__init__()

        self.heart_img = pygame.image.load(imgfile)
        self.rect = self.heart_img.get_rect()
        self.pos = pos
        self.HP = hp
        self.speed = 7
        self.Invincible = 0 #受到攻击后的无敌时间

    # 裂开的特效（待完善） ；return 是否活着
    def is_dead(self):
        if self.HP <= 0:
            return True
        else:
            return False

    # 居中画图
    def target_pos(self, pos):
            pos = (pos[0]-self.rect[-2]//2,pos[1]-self.rect[-1]//2)
            return pos
