import numpy as np
from enum import IntEnum
from field_objects import place_random, Player, Ball, Goal


class Team:
    def __init__(self, field_size, n_players=3):
        '''
        Class for team of agents
        '''
        self.n_players = n_players
        # Create a set of n_players
        self.field_size = field_size
        pass

    def step(self, action):
        # Split action vector per player

        pass

    def reset(self, side):

        self.side = side
        spawn_points = place_random()
        for p in players:

            # Re-spawn players
        pass


class GridWorld:

    def __init__(self, ):

        self.init_grid()
        self.height = 16  # Grid height
        self.width = 24   # Grid width
        self.n_team_players = 3  # number of players per team
        # Set done flag to false
        self.done = False

        # Actions Enum
        class Actions(IntEnum):
            up = 0
            down = 1
            left = 2
            right = 3
            ball = 4
        self.actions = Actions

        # # Sides Enum
        # class Sides(IntEnum):
        #     # Only two sides for now
        #     blue = 0
        #     red = 1
        # self.sides = Sides

        # Field Zone Enum
        class FieldZone(IntEnum):
            left = 0
            middle = 1
            right = 2
        self.field_zone = FieldZone
        field_zone.right.real
        # initialize grid
        self.grid = self.generate_grid(grid_size=(self.height, self.width))

        # Generate Teams of players randomly switching sides
        swap_sides = np.random.choice(a=[False, True])
        self.teams = {
            'blue': Team(n_players=self.n_team_players),
            'red': Team(n_players=self.n_team_players),
        }

    def reset(self, random_agent=False, random_goal=False):
        '''
            observation: agent: 1
                         goal: 2
                         wall: -1
                         else: 0
        '''
        # Randomly switch team sides
        swap_sides = np.random.choice(a=[False, True])

        self.teams['blue'].reset(side=self.field_zone.left if swap_sides else self.field_zone.right)
        self.teams['red'].reset(side=self.field_zone.right if swap_sides else self.field_zone.left)

        self.grid[self.grid == 1] = 0
        self.grid[self.grid == 2] = 0

        if random_agent is True:
            # random agent position
            random_pos = np.random.randint(self.height * self.width - 1)
            self.pos = [random_pos // self.height, random_pos % self.width]
        else:
            self.pos = [0, 0]

        if random_goal is True:
            # random goal position
            random_goal = np.random.randint(self.height * self.width - 1)
            self.goal = (random_goal // self.height, random_goal % self.width)
        else:
            self.goal = (self.height - 1, self.width - 1)

        self.grid[self.pos[0], self.pos[1]] = 1
        self.grid[self.goal] = 2
        self.done = False

        return self.grid

    def step(self, action):
        pass
        return (None, None, None, None)

    def set_agent_pos(self, row, col):
        assert row < self.height
        assert col < self.width

        original_pos = self.pos.copy()
        self.grid[original_pos[0], self.original_pos[1]] = 0
        self.pos = [row, col]
        self.grid[self.pos[0], self.pos[1]] = 1

        return self.grid.copy()

    def generate_grid(self, grid_size):
        global_grid = np.zeros(shape=grid_size)
        # import matplotlib.pyplot as plt
        # plt.imshow(global_grid)
        # plt.grid(1)

    def load_file(self, file):
        with open(file, 'r') as f:
            grid_map = f.readlines()
        grid_map_array = np.array(
            list(map(
                lambda x: list(map(
                    lambda y: int(y),
                    x.split(' ')
                )),
                grid_map
            ))
        )

        self.grid = grid_map_array
        self.height = grid_map_array.shape[0]
        self.width = grid_map_array.shape[0]
        agent_pos = np.argwhere(grid_map_array == 1)
        goal_pos = np.argwhere(grid_map_array == 2)
        assert agent_pos.shape[0] == 1 and goal_pos.shape[0] == 1
        self.pos = [agent_pos[0][0], agent_pos[0][1]]
        self.goal = (goal_pos[0][0], goal_pos[0][1])
        print(grid_map_array, self.height, self.width)

    def render(self):
        return self.grid.copy()


if __name__ == '__main__':
    env = GridWorld()
    state = env.reset(random_loc=False)
    state = env.step(1)
    env.step(1)
    env.step(1)
    env.step(1)
    env.step(2)
    env.step(2)
    env.step(1)
    state = env.step(2)
    state = env.reset(random_loc=False)

    print(state)
