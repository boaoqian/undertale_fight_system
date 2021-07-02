from attack import Basic_bullet
from typing import Text, final
import pygame
from Block import *
from Heart import *
import time
import numpy as np


# 开场白
def starting(clock, fps, screen):
    screen = screen
    font = pygame.font.Font('Static/8bitoperator_jve.ttf', 40)
    color = [200, 200, 200]
    text = TextClass(font, 'Press A Key To Start', color)
    screen.blit(text.img, text.target_pos())
    pygame.display.flip()
    pygame.mixer.music.play()
    ok = True
    a = 255
    state = True
    while ok:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                ok = False

            elif event.type == pygame.QUIT:
                ok = False
                pygame.quit()
        # 闪烁
        if a >= 255:
            state = True
        elif a <= 50:
            state = False
        if state:
            a -= 5
        else:
            a += 5
        screen.fill([0, 0, 0])
        text.img.set_alpha(a)
        screen.blit(text.img, text.target_pos())
        clock.tick(fps)
        pygame.display.flip()

    # 清屏，关闭音乐。
    screen.fill([0, 0, 0])
    pygame.display.flip()
    pygame.mixer.music.stop()


class menu:
    def __init__(self,screen,clock,heart) -> None:

        self.screen = screen

        #资源
        self.font = pygame.font.Font('Static/8bitoperator_jve.ttf', 40)
        self.MenuSelect = pygame.mixer.Sound('Static/MenuSelect.ogg')
        self.MenuCursor = pygame.mixer.Sound('Static/MenuCursor.ogg')

        #基本属性
        self.heart = heart
        self.fps = heart.fps

        selet = 0
        self.screen.fill([0, 0, 0])
        menu = self.op(self.font, selet)
        menu_h = menu.get_rect()[-1]
        self.screen.blit(menu, (40, 600-menu_h-10))

        state_bar = State_Bar(hp=heart.HP)
        state_bar_pos = (40, 600-menu_h-60)  # 间隙10+hp_bar宽40+menu+10
        self.screen.blit(state_bar.surface, state_bar_pos)

        clock.tick(self.fps)
        pygame.display.flip()

        text_block = Menu_Text(self.font, 1)
        text_block_pos = [50, state_bar_pos[-1] -
                        text_block.rect[-1]]  # 位置hp_bar宽40-10-self.h
        text = 'welcome to play'
        text_block.write(text)
        self.screen.blit(text_block.surface, text_block_pos)
        pygame.display.flip() 

    def op(self,font, selet):

        op_list = ['FIGHT', 'ACT', 'ITEM', 'MERCY']
        text_list = []
        for i, t in enumerate(op_list):
            if i == selet:
                pos_x = (75, 265, 455, 645)
                text_list.append(TextClass(font, t, color=[255, 215, 0]))
            else:
                pos_x = (75, 265, 455, 645)
                text_list.append(TextClass(font, t))
        h = text_list[0].rect[-1]
        op_surface = pygame.surface.Surface((720, h))
        h //= 2
        for i, t in enumerate(text_list):
            op_surface.blit(t.img, (t.target_pos((pos_x[i], h))))

        return op_surface
