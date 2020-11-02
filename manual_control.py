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

        if done:
            print('done!')
            self.reset()
        else:
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
            self.step(env.actions.up)
            return
        if event.key == 'down':
            self.step(env.actions.down)
            return
        if event.key == 'left':
            self.step(env.actions.left)
            return
        if event.key == 'right':
            self.step(env.actions.right)
            return


if __name__ == '__main__':

    env = SoccerGridWorld()
    window = Window(img_size=(env.height, env.width, 3))
    man_ctrl = ManualController(env=env)
    window.reg_key_handler(man_ctrl.key_handler)

    man_ctrl.reset()

    # Blocking event loop
    window.show(block=True)
