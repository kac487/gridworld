import numpy as np
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

    def step(self, action, grid):
        # Split action vector per player
        for i, plyr in enumerate(self.players):
            # Each of the players takes action
            self.grid = plyr.take_action(action[i], self.grid)

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

    def take_action(self, action, grid):
        # move player to new positition
        # action(up:0, down:1, left:2, right:3)

        if action in [ACTIONS.up, ACTIONS.down, ACTIONS.left, ACTIONS.right]:
            # Player action is to move
            if check_valid_move(self.pos, action, grid):
                # We are moving to a valid location

                # Rremove current position on the grid
                grid[self.pos + (LAYERS.own_players)] = False

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
                grid[self.pos + (LAYERS.own_players)] = True

                return grid

            else:
                # We are trying to move somewhere invalid
                return grid
        elif action == ACTIONS.ball:
            # Player action is on the ball
            # TODO the following:
            # Pick up the ball if we are next to it
            # Drop the ball if there are no players to pass to
            # Pass the ball if there is a teammate close
            # Steal the ball if we are near a rival player with it

            return grid

        else:
            raise ValueError('Invalid action specified: %s' % action)

        # handle ball plays (pick, drop, pass, steal)

    def reset(self, pos):
        self.has_ball = False
        self.pos = pos
        # respawn at specified location

    def fake(self,):
        pass
        # TODO: Impiment this


# %% SoccerGridWorld Class
class SoccerGridWorld:

    def __init__(self, ):

        self.height = 16                # Grid height
        self.width = 24                 # Grid width
        self.n_layers = len(LAYERS)     # Grid channels
        self.n_team_players = 3         # number of players per team

        # Set done flag to false
        self.done = False

        # Generate Teams of Players
        self.teams = {
            'blue': Team(field_size=(self.height, self.width), n_players=self.n_team_players),
            'red': Team(field_size=(self.height, self.width), n_players=self.n_team_players),
        }

    def reset(self, ):

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
        ball_spawn = place_random(region=FIELD_ZONE.middle, field_size=(self.height, self.width))
        grid_ball_lyr[ball_spawn[0, 0], ball_spawn[0, 1], 0] = True

        # Create Local grid versions for each of the teams
        self.teams['blue'].grid = np.concatenate((grid_blue_lyrs, grid_ball_lyr, np.flip(grid_red_lyrs, axis=-1)), axis=-1)
        self.teams['red'].grid = np.concatenate((grid_red_lyrs, grid_ball_lyr, np.flip(grid_blue_lyrs, axis=-1)), axis=-1)

        # Set the done flag
        self.done = False

        return

    def step(self, action):
        pass

        # TODO
        # We update the defending team side first when the ball is on the side of the field
        # nearest the defending team's goal

        # Check which side of the field the ball is on

        # Get the team currently playing that side of the field and update that team first

        # Update the offensive team next

        return (None, None, None, None)

    def render(self):
        return {'blue': grid_to_img(self.teams['blue'].grid),
                'red': grid_to_img(self.teams['red'].grid), }


if __name__ == '__main__':
    self = SoccerGridWorld()
    state = self.reset()
    self.render()
    # state = env.step(1)
    # env.step(1)
    # env.step(1)
    # env.step(1)
    # env.step(2)
    # env.step(2)
    # env.step(1)
    # state = env.step(2)
    # state = env.reset(random_loc=False)

    print(state)
