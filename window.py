import matplotlib.pyplot as plt
import numpy as np

# %matplotlib tk

class Window:
    def __init__(self, img_size):

        self.img_size = img_size

        self.fig = plt.figure()
        self.axes = {
            'blue': self.fig.add_subplot(1, 2, 1),
            'red': self.fig.add_subplot(1, 2, 2),
        }

        for t, ax in self.axes.items():
            ax.set_title(t + ' perspective')
            ax.get_yaxis().set_visible(False)
            ax.get_xaxis().set_visible(False)

        self.img_h = {
            'blue': self.axes['blue'].imshow(np.zeros(self.img_size)),
            'red': self.axes['red'].imshow(np.zeros(self.img_size)),
        }

        self.fig.canvas.set_window_title("Grid Soccer")

        self.closed = False

        def close_handler(evt):
            self.closed = True

        self.fig.canvas.mpl_connect('close_event', close_handler)

    def show_grid(self, img_dict):

        for team, hdl in self.img_h.items():
            hdl.set_data(img_dict[team])
        self.fig.canvas.draw()

        # Let matplotlib process UI events
        # This is needed for interactive mode to work properly
        plt.pause(0.001)

    def reg_key_handler(self, key_handler):
        self.fig.canvas.mpl_connect('key_press_event', key_handler)

    def show(self, block=True):
        # If not blocking, trigger interactive mode
        if not block:
            plt.ion()

        # Show the plot
        # In non-interative mode, this enters the matplotlib event loop
        # In interactive mode, this call does not block
        plt.show()

    def close(self):
        plt.close()


if __name__ == '__main__':
    window = Window()
