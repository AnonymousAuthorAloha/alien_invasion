class GameStates:
    """跟踪游戏统计信息"""
    def __init__(self,ai_game):
        """初始统计信息"""
        self.settings=ai_game.settings
        self.reset_stats()
        #游戏启东时处于活动状态
        self.game_active=False

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ship_left=self.settings.ship_limit