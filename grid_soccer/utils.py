from matplotlib import colors
from enum import IntEnum
import numpy as np


class Actions(IntEnum):
    no_move = 0
    up = 1
    down = 2
    left = 3
    right = 4
    ball = 5


ACTIONS = Actions


class FieldZone(IntEnum):
    left = 0
    middle = 1
    right = 2


FIELD_ZONE = FieldZone


class Layers(IntEnum):
    own_goal = 0
    own_players = 1
    ball = 2
    rival_players = 3
    rival_goal = 4


LAYERS = Layers

# Assign a color to each channel
LAYER_COLORS = {
    LAYERS.own_goal: 'lightgreen',
    LAYERS.own_players: 'green',
    LAYERS.ball: 'blueviolet',
    LAYERS.rival_players: 'darkorange',
    LAYERS.rival_goal: 'wheat'
}


def place_random(region, field_size, num_draws=1):

    # Assign a random set of indices in specified field region
    rand_y = np.random.randint(low=0, high=field_size[0], size=num_draws)

    half = (field_size[1])//2
    middle_split = (field_size[1]-2)//4

    if region is FIELD_ZONE.left:  # field zone left
        # Selects random place on left side of the field
        rand_x = np.random.randint(low=1, high=half - middle_split, size=num_draws)
    elif region is FIELD_ZONE.middle:  # field zone middle
        # Selects random place in the middle of the field
        rand_x = np.random.randint(low=half - middle_split, high=half + middle_split, size=num_draws)
    elif region is FIELD_ZONE.right:  # field zone right
        # Selects random place on right side of the field
        rand_x = np.random.randint(low=half + middle_split, high=field_size[1]-1, size=num_draws)
    else:
        raise ValueError('Invalid field region specified')

    return np.vstack((rand_y, rand_x)).T


# %% Convert channels to colors
def grid_to_img(grid):
    img = np.zeros(grid.shape[:2] + (3,))
    for lyr in LAYERS:
        img = np.maximum(img, np.array(colors.to_rgb(LAYER_COLORS[lyr])) * grid[:, :, lyr:lyr+1])
    return img
