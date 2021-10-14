import pygame

class Ship:
    """管理飞船的类"""

    def __init__(self,ai_game):
        """初始化飞船并设置其初始位置"""
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()
        self.settings=ai_game.settings

        #在飞船的属性x中存储小数值

        #加载飞船图像并获取其外界矩形
        self.image=pygame.image.load('images/Trump_gun_new.bmp')
        self.rect=self.image.get_rect()


        #对于每艘新飞船，都将其放入屏幕中底部
        self.rect.midbottom=self.screen_rect.midbottom

        self.x=float(self.rect.x)
        self.y=float(self.rect.y)

        #移动标志
        self.moving_right=False
        self.moving_left=False
        self.moving_up=False
        self.moving_down=False

    def update(self):
        """根据移动标志调整飞船位置"""
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.x+=self.settings.ship_speed
        if self.moving_left and self.rect.left>self.screen_rect.left:
            self.x-=self.settings.ship_speed
        if self.moving_up and self.rect.top>self.screen_rect.top:
            self.y-=self.settings.ship_speed
        if self.moving_down and self.rect.bottom<self.screen_rect.bottom:
            self.y+=self.settings.ship_speed

        self.rect.x=self.x
        self.rect.y=self.y

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        self.rect.midbottom=self.screen_rect.midbottom
        self.x,self.y=float(self.rect.x),float(self.rect.y),
