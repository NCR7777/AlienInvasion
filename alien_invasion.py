# Author: nachunrui
# CreateTime: 2021/4/14 22:19
import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet


def _windowed_operation(settings):
    """窗口化运行游戏"""
    return pygame.display.set_mode((settings.screen_width, settings.screen_height))


def _full_screen(settings):
    """全屏运行游戏"""
    screen_rect = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    settings.screen_width = screen_rect.get_rect().width
    settings.screen_height = screen_rect.get_rect().height
    return screen_rect


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()

        if self.settings.screen_height == -1 and self.settings.screen_width == -1:
            # 全屏运行游戏
            self.screen = _full_screen(self.settings)
        else:
            # 窗口化运行游戏
            self.screen = _windowed_operation(self.settings)

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            # 向右移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self, event):
        """相应松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""

        # 每次循环时都重绘屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blit_me()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 监视键盘和鼠标事件
            self._check_events()

            # 加载飞船移动
            self.ship.update()

            # 加载子弹
            self.bullets.update()

            # 更新屏幕上的图像，并切换到新屏幕
            self._update_screen()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
