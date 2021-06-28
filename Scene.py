from typing import Text, final
import pygame
from Block import *
from Heart import *
# 开场白


def starting(clock, fps, screen, font):
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


def menu(clock, fps, screen, font, lv=23, hp=[76, 76]):
    selet = 0
    screen.fill([0, 0, 0])
    menu = op(font, selet)
    menu_h = menu.get_rect()[-1]
    screen.blit(menu, (40, 600-menu_h-10))

    state_bar = State_Bar()
    state_bar_pos = (40, 600-menu_h-60)  # 间隙10+hp_bar宽40+menu+10
    screen.blit(state_bar.surface, state_bar_pos)

    clock.tick(fps)
    pygame.display.flip()
    Running = True
    while Running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    selet += 1
                    if selet > 3:
                        selet = 0
                elif event.key == pygame.K_LEFT:
                    selet -= 1
                    if selet < 0:
                        selet = 3
                screen.fill([0, 0, 0])
                menu = op(font, selet)
                menu_h = menu.get_rect()[-1]
                screen.blit(menu, (40, 600-menu_h-10))
                screen.blit(state_bar.surface, state_bar_pos)
                pygame.display.flip()
        clock.tick(fps)


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
def avoid(clock, fps, screen, font, lv=23, hp=[76, 76]):
    screen.fill([0, 0, 0])
    state_bar = State_Bar()
    state_bar_pos = (40, 600-60)  # 间隙10+hp_bar宽
    screen.blit(state_bar.surface, state_bar_pos)

    avoid_scene = Avoid_Scene((800,400),[250,200])
    avoid_scene_pos = [400-avoid_scene.f_size[0]//2, state_bar_pos[1]-avoid_scene.f_size[1]-10]
    screen.blit(avoid_scene.full_area_surface, avoid_scene_pos)
    pygame.mixer.music.load('Static/MEGALOVANIA.wav')
    pygame.mixer.music.play()

    clock.tick(fps)
    pygame.display.flip()

    Running = True
    press = [0,0] # up down ;right left
    while Running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
        if press[0] != 0 or press[1] != 0 :
            avoid_scene.update(press[0],press[1])
            screen.blit(avoid_scene.full_area_surface, avoid_scene_pos)
            pygame.display.flip()

    pygame.quit()

# pygame.init()
# font = pygame.font.Font('Static/8bitoperator_jve.ttf',40)
# img=Avoid_Scene()
# img.update()
# pygame.image.save(img.surface,"test.png") #这句话保存图片
