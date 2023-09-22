#coding=gbk

import pygame

from pygame.sprite import Group
#游戏统计信息
from game_stats import GameStates
#游戏设置
from settings import Settings
#游戏飞船
from ship import Ship
#Play按钮
from button import Button
# 显示分数
from scoreboard import Scoreboard
#游戏功能
import game_functions as gf

def run_game():
    # 初始化游戏
    pygame.init()
    
    #设置
    ai_settings = Settings()
    
    #主显示
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    #创建一个用于存储游戏统计信息的实例,并创建记分牌
    stats = GameStates(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)
    #创建一艘飞船以及子弹和外星人编组
    ship = Ship(ai_settings,screen)
    bullets = Group()
    aliens = Group()
    play_button = Button(ai_settings,screen,'PLAY')
    #开始游戏的主循环
    while True:
        
        #监视键盘和鼠标事件
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            #更新飞船位置
            ship.update()
            #更新子弹位置
            gf.update_bullets(ai_settings,screen,stats,sb,ship,bullets,aliens)
            # 更新外星人位置
            gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)
        
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)
        
        
run_game()
        
