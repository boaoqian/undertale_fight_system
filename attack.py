import pygame
import random
import numpy as np


class Basic_bullet(pygame.sprite.Sprite):
    def __init__(self, available_area, size=20) -> None:
        '''
        surface:传入Avoid_Scene对象
        '''
        color = [255, 255, 255]  # 子弹颜色
        self.size = size
        self.bullet = pygame.surface.Surface([self.size]*2)  # 子弹图像
        self.available_area = available_area
        #self.speed = np.array([random.randrange(-10, 10), random.randrange(-10, 10)])
        self.speed = 6
        pygame.draw.circle(self.bullet,color,[size/2]*2,size/2,0)
        self.out = False

    def setup(self, surface, heart_size, pos=None):
        '''
        surface:传入Avoid_Scene对象\n
        pos：初始位置\n
        若pos为none则随机初始位置
        '''
        if pos == None:
            pos = [random.randint(self.available_area[0], self.available_area[2]),
                   random.randint(self.available_area[1], self.available_area[3])]

        self.pos = np.array(pos,np.float64)
        surface.blit(self.bullet, pos)

        # 碰撞检测中的r
        self.r = (heart_size[0]/2+self.size/2)**2

    # 碰撞检测
    def collision(self, heart_pos):
        p1 = np.array(self.pos)
        p2 = np.array(heart_pos)
        d = np.sum(np.power(p1-p2, 2))
        if d < self.r:
            return True
        else:
            return False

    def action(self, surface ,heart_pos):
        speed = -(self.pos-heart_pos)/np.linalg.norm(self.pos-heart_pos)+np.random.rand(2)*np.random.randint(-1,2,size=2)
        self.pos += speed*self.speed
        for i, p in enumerate(self.pos):
            if p < self.available_area[i] or p > self.available_area[i+2]:
                self.out = True
                self.bullet.fill([0, 0, 0])

        surface.blit(self.bullet, [self.pos[0], self.pos[1]])
