import sys
import numpy as np
from grid_soccer.gridwolrd import SoccerGridWorld
from window import Window


class ManualController:
    def __init__(self, env):
        self.controlled_player = 0
        self.env = env

    def reset(self,):
        state = env.reset()
        img_dict = env.render()
        window.show_grid(img_dict)

    def step(self, action):
        state, reward, done, info = env.step(action)
        img_dict = env.render()
        # print('action=%d, reward=%.2f' % (action, reward))

        if done['blue'] or done['red']:
            print('done!')
            self.reset()
        # else:
        window.show_grid(img_dict)

    def key_handler(self, event):
        print('pressed', event.key)

        default_action = [env.actions.no_move, ] * 3

        if event.key == 'escape':
            window.close()
            return

        if event.key == 'backspace':
            self.reset()
            return

        if event.key == '1':
            self.controlled_player = 1
            return

        if event.key == '2':
            self.controlled_player = 2
            return

        if event.key == '3':
            self.controlled_player = 3
            return

        if event.key == 'up':
            act = default_action.copy()
            act[self.controlled_player-1] = env.actions.up
            self.step({'blue': act, 'red': default_action})
            return

        if event.key == 'down':
            act = default_action.copy()
            act[self.controlled_player-1] = env.actions.down
            self.step({'blue': act, 'red': default_action})
            return

        if event.key == 'left':
            act = default_action.copy()
            act[self.controlled_player-1] = env.actions.left
            self.step({'blue': act, 'red': default_action})
            return

        if event.key == 'right':
            act = default_action.copy()
            act[self.controlled_player-1] = env.actions.right
            self.step({'blue': act, 'red': default_action})
            return

        if event.key == ' ':
            act = default_action.copy()
            act[self.controlled_player-1] = env.actions.ball
            self.step({'blue': act, 'red': default_action})
            return


if __name__ == '__main__':

    env = SoccerGridWorld()
    (env.actions.down, ) * 3
    window = Window(img_size=(env.height, env.width, 3))
    man_ctrl = ManualController(env=env)
    window.reg_key_handler(man_ctrl.key_handler)

    man_ctrl.reset()

    # Blocking event loop
    window.show(block=True)
