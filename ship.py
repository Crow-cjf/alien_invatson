# coding=gbk

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    
    def __init__(self,ai_settings,screen):
        """��ʼ���ɴ����������ʼλ��"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #���طɴ�ͼ�񲢻�ȡ����Ӿ���
        self.image = pygame.image.load(r'images\ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        #�ƶ���־
        self.moving_right = False
        self.moving_left = False
        #��ÿ���·ɴ�������Ļ�ײ�����
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        #���÷ɴ�������center�д洢С��
        self.center = float(self.rect.centerx)
        """rect������ֻ�ܴ洢����ֵ"""
        
    def update(self):
        """�����ƶ���־���·ɴ�λ��"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            '''rect.right�õ����Ǿ����ұ�Ե��x����'''
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left >0 :
            self.center -= self.ai_settings.ship_speed_factor
        #����û��ʹ��elif����Ϊ�����ƶ������ȼ���ͬ����˴���ͬʱ��ס���Ҽ����ɴ������ƶ�
        
        self.rect.centerx = self.center
        
    def blitme(self):
        """��ָ��λ�û��Ʒɴ�"""
        self.screen.blit(self.image,self.rect)
        
    def center_ship(self):
        """���ɴ��ָ�����Ļ����"""
        self.center = self.screen_rect.centerx
