import numpy as np
from grid_soccer.player import Player
from grid_soccer.utils import (
    FIELD_ZONE,
    # ACTIONS,
    LAYERS,
    place_random,
    # check_valid_move,
    # grid_to_img,
    )


# %% Team Class
class Team:
    def __init__(self, field_size, n_players):
        '''
        Class for team of agents
        '''
        self.n_players = n_players
        # Create a set of n_players
        self.field_size = field_size

        # Set default value for the grid
        self.grid = None

        # Set default value for side
        self.side = None

        # Create a list of players
        self.players = [Player(team=self) for _ in range(self.n_players)]

        # Create reference to rival team
        self.rival_team = None

    def step(self, action):
        # Split action vector per player
        for i, plyr in enumerate(self.players):
            # Each of the players takes action
            self.grid = plyr.take_action(action[i], self.grid)

        # TODO add split from internal state here for fakes
        grid_lyr_proj = self.grid[:, :, :3]

        return grid_lyr_proj

    def reset(self, side):

        self.side = side

        # Team Grid of shape (Y, X, [goal, own_players])
        team_grid = np.zeros(shape=(self.field_size[0], self.field_size[1], 2), dtype=np.bool)

        # Re-spawn players
        player_spawns = place_random(region=side, field_size=self.field_size, num_draws=self.n_players)
        for i, plyr in enumerate(self.players):
            team_grid[player_spawns[i, 0], player_spawns[i, 1], LAYERS.own_players] = True
            plyr.reset(pos=player_spawns[i])

        # Set the goal grid position(s)
        if side is FIELD_ZONE.left:
            x_ix = 0
        elif side is FIELD_ZONE.right:
            x_ix = self.field_size[1]-1
        else:
            raise ValueError('Invalid side specified %s' % side)

        team_grid[self.field_size[0]//2-1:self.field_size[0]//2+2, x_ix, LAYERS.own_goal] = True

        return team_grid
