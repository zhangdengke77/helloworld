import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_settings,screen):
        super(Ship,self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        #加载飞船图像并获取其外接矩形，rect是位置信息
        self.image = pygame.image.load(r'D:\python代码\飞船项目\ship_1.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()


        #将每艘新飞船放在屏幕底部中心，飞船的中心是屏幕的中心，飞船的底部是屏幕的底部
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #在飞船的属性center中存储小数位
        self.center = float(self.rect.centerx)

        #移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船位置"""
        #判断是否按下去了，并且方块的right小于屏幕的right
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left> 0:
            self.center -= self.ai_settings.ship_speed_factor
        #根据self.center更新rect对象
        self.rect.centerx = self.center

    def blitme(self):
        #在指定位置绘制飞船
        self.screen.blit(self.image,self.rect)
    def center_ship(self):
        '''让飞船在屏幕上居中'''
        self.center = self.screen_rect.centerx