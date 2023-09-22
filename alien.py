# coding=gbk
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """��ʾ���������˵���"""
    def __init__(self,ai_settings,screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #����������ͼ�񣬲�������rect����
        self.image = pygame.image.load(r'images\alien.bmp')
        self.rect = self.image.get_rect()
        
        #ÿ�����������������Ļ���ϽǸ���
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #�洢�����˵�׼ȷλ��
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
    def blitme(self):
        """��ָ��λ�û���������"""
        self.screen.blit(self.image,self.rect)
        
    def check_edges(self):
        """����������Ƿ�����Ļ��Ե�����ǣ�����True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        if self.rect.left <= 0:
            return True
    
    def update(self):
        """�ƶ�������"""
        self.x += (self.ai_settings.alien_speed_factor 
                    * self.ai_settings.alien_direction)
        self.rect.x = self.x
