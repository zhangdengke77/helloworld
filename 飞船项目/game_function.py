import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

#按键响应
def check_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
        # 飞船向左移动
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
        #创建一颗子弹，并将其编入编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats,sb, play_button ,ship,aliens, bullets):
    # 这个函数整体是监视键盘动作
    for event in pygame.event.get():  # 这个循环是退出机制
        if event.type == pygame.QUIT:
            sys.exit()  #这个是退出的意思

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats,sb, play_button, ship, aliens, bullets,  mouse_x, mouse_y)

            #下面两个elif按下去的时候变成ture抬起来的时候变成false
        elif event.type == pygame.KEYDOWN:
            # 飞船向右移动
            check_keydown_events(event,ai_settings,screen, ship, bullets)
        #抬起键盘来是false
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
def check_play_button(ai_settings, screen, stats, sb,play_button,ship, aliens,bullets, mouse_x,mouse_y):
    '''单机play开始新游戏'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏属性
        ai_settings.initialize_dynamic_settings()
        '''下面的语句是是否能看见鼠标'''
        pygame.mouse.set_visible(False)
        #重置游戏信息
        stats.reset_stats()
        stats.game_active = True

        #重置记分牌图像
        sb.prep_score
        sb.prep_high_score
        sb.prep_level
        sb.prep_ships()

        #清空子弹盒外星人列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()




def update_screen(ai_settings, screen,stats, sb, ship, aliens, bullets, play_button):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 画飞船
    ship.blitme()
    #画外星人
    aliens.draw(screen)
    sb.show_score()
    #如果游戏处于非活动状态就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()
    #显示得分



    # 让最近绘制的屏幕可见
    pygame.display.flip()
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(ai_settings, screen, stats, sb,ship, aliens, bullets)
def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''响应子弹和外星人的碰撞
    删除发生碰撞的子弹和外星人
    '''
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)#第一个改成false子弹无敌，第二个外星人无敌
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        #提高等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)



def get_number_aliens_(ai_settings, alien_width):
    #计算每行可以容纳多少个外星人
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    '''计算屏幕可以容纳多少行外星人'''
    available_space_y = (ai_settings.screen_height- (6 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return  number_rows

def create_alien(ai_settings, screen, aliens, alien_number,row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship,  aliens):
    """创建外星人群"""
    alien = Alien(ai_settings, screen)#创建一个外星人并且测量其宽度和能容纳的数量
    number_aliens_x = get_number_aliens_(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    #开始创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    '''外星人到达边缘应该怎么办'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    '''让外星人群往下移动并且改变方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen,stats,sb,  ship, aliens, bullets):
    '''响应被外星人撞到的飞船'''
    if stats.ships_left > 0:
        stats.ships_left -= 1

        #更新记分牌
        sb.prep_ships()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群外星人，并将飞船放到屏幕低端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen,stats,sb, ship, aliens, bullets):
    '''检查外星人是否到达了底端'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船一样处理
            ship_hit(ai_settings,screen, stats,sb,  ship, aliens, bullets)
            break


def update_aliens(ai_settings,screen, stats,sb, ship, aliens,bullets):
    '''检查是否有外星人位于屏幕边缘，并且更新整群外星人的位置'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings,screen, stats,sb, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, screen,stats,sb, ship, aliens, bullets)

def check_high_score(stats,sb):
    '''检查是否取得最高分'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()









