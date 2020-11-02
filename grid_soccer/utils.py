from matplotlib import colors
from enum import IntEnum
import numpy as np


class Actions(IntEnum):
    up = 0
    down = 1
    left = 2
    right = 3
    ball = 4


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


# %% Check that movement is valid
def check_valid_move(pos, action, grid):
    assert action.real < 4  # only should be called on movement actions

    # Ignore goal layers and perform logical or to get reduced grid of obsticles
    obsticle_grid = np.any(grid[:, 1:-1, [LAYERS.own_players, LAYERS.rival_players]], axis=-1)

    # Make sure we are still on the board
    assert -1 < pos[0] < obsticle_grid.shape[0] and -1 < pos[1] < obsticle_grid.shape[1]

    # Assume move is valid before running checks
    valid_move = True

    # MOVING UP
    if action == ACTIONS.up:
        if pos[0] == 0:
            # Can't move off the board
            valid_move = False
        elif obsticle_grid[pos[0]-1, pos[1]] is True:
            # Can't move if an object is there
            valid_move = False

    # MOVING DOWN
    elif action == ACTIONS.down:
        if pos[0] == obsticle_grid.shape[0]-1:
            # Can't move off the board
            valid_move = False
        elif obsticle_grid[pos[0]+1, pos[1]] is True:
            # Can't move if an object is there
            valid_move = False

    # MOVING LEFT
    elif action == ACTIONS.left:
        if pos[1] == 0:
            # Can't move off the board
            valid_move = False
        elif obsticle_grid[pos[0], pos[1]-1] is True:
            # Can't move if an object is there
            valid_move = False

    # MOVING RIGHT
    elif action == ACTIONS.right:
        if pos[1] == obsticle_grid.shape[1]-1:
            # Can't move off the board
            valid_move = False
        elif obsticle_grid[pos[0], pos[1]+1] is True:
            # Can't move if an object is there
            valid_move = False

    return valid_move


# %% Convert channels to colors
def grid_to_img(grid):
    img = np.zeros(grid.shape[:2] + (3,))
    for lyr in LAYERS:
        img = np.maximum(img, np.array(colors.to_rgb(LAYER_COLORS[lyr])) * grid[:, :, lyr:lyr+1])
    return img
