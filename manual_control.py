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

        # if done:
        #     print('done!')
        #     self.reset()
        # else:
        window.show_grid(img_dict)

    def key_handler(self, event):
        print('pressed', event.key)

        if event.key == 'escape':
            window.close()
            return

        if event.key == 'backspace':
            self.reset()
            return

        if event.key == 'up':
            self.step({'blue': (env.actions.up,)*3, 'red': (env.actions.no_move,)*3})
            return

        if event.key == 'down':
            self.step({'blue': (env.actions.down,)*3, 'red': (env.actions.no_move,)*3})
            return

        if event.key == 'left':
            self.step({'blue': (env.actions.left,)*3, 'red': (env.actions.no_move,)*3})
            return

        if event.key == 'right':
            self.step({'blue': (env.actions.right,)*3, 'red': (env.actions.no_move,)*3})
            return

        if event.key == ' ':
            self.step({'blue': (env.actions.ball,)*3, 'red': (env.actions.no_move,)*3})
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
