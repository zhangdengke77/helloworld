class Settings():
    # 储存外星人入侵的所有设置的类
    def __init__(self):
        # 初始化游戏的设置
        # 屏幕设置
        self.screen_width = 1400
        self.screen_height = 700
        self.bg_color = (0, 0, 0)


        self.bullet_width = 3#原来是3
        self.bullet_height = 15
        self.bullet_color = 255, 255, 255
        self.bullets_allowed = 100
        #外星人设置
        self.fleet_drop_speed = 10
        #fleet_direction = 1是往右移动， = -1是往左移动

        self.ship_limit = 2
        #以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        #外星人难度增加点数增加
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 3.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        #记分
        self.alien_points = 50

    def increase_speed(self):
        '''提高速度的设置'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)


