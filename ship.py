# coding=gbk

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    
    def __init__(self,ai_settings,screen):
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load(r'images\ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        #移动标志
        self.moving_right = False
        self.moving_left = False
        #将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        #设置飞船的属性center中存储小数
        self.center = float(self.rect.centerx)
        """rect的属性只能存储整数值"""
        
    def update(self):
        """根据移动标志更新飞船位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            '''rect.right得到的是矩形右边缘的x坐标'''
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left >0 :
            self.center -= self.ai_settings.ship_speed_factor
        #这里没有使用elif是因为左右移动的优先级相同，如此处理同时按住左右键，飞船不会移动
        
        self.rect.centerx = self.center
        
    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)
        
    def center_ship(self):
        """将飞船恢复到屏幕中央"""
        self.center = self.screen_rect.centerx
