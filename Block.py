import pygame
from attack import *
from Heart import *
import numpy as np

class TextClass:
    def __init__(self, font, text, color=[255,255,255]):
        #写字
        text = font.render(text, 0, color)
        t_rect = text.get_rect()
        #画框
        w = 20  # 框宽
        self.img = pygame.surface.Surface((t_rect[-2]+w,t_rect[-1]+w))
        self.rect = self.img.get_rect()
        pygame.draw.rect(self.img, color, self.rect,w//4)
        
        #画
        self.img.blit(text,(w//2,w//2))

    # 居中画图
    def target_pos(self, pos=(400,300)):
            pos = (pos[0]-self.rect[-2]//2,pos[1]-self.rect[-1]//2)
            return pos


class State_Bar:
    def __init__(self,lv=23,hp=[76,76]):
        self.color = [255,255,255]
        self.font = pygame.font.Font('Static/8bitoperator_jve.ttf',35)
        self.text_bar_w = [245,455] #控制文字的宽
        self.hp_bar_w = [250,450]   #控制hp宽
        self.bar_legth=self.hp_bar_w[1]-self.hp_bar_w[0]
        self.hp_bar_h = 33
        self.surface = pygame.surface.Surface((800,40))
        lv_text = self.font.render(f'LV {lv}', 0, self.color)
        hp_text = self.font.render(f'HP {hp[0]}/{hp[1]}', 0, self.color)

        self.lv = lv
        self.hp = hp

        pygame.draw.rect(self.surface, [255,215,0], [self.hp_bar_w[0],(40-self.hp_bar_h)//2,(self.bar_legth)*hp[0]//hp[1],self.hp_bar_h], 0) #画hp条【300-500px】
        lv_pos = lv_text.get_rect()[-2]
        self.surface.blit(lv_text,[self.text_bar_w[0]-lv_pos,0])
        self.surface.blit(hp_text,[self.text_bar_w[1],0])

    # 状态栏
    def update_state(self):
        self.surface.fill([0,0,0])
        lv_text = self.font.render(f'LV {self.lv}', 0, self.color)
        hp_text = self.font.render(f'HP {self.hp[0]}/{self.hp[1]}', 0, self.color)
        pygame.draw.rect(self.surface, [255,215,0], [self.hp_bar_w[0],(40-self.hp_bar_h)//2,(self.bar_legth)*self.hp[0]//self.hp[1],self.hp_bar_h], 0) #画hp条【300-500px】
        lv_pos = lv_text.get_rect()[-2]
        self.surface.blit(lv_text,[self.text_bar_w[0]-lv_pos,0])
        self.surface.blit(hp_text,[self.text_bar_w[1],0])

class Avoid_Scene:
    def __init__(self,size=[300,300],pos=[150,150],bk=[50,50]) -> None:
        '''
        size: 区域大小
        pos: heart的初始位置\n
        self.surface是区块结果
        '''
        self.HP = 76
        self.color = [255,255,255]
        self.f_size = size #区域大小
        self.bk = bk #越大，可动区相对区域越小
        self.size = [size[0]-bk[0],size[1]-bk[1]] #可动区域大小
        self.bk = [bk[0]//2,bk[1]//2]   #保证可动区居中
        heart_path = 'Static/red_heart.png'
        
        #资源
        self.playerdamaged = pygame.mixer.Sound('Static/playerdamaged.ogg')

        # heart 初始化
        self.heart = Heart(heart_path,self.HP,(self.size[0]/2,self.size[1]/2))
        self.heart.pos=pos
        pos = self.heart.target_pos(self.heart.pos)
        heart_size = self.heart.heart_img.get_rect()[-2:]

        # heart可活动的区域
        self.available_area=[6+heart_size[0]//2, 6+heart_size[1]//2, self.size[0]-6-heart_size[0]//2,self.size[1]-6-heart_size[1]//2]
        self.full_area_surface = pygame.surface.Surface(self.f_size)
        self.surface = pygame.surface.Surface(self.size)
        pygame.draw.rect(self.surface,[255,255,255],(0,0,self.size[0],self.size[1]),5) #surface,color,pos,widht

        # 子弹初始化
        bullet_num = 12
        self.bullet_size = 10
        self.bullet_group = []
        for _ in range(bullet_num):
            bullet = Basic_bullet(self.available_area,self.bullet_size)
            bullet.setup(self.surface)
            self.bullet_group.append(bullet)

        #碰撞检测中的r
        self.r = (heart_size[0]/2+self.bullet_size/2)**2

        self.surface.blit(self.heart.heart_img,pos)
        self.full_area_surface.blit(self.surface,self.bk)

    # 碰撞检测 
    def collision(self,pos_1,pos_2):
        p1 = np.array(pos_1)
        p2 = np.array(pos_2)
        d = np.sum(np.power(p1-p2,2))
        if d < self.r:
            return True
        else:
            return False

    def update(self,d_x,d_y):
        '''
        d_x,d_y: 为位置变化量 (单位：px)
        '''
        self.heart.pos[0] += d_x*self.heart.speed
        self.heart.pos[1] -= d_y*self.heart.speed

        # 防止跑出边框
        for i,p in enumerate(self.heart.pos):
            if p < self.available_area[i]:
                self.heart.pos[i] = self.available_area[i]
            elif p > self.available_area[i+2]:
                self.heart.pos[i] = self.available_area[i+2]
        
        self.surface.fill([0,0,0])
        self.full_area_surface.fill([0,0,0])
        pygame.draw.rect(self.surface,[255,255,255],(0,0,self.size[0],self.size[1]),5) #surface,color,pos,widht
        pos = self.heart.target_pos(self.heart.pos)

        # 子弹更新
        for i, bullet in enumerate(self.bullet_group):
            if self.collision(bullet.pos,self.heart.pos):
                self.bullet_group[i].out=True
                self.heart.HP -= 3
                self.playerdamaged.stop()
                self.playerdamaged.play()
                
            if bullet.out:
                bullet = Basic_bullet(self.available_area, self.bullet_size)
                bullet.setup(self.surface)
                self.bullet_group[i] = bullet
            
            bullet.action(self.surface)

        
        self.surface.blit(self.heart.heart_img,pos)
        self.full_area_surface.blit(self.surface,self.bk)

        