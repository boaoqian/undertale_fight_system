from attack import Basic_bullet
from typing import Text, final
import pygame
from Block import *
from Heart import *
import time
import numpy as np

class Setting:
    def __init__(self) -> None:
        self.pos={}

setting = Setting()

def starting(clock, fps, screen):
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


def get_font_size(font, text):
    text = font.render(text, 0, [0, 0, 0])
    return text.get_rect()[-2:]

# 选项


def op(font, selet):

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

# 菜单界面（待完善）


def quit_now():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()


def menu(clock, fps, screen, text, lv=23, hp=[76, 76]):

    font = pygame.font.Font('Static/8bitoperator_jve.ttf', 40)
    MenuSelect = pygame.mixer.Sound('Static/MenuSelect.ogg')
    MenuCursor = pygame.mixer.Sound('Static/MenuCursor.ogg')
    selet = 0
    screen.fill([0, 0, 0])
    menu = op(font, selet)
    menu_h = menu.get_rect()[-1]
    screen.blit(menu, (40, 600-menu_h-10))

    state_bar = State_Bar(hp=hp)
    state_bar_pos = (40, 600-menu_h-60)  # 间隙10+hp_bar宽40+menu+10
    screen.blit(state_bar.surface, state_bar_pos)
    setting.pos['state_bar_pos']=state_bar_pos

    clock.tick(fps)
    pygame.display.flip()

    text_block = Menu_Text(font, 1)
    text_block_pos = [50, state_bar_pos[-1] -
                      text_block.rect[-1]]  # 位置hp_bar宽40-10-self.h
    
    for l in text:
        text_block.write_letter(l)
        screen.blit(text_block.surface, text_block_pos)
        pygame.display.flip()
        pygame.time.delay(30)

    # 玩家时间
    Running = True
    while Running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    MenuSelect.play()
                    Running = False
                    pygame.display.flip()
                    return selet

                elif event.key == pygame.K_RIGHT:
                    MenuCursor.play()
                    selet += 1
                    if selet > 3:
                        selet = 0
                elif event.key == pygame.K_LEFT:
                    MenuCursor.play()
                    selet -= 1
                    if selet < 0:
                        selet = 3
                menu = op(font, selet)
                menu_h = menu.get_rect()[-1]
                screen.blit(menu, (40, 600-menu_h-10))
                pygame.display.flip()


# 画场景和心
def avoid_draw():
    size = [300, 300]
    heart_path = 'Static/red_heart.png'
    surface = pygame.surface.Surface(size)
    heart = Heart(heart_path, 76, (size[0]/2, size[1]/2))
    pos = heart.target_pos(heart.pos)
    # surface,color,pos,widht
    pygame.draw.rect(surface, [255, 255, 255], (0, 0, size[0], size[1]), 5)
    surface.blit(heart.heart_img, pos)
    return surface

# 躲避攻击的场景


def die(screen):
    screen.fill([0, 0, 0])
    s = pygame.mixer.Sound('Static/HeartShatter.ogg')
    img = pygame.image.load('Static/red_heart.png')
    s_img = pygame.image.load('Static/s_heart.png')

    screen.blit(img, [390, 290])
    pygame.display.flip()
    pygame.time.delay(1000)
    s.play()
    screen.fill([0, 0, 0])
    screen.blit(s_img, [390, 290])
    pygame.display.flip()
    pygame.time.delay(1500)
    screen.fill([0, 0, 0])


def animation(pos1, pos2, screen, times):
    d_x = (pos1[0] - pos2[0])/times
    d_y = (pos1[1] - pos2[1])/times
    d_w = (pos1[2] - pos2[2])/times
    d_h = (pos1[3] - pos2[3])/times
    mask=[0,0,800,setting.pos['state_bar_pos'][-1]+60]
    for i in range(times):
        pygame.draw.rect(screen,[0,0,0],mask,0)
        pos = [pos1[0]-d_x*i, pos1[1]-d_y*i, pos1[2]-d_w*i, pos1[3]-d_h*i]
        pygame.draw.rect(screen,[255,255,255],pos,5)
        pygame.display.flip()
        pygame.time.delay(10)


def avoid(clock, fps, screen,hp=76):
    screen.fill([0, 0, 0])
    state_bar = State_Bar(hp=[hp, 76])
    state_bar_pos = (40, 600-60)  # 间隙10+hp_bar宽
    screen.blit(state_bar.surface, state_bar_pos)

    # 初始化avoid_scene
    avoid_scene = Avoid_Scene([10, 10, 3, 1], (400, 400), hp, [200, 200])
    avoid_scene_pos = [400-avoid_scene.f_size[0]//2,
                       state_bar_pos[1]-avoid_scene.f_size[1]-10]
    screen.blit(avoid_scene.full_area_surface, avoid_scene_pos)
    pygame.mixer.music.load('Static/MEGALOVANIA.wav')
    pygame.mixer.music.play()

    start_time = time.time()
    finish_time =  10# 游戏时间
    clock.tick(fps)
    pygame.display.flip()

    Running = True
    press = [0, 0]  # up down ;right left
    while Running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                Running = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP and press[1] == 1:
                    press[1] = 0
                elif event.key == pygame.K_DOWN and press[1] == -1:
                    press[1] = 0
                elif event.key == pygame.K_LEFT and press[0] == -1:
                    press[0] = 0
                elif event.key == pygame.K_RIGHT and press[0] == 1:
                    press[0] = 0

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    press[1] = 1
                elif event.key == pygame.K_DOWN:
                    press[1] = -1
                elif event.key == pygame.K_LEFT:
                    press[0] = -1
                elif event.key == pygame.K_RIGHT:
                    press[0] = 1
        state_bar.hp[0] = avoid_scene.heart.HP
        state_bar.update_state()
        avoid_scene.update(press[0], press[1])
        screen.blit(avoid_scene.full_area_surface, avoid_scene_pos)
        screen.blit(state_bar.surface, state_bar_pos)
        pygame.display.flip()

        if time.time()-start_time >= finish_time:
            pygame.mixer.music.fadeout(1000)
            pos1 = [avoid_scene_pos[0], avoid_scene_pos[1], avoid_scene.f_size[0],avoid_scene.f_size[1]]
            pos2 = [50,284,700,200]
            animation(pos1,pos2,screen,30)
            Running = False
            return avoid_scene.heart.HP

        elif avoid_scene.heart.is_dead():
            pygame.mixer.music.stop()
            die(screen)
            Running = False
            return 76


def fight(clock,fps,screen):
    sound = pygame.mixer.Sound('Static/playerfight.ogg')
    target = pygame.image.load('Static/target.png')

    surface = pygame.surface.Surface(target.get_rect()[-2:])
    pygame.draw.rect(surface,[255,255,255],surface.get_rect(),5)

    start = 0
    final = target.get_rect()[2]
    times = 50
    d_x = (final-start)/times
    pos = [50,setting.pos['state_bar_pos'][-1]-surface.get_rect()[-1]-10]

    surface.blit(target,[0,0])
    pygame.draw.rect(surface,[255,255,255],[start,15,10,120])
    pygame.draw.rect(screen,[0,0,0],[0,0,800,setting.pos['state_bar_pos'][-1]-1])
    screen.blit(surface,pos)
    pygame.display.flip()
    pygame.time.delay(500)
    hit = False
    for _ in range(times):
        if hit:
            break
        start += d_x
        surface.fill([0,0,0])
        pygame.draw.rect(surface,[255,255,255],surface.get_rect(),5)
        surface.blit(target,[0,0])
        pygame.draw.rect(surface,[255,255,255],[start,15,10,120])
        screen.blit(surface,pos)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    sound.play()
                    pygame.time.delay(500)
                    hit = True

        clock.tick(fps)



def act(clock, fps, screen):
    pass


def item(clock, fps, screen):
    pass


def mercy(clock, fps, screen):
    pass
