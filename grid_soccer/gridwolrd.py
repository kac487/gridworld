import numpy as np
import gym
from grid_soccer.utils import (
    FIELD_ZONE,
    ACTIONS,
    LAYERS,
    place_random,
    check_valid_move,
    grid_to_img,
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
        self.players = [Player() for _ in range(self.n_players)]

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


# %% Player Class
class Player:
    def __init__(self, ):
        '''
        Class for agents (members of a team)
        '''
        super().__init__()

        self.has_ball = False
        self.pos = None

    def take_action(self, action, grid):
        # move player to new positition
        # action(up:0, down:1, left:2, right:3)

        if action == ACTIONS.no_move:
            # No move made for this player
            return grid

        if action in [ACTIONS.up, ACTIONS.down, ACTIONS.left, ACTIONS.right]:
            # Player action is to move
            if check_valid_move(self.pos, action, grid):
                # We are moving to a valid location

                # Rremove current position on the grid
                grid[self.pos[0], self.pos[1], LAYERS.own_players] = False

                # Update the player's position
                if action == ACTIONS.up:
                    self.pos[0] -= 1
                elif action == ACTIONS.down:
                    self.pos[0] += 1
                elif action == ACTIONS.left:
                    self.pos[1] -= 1
                elif action == ACTIONS.right:
                    self.pos[1] += 1

                # Update the new position on the grid
                grid[self.pos[0], self.pos[1], LAYERS.own_players] = True

        elif action == ACTIONS.ball:
            # Player action is on the ball
            # TODO the following:
            # Pick up the ball if we are next to it
            # Drop the ball if there are no players to pass to
            # Pass the ball if there is a teammate close
            # Steal the ball if we are near a rival player with it
            pass

        else:
            raise ValueError('Invalid action specified: %s' % action)

        # handle ball plays (pick, drop, pass, steal)
        print('current_pos ', self.pos)

        # Return the grid
        return grid

    def reset(self, pos):
        self.has_ball = False
        self.pos = pos
        # respawn at specified location

    def fake(self,):
        pass
        # TODO: Impiment this


# %% SoccerGridWorld Class
class SoccerGridWorld(gym.Env):

    def __init__(self, ):

        self.height = 16                # Grid height
        self.width = 24                 # Grid width
        self.n_layers = len(LAYERS)     # Grid channels
        self.n_team_players = 3         # number of players per team
        self.ball_pos = None            # Field for the true ball position

        self.actions = ACTIONS

        # Set done flag to false
        self.done = False

        # Generate Teams of Players
        self.teams = {
            'blue': Team(field_size=(self.height, self.width), n_players=self.n_team_players),
            'red': Team(field_size=(self.height, self.width), n_players=self.n_team_players),
        }

    def get_act_space(self,):
        return {'blue': gym.spaces.Box(low=0, high=len(ACTIONS), shape=self.n_team_players),
                'red': gym.spaces.Box(low=0, high=len(ACTIONS), shape=self.n_team_players), }

    def get_obs_space(self,):
        return {'blue': gym.spaces.Box(low=0, high=1, shape=(self.height, self.width, len(LAYERS))),
                'red': gym.spaces.Box(low=0, high=1, shape=(self.height, self.width, len(LAYERS))), }

    def reset(self,):

        # grid = self.generate_grid(grid_size=(self.height, self.width, self.n_layers))

        # Randomly switch team sides
        swap_sides = np.random.choice(a=[False, True])

        # Reset each of the teams
        grid_blue_lyrs = self.teams['blue'].reset(
            side=FIELD_ZONE.left if swap_sides else FIELD_ZONE.right)

        grid_red_lyrs = self.teams['red'].reset(
            side=FIELD_ZONE.right if swap_sides else FIELD_ZONE.left)

        # Randomly position the Ball in the middle zone of the field
        grid_ball_lyr = np.zeros(shape=(self.height, self.width, 1))
        self.ball_pos = place_random(region=FIELD_ZONE.middle, field_size=(self.height, self.width))[0]

        grid_ball_lyr[self.ball_pos[0], self.ball_pos[1], 0] = True

        # Create Local grid versions for each of the teams
        self.teams['blue'].grid = np.concatenate((grid_blue_lyrs, grid_ball_lyr, np.flip(grid_red_lyrs, axis=-1)), axis=-1)
        self.teams['red'].grid = np.concatenate((grid_red_lyrs, grid_ball_lyr, np.flip(grid_blue_lyrs, axis=-1)), axis=-1)

        # Set the done flag
        self.done = False

        return {'blue': self.teams['blue'].grid, 'red': self.teams['red'].grid}

    def step(self, action):

        # We update the defending team side first when the ball is on the side of the field
        # nearest the defending team's goal

        update_order = ['blue', 'red']

        # Check which side of the field the ball is on
        if self.ball_pos[1] < self.width//2:
            # Ball is on the left side of the field
            if self.teams['red'].side is FIELD_ZONE.left:
                update_order.reverse()
        else:
            # Ball is on the right side of the field
            if self.teams['red'].side is FIELD_ZONE.right:
                update_order.reverse()

        for i in range(len(update_order)):
            # Output layers of what the teams is projecting is happening
            team_lyrs_proj = self.teams[update_order[i]].step(action[update_order[i]])
            if i == 0:
                self.teams[update_order[i+1]].grid[:, :, -3:] = np.flip(team_lyrs_proj, axis=-1)
            elif i == 1:
                self.teams[update_order[i-1]].grid[:, :, -3:] = np.flip(team_lyrs_proj, axis=-1)

        # TODO add logic for moving the ball, passig, and stealing

        obs = {'blue': self.teams['blue'].grid, 'red': self.teams['red'].grid}
        reward = {'blue': 0, 'red': 0}
        done = {'blue': False, 'red': False}
        info = {'blue': {}, 'red': {}}

        return (obs, reward, done, info)

    def render(self):
        return {'blue': grid_to_img(self.teams['blue'].grid),
                'red': grid_to_img(self.teams['red'].grid), }


if __name__ == '__main__':
    self = SoccerGridWorld()
    state = self.reset()
    self.render()
    state = self.step({'blue': [1, 1, 1], 'red': [0, 0, 0]})
    # env.step(1)
    # env.step(1)
    # env.step(1)
    # env.step(2)
    # env.step(2)
    # env.step(1)
    # state = env.step(2)
    # state = env.reset(random_loc=False)

    print(state)
