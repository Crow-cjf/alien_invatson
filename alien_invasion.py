#coding=gbk

import pygame

from pygame.sprite import Group
#��Ϸͳ����Ϣ
from game_stats import GameStates
#��Ϸ����
from settings import Settings
#��Ϸ�ɴ�
from ship import Ship
#Play��ť
from button import Button
# ��ʾ����
from scoreboard import Scoreboard
#��Ϸ����
import game_functions as gf

def run_game():
    # ��ʼ����Ϸ
    pygame.init()
    
    #����
    ai_settings = Settings()
    
    #����ʾ
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    #����һ�����ڴ洢��Ϸͳ����Ϣ��ʵ��,�������Ƿ���
    stats = GameStates(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)
    #����һ�ҷɴ��Լ��ӵ��������˱���
    ship = Ship(ai_settings,screen)
    bullets = Group()
    aliens = Group()
    play_button = Button(ai_settings,screen,'PLAY')
    #��ʼ��Ϸ����ѭ��
    while True:
        
        #���Ӽ��̺�����¼�
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            #���·ɴ�λ��
            ship.update()
            #�����ӵ�λ��
            gf.update_bullets(ai_settings,screen,stats,sb,ship,bullets,aliens)
            # ����������λ��
            gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)
        
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)
        
        
run_game()
        
