import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_states import GameStates
from button import Button

class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings=Settings()

        self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        # self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width=self.screen.get_rect().width
        self.settings.screen_height=self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')

        self.stats=GameStates(self)

        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()

        self._creat_fleet()

        self.moving_right=False

        #绘制Play按钮
        self.play_button=Button(self,"play")


    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.stats.game_active:
                """监视键盘和鼠标事件"""
                self.ship.update()
                self.bullets.update()

                #删除消失子弹
                self._update_bullets()

                self._update_aliens()

                #每次循环重绘屏幕
                #让最近绘制的屏幕可见
            self._update_screen()


    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
               self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_keydown_events(self,event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key==pygame.K_q or event.key==pygame.K_ESCAPE:
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self,event):
        """响应松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False


    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中。"""
        if len(self.bullets)<self.settings.bullet_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        #更新子弹位置
        self.bullets.update()
        #删除消失的子弹
        self._delete_disappeared_bullet()
        #检查是否有子弹击中敌人
        #若击中，则删除相应子弹和外星人
        self._check_bullet_alien_collision()


    def _check_bullet_alien_collision(self):
        """响应子弹和外星人碰撞"""
        #删除发生碰撞的子弹和外星人
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if not self.aliens:
            self.bullets.empty()
            self._creat_fleet()


    def _delete_disappeared_bullet(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)


    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #若游戏处于非活动状态，就绘制Play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


    def _creat_fleet(self):
        alien=Alien(self)
        alien_width=alien.rect.width
        alien_height=alien.rect.height
        ship_height=self.ship.rect.height

        available_space_x=self.screen.get_rect().width-2*alien_width
        number_aliens_x=available_space_x//(2*alien_width)

        available_space_y=self.screen.get_rect().height-3*alien_height-ship_height
        number_rows=available_space_y//(2*alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._creat_alien(alien_number,row_number)


    def _creat_alien(self,alien_number,row_number):
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        alien.x=(alien_number*2+1)*alien_width
        alien.y=(row_number*2+1)*alien_height
        alien.rect.x=alien.x
        alien.rect.y=alien.y
        self.aliens.add(alien)


    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()


    def _ship_hit(self):
        if self.stats.ship_left>0:
            self.stats.ship_left-=1

            self.aliens.empty()
            self.bullets.empty()

            self._creat_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active=False


    def _check_fleet_edges(self):
        for  alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1


    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕底端"""
        screen_rect=self.screen.get_rect()
        for alien in self.aliens:
            if alien.rect.bottom>=screen_rect.bottom:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        """在玩家单击Play按钮时开始新的游戏"""
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #重置游戏统计信息

            self.stats.game_active=True

            #清空余下的外星人和子弹。
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人并让飞船居中
            self._creat_fleet()
            self.ship.center_ship()


if __name__=='__main__':
    # 创建游戏实例并运行游戏
    ai=AlienInvasion()
    ai.run_game()
