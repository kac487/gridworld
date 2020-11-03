import numpy as np
from grid_soccer.utils import (
    ACTIONS,
    LAYERS,
    )


# %% Player Class
class Player:
    def __init__(self, team):
        '''
        Class for agents (members of a team)
        '''
        super().__init__()

        self.has_ball = False
        self.pos = None
        self.team = team
        self.steal_dist = 1  # pix away for valid steal
        self.pass_dist = 1   # pix away for valid pass

    def take_action(self, action, grid):
        '''
        Execute the specifed action updating the passed grid
        '''

        if action == ACTIONS.no_move:
            # No move made for this player (this code does nothing lol)
            pass

        elif action in [ACTIONS.up, ACTIONS.down, ACTIONS.left, ACTIONS.right]:
            # Player action is to move
            if self.check_valid_move(action, grid):
                # We are moving to a valid location

                # Rremove current position on the grid
                grid[self.pos[0], self.pos[1], LAYERS.own_players] = False

                # Rremove current ball position if we have the ball
                if self.has_ball:
                    grid[self.pos[0], self.pos[1], LAYERS.ball] = False

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

                # Update the ball position on the grid if we have the ball
                if self.has_ball:
                    grid[self.pos[0], self.pos[1], LAYERS.ball] = True

        elif action == ACTIONS.ball:

            # We have the ball
            if self.has_ball:
                # ATTEMPT TEAMMATE PASS ------
                did_pass = False
                for tmt in [p for p in self.team.players if p is not self]:
                    if np.all(np.abs(np.subtract(tmt.pos, self.pos)) <= self.pass_dist):
                        # print('PASSING THE BALL') # DEBUG
                        self.has_ball = False
                        tmt.has_ball = True
                        did_pass = True
                        grid[self.pos[0], self.pos[1], LAYERS.ball] = False
                        grid[tmt.pos[0], tmt.pos[1], LAYERS.ball] = True
                        break

                # DROP THE BALL ---------
                if not did_pass:
                    # print('DROPPING THE BALL') # DEBUG
                    self.has_ball = False

            # We do not have the ball
            else:
                # PICKUP THE BALL -----
                # Check if we are on top of the ball
                if np.all(grid[self.pos[0], self.pos[1], [LAYERS.own_players, LAYERS.ball]]):
                    # print('PICKING UP THE BALL') # DEBUG
                    self.has_ball = True

                # STEAL THE BALL --------
                else:
                    steal_rvl_pos = self.close_rival_w_ball(grid)
                    if steal_rvl_pos:
                        for rvl in [p for p in self.team.rival_team.players if p is not self]:
                            if rvl.pos == steal_rvl_pos:
                                # We are going to steal the ball
                                # print('STEALING THE BALL') # DEBUG
                                self.has_ball = True
                                rvl.has_ball = False
                                grid[rvl.pos[0], rvl.pos[1], LAYERS.ball] = False
                                grid[self.pos[0], self.pos[1], LAYERS.ball] = True
                                break

        else:
            raise ValueError('Invalid action specified: %s' % action)

        # Return the grid
        return grid

    def reset(self, pos):
        '''
        Reset the player
        '''
        self.has_ball = False
        self.pos = pos
        # respawn at specified location

    def close_rival_w_ball(self, grid):
        '''
        Searches for a nearby rival with the ball (to steal from)
        '''

        rival_w_ball_lyr = np.all(grid[:, :, [LAYERS.ball, LAYERS.rival_players]], axis=-1)

        if np.any(rival_w_ball_lyr):

            # Position of the rival with the ball
            riv = (np.argmax(rival_w_ball_lyr, axis=-1),
                   np.argmax(rival_w_ball_lyr, axis=0))

            if np.all(np.abs(np.subtract(riv, self.pos)) <= self.steal_dist):
                # rival w ball position is close enough to steal from
                return riv

        return None

    def check_valid_move(self, action, grid):
        '''
        Check of the movement is valid
        '''
        assert action.real < 5  # only should be called on movement actions

        # Ignore goal layers and perform logical or to get reduced grid of obsticles
        obsticle_grid = np.any(grid[:, :, [LAYERS.own_players, LAYERS.rival_players]], axis=-1)
        # print(obsticle_grid)

        # Make sure we are still on the board
        assert -1 < self.pos[0] < obsticle_grid.shape[0] and -1 < self.pos[1] < obsticle_grid.shape[1]

        # Assume move is valid before running checks
        valid_move = True

        # MOVING UP
        if action == ACTIONS.up:
            if self.pos[0] == 0:
                # Can't move off the board
                valid_move = False
            elif obsticle_grid[self.pos[0]-1, self.pos[1]]:
                # Can't move if an object is there
                valid_move = False

        # MOVING DOWN
        elif action == ACTIONS.down:
            if self.pos[0] == obsticle_grid.shape[0]-1:
                # Can't move off the board
                valid_move = False
            elif obsticle_grid[self.pos[0]+1, self.pos[1]]:
                # Can't move if an object is there
                valid_move = False

        # MOVING LEFT
        elif action == ACTIONS.left:
            if self.pos[1] == 0:
                # Can't move off the board
                valid_move = False
            elif obsticle_grid[self.pos[0], self.pos[1]-1]:
                # Can't move if an object is there
                valid_move = False

        # MOVING RIGHT
        elif action == ACTIONS.right:
            if self.pos[1] == obsticle_grid.shape[1]-1:
                # Can't move off the board
                valid_move = False
            elif obsticle_grid[self.pos[0], self.pos[1]+1]:
                # Can't move if an object is there
                valid_move = False

        # DEBUG
        if valid_move is False:
            print('Invalid Move')

        return valid_move

    def fake(self,):
        pass
        # TODO: Impiment this
