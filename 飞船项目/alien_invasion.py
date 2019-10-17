import sys

import pygame
from pygame.sprite import Group
# 从settings这个文件里把Settings这个类引进来
from settings import Settings
from ship import Ship
import game_function as gf
from game_stats import GameStats
from button import Button
from scoreborad import Scoreboard


def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    pygame.display.set_caption("Alien Invasion")#定义了窗口的名称



    screen =  pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")#注意不要放到screen前面去
    #创建存储游戏统计的实时信息，并且创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    #创建一艘飞船
    ship = Ship(ai_settings, screen)
    #创建一个用于存储子弹的编组
    bullets = Group()
    #创建一个外星人
    aliens = Group()
    #创建外星人群
    gf.create_fleet(ai_settings,screen, ship,aliens)


    #开始游戏的主循环
    while True:
        gf.check_events(ai_settings, screen, stats,sb, play_button, ship, aliens, bullets)#一定要注意顺序

        #监视鼠标键盘时间
        if stats.game_active:#这样就可以锁住屏幕可操作部分
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings,screen,stats,sb, ship,  aliens, bullets)

        gf.update_screen(ai_settings, screen,stats, sb,ship,aliens,bullets, play_button)

run_game()
