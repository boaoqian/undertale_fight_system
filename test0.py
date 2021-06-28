import pygame
from pygame import rect
from pygame.locals import *
from Block import TextClass
from Scene import *

# 初始化设置
pygame.init()
fps = 30
clock = pygame.time.Clock()   #创建一个时间对象

#资源
icon = pygame.image.load('Static/red_heart_big.png')
font = pygame.font.Font('Static/8bitoperator_jve.ttf',40)
bgm = pygame.mixer.music.load('Static/onceupatime.wav')
color = [200,200,200]

#屏幕
pygame.display.set_icon(icon)
pygame.display.set_caption('undertale_FightSystem')
screen = pygame.display.set_mode((800,600)) #不可变
screen.fill([0,0,0])

#主逻辑

def main(screen, clock, fps, font):
    starting(clock,fps,screen,font)
    menu(clock,fps,screen,font)
    avoid(clock,fps,screen,font)
    #menu(clock,fps,screen,font)


if __name__ == '__main__':
    main(screen, clock, fps, font)