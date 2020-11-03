import numpy as np
import gym
from grid_soccer.team import Team
from grid_soccer.utils import (
    FIELD_ZONE,
    ACTIONS,
    LAYERS,
    place_random,
    grid_to_img,
    )


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

        # Set references to rival teams
        self.teams['blue'].rival_team = self.teams['red']
        self.teams['red'].rival_team = self.teams['blue']

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

        # NOTE: This is where each team updates the other wiht a projected set of layers

        for i in range(len(update_order)):
            # Output layers of what the teams is projecting is happening
            team_lyrs_proj = self.teams[update_order[i]].step(action[update_order[i]])
            if i == 0:
                self.teams[update_order[i+1]].grid[:, :, -3:] = np.flip(team_lyrs_proj, axis=-1)
            elif i == 1:
                self.teams[update_order[i-1]].grid[:, :, -3:] = np.flip(team_lyrs_proj, axis=-1)

        # TODO derive the true ball position from both teams and track it there
        # TODO use ball position to set the done flag

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
