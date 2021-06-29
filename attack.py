import pygame
import random

class Basic_bullet(pygame.sprite.Sprite):
    def __init__(self, available_area,size=20) -> None:
        '''
        surface:传入Avoid_Scene对象
        '''
        color = [255,255,255] # 子弹颜色
        self.size = size
        self.bullet = pygame.surface.Surface([self.size]*2) #子弹图像
        self.available_area = available_area
        self.pos = [0,0]
        self.speed = [random.randrange(-4,4),random.randrange(-4,4)]
        self.bullet.fill(color)
        self.out = False

    def setup(self,surface,pos=None):
        '''
        surface:传入Avoid_Scene对象\n
        pos：初始位置\n
        若pos为none则随机初始位置
        '''
        if pos == None:
            pos = [random.randint(self.available_area[0],self.available_area[2]),
                    random.randint(self.available_area[1],self.available_area[3])]  
        if self.speed[0] == 0 and self.speed[1] == 0:
            self.speed = [random.randrange(-4,4),random.randrange(-4,4)]

        self.pos[0] = pos[0]
        self.pos[1] = pos[1]
        surface.blit(self.bullet,pos)

    def action(self,surface):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        for i,p in enumerate(self.pos):
            if p < self.available_area[i] or p > self.available_area[i+2]:
                self.out = True
                self.bullet.fill([0,0,0])

        surface.blit(self.bullet,[self.pos[0],self.pos[1]])


