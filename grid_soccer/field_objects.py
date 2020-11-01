import numpy as np
from enum import IntEnum


# %% Helper Methods
def place_random(region, field_size, num_draws=1):
    # Assign a random set of indices in specified field region
    rand_y = np.random.randint(low=0, high=field_size[0], size=num_draws)

    half = (field_size[1])//2
    middle_split = (field_size[1]-2)//4

    if region.real == 0:  # field zone left
        # Selects random place on left side of the field
        rand_x = np.random.randint(low=1, high=half - middle_split, size=num_draws)
    elif region.real == 1:  # field zone middle
        # Selects random place in the middle of the field
        rand_x = np.random.randint(low=half - middle_split, high=half + middle_split, size=num_draws)
        # Selects random place on right side of the field
    elif region.real == 2:  # field zone right
        rand_x = np.random.randint(low=half + middle_split, high=field_size[1]-1, size=num_draws)
    else:
        raise ValueError('Invalid field region specified')

    return np.array([rand_y, rand_x])


# %% Field Object Base class
class FieldObject:
    def __init__(self, ):
        '''
        Base Class for Field Objects
        '''
        self.pos = None  # X, Y position


# %% Player Class
class Player(FieldObject):
    def __init__(self, init_pos, side, ):
        '''
        Class for agents (members of a team)
        '''
        super().__init__()
        self.side = side
        pass

    def step(self, action):
        # move player to new positition
        # action(up:0, down:1, left:2, right:3)
        original_pos = self.pos.copy()
        out_of_boundary = False
        if action == self.actions.up:
            if self.pos[0] - 1 >= 0:
                self.pos[0] = self.pos[0] - 1
            else:
                out_of_boundary = True
        elif action == self.actions.down:
            if self.pos[0] + 1 < self.height:
                self.pos[0] = self.pos[0] + 1
            else:
                out_of_boundary = True
        elif action == self.actions.left:
            if self.pos[1] - 1 >= 0:
                self.pos[1] = self.pos[1] - 1
            else:
                out_of_boundary = True
        elif action == self.actions.right:
            if self.pos[1] + 1 < self.width:
                self.pos[1] = self.pos[1] + 1
            else:
                out_of_boundary = True

        if (self.pos[0], self.pos[1]) == self.goal:
            reward = 1
            self.done = True
        elif self.grid[self.pos[0], self.pos[1]] == -1:
            reward = 0
            self.pos = original_pos
        elif out_of_boundary:
            reward = 0
            self.pos = original_pos
        else:
            reward = 0
            self.grid[self.pos[0], self.pos[1]] = 1
            self.grid[original_pos[0], original_pos[1]] = 0

        # handle ball plays (pick, drop, pass, steal)

    def fake(self, ):
        pass
        # TODO: Impiment this


# %% Ball Class
class Ball(FieldObject):
    def __init__(self,):
        super().__init__()


# %% Goal Class
class Goal(FieldObject):
    def __init__(self, ):
        pass
