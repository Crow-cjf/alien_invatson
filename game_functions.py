#coding=gbk
import sys
from random import randint
from time import sleep
import pygame
#子弹
from bullet import Bullet
#外星人
from alien import Alien

def check_keydown_events(event,ai_settings,screen,stats,play_button,
            ship,aliens,bullets):
    """响应按键"""
    if event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        stats.game_active = False
        pygame.mouse.set_visible(True)
#因为一个按键对应一个event，同时按下左右将产生两个event，在check_events结束前，moving将都会置位

def check_keyup_events(event,ship):
    """响应松开"""
    if event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_a:
        ship.moving_left = False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """ 响应鼠标和按键事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #退出
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,
                        aliens,bullets,mouse_x,mouse_y)
            
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,stats,play_button,
                        ship,aliens,bullets)
            
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        
def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,
                bullets,mouse_x,mouse_y):
    """在玩家单击PLAY按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        # 重置计分牌图像
        sb.prep_score()
        sb.prep_level()
        sb.prep_high_score()
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        
def update_bullets(ai_settings,screen,stats,sb,ship,bullets,aliens):
    """更新子弹的位置，并删除已经消失的子弹"""
    #更新子弹位置
    bullets.update()
    #删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 检查是否有子弹击中了外星人
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,bullets,aliens)

def check_high_score(stats,sb):
    """检查是否诞生了最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,bullets,aliens):
    """响应外星人和子弹的碰撞"""
    #删除碰撞的外星人和子弹
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
        
    if len(aliens) == 0:
        # 删除现有所有子弹，加快游戏节奏，并创建一个新的外星人群
        bullets.empty()
        ai_settings.increase_speed()
        
        # 提高等级
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings,screen,ship,aliens)
        
def fire_bullet(ai_settings,screen,ship,bullets):
    """如果还没达到限制，就发射一发子弹"""
    if len(bullets) < ai_settings.bullet_allowed:
            # 创建一颗子弹，并将其加入到编组bullets中
            new_bullet = Bullet(ai_settings,screen,ship)
            bullets.add(new_bullet)
            
def get_number_aliens_x(ai_settings,alien_width):
    """计算每行可容纳多少个外星人"""
    # 创建一个外星人，计算一行可容纳多少个外星人
    # 外星人间的间距为外星人的宽度
    available_space_x = ai_settings.screen_width-3*alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    """计算屏幕可以容纳多少行外星人"""
    available_space_y = ai_settings.screen_height - 2*ship_height - 3*alien_height
    number_rows = int(available_space_y / (2 * alien_height) )
    return number_rows
    
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings,screen)
    alien.x = ((1 +2*alien_number)*alien.rect.width +
            randint(-alien.rect.width,alien.rect.width))
    alien.y = ((2 + 2*row_number)*alien.rect.height +
            randint(-alien.rect.height,alien.rect.height))
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    
    
    # 创建外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def check_fleet_edges(ai_settings,aliens):
    """有外星人到达屏幕边缘时采取相应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    """将外星人整群向下移动，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.y +=  ai_settings.alien_drop_speed
        alien.rect.y = alien.y
    
    ai_settings.alien_direction *= -1
        
def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """发生碰撞后响应"""
    if stats.ships_left >0 :
        #剩余飞船数减一
        stats.ships_left -= 1
        
        # 更新记分牌
        sb.prep_ships()
        
        #清空外星人列表和子弹列表
        bullets.empty()
        aliens.empty()
        
        #创建一群新的外星人，并将飞船放到屏幕中间
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        
        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        
def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
            break
            
def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
    
    check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)
     
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    """ 更新屏幕上的图像，并切换到新屏幕"""
    
    #每次循环重新绘制屏幕
    screen.fill(ai_settings.bg_color)
    
    for bullet in bullets:
        bullet.draw_bullet()
   
    #绘制飞船
    ship.blitme()
    #绘制外星人
    aliens.draw(screen)
    #绘制得分
    sb.show_score()
    # 根据情况绘制PLAY按钮
    if not stats.game_active:
        play_button.draw_button()
    
    #注意绘制顺序
    
    # 让最近绘制的屏幕可见
    pygame.display.flip()
    #每次循环时，绘制新屏幕，擦去旧屏幕
            
