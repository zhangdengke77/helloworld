import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """这是一个对于飞船子弹进行管理的类"""
    def __init__(self, ai_settings, screen, ship):
        """在飞船所在位置创建一个子弹对象"""
        super(Bullet,self).__init__()
        self.screen = screen

        #下面先画出一个矩形，然后再设置其正确位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        #用小数储存子弹位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """此函数更新子弹移动的位置"""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)