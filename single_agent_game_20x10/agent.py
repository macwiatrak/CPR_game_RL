import numpy as np
from celltype import *
from foodobj import *

class AgentObj:
    def __init__(self, coordinates, type, name, direction=0, mark=0, hidden=0):
        self.x = coordinates[0]
        self.y = coordinates[1]
        # 0: r, 1: g, 3: b
        self.type = type
        self.name = name
        self.hidden = hidden

        # 0: right, 1:top 2: left. 3: bottom
        self.direction = direction
        self.mark = mark
        self.observation = None

    def is_hidden(self):
        return self.hidden > 0

    def add_mark(self, agent_hidden):
        self.mark += 1
        if self.mark >= 2:
            self.mark = 0
            self.hidden = agent_hidden
        return self.mark

    def sub_hidden(self):
        self.hidden -= 1
        self.hidden = 0 if self.hidden <= 0 else self.hidden
        return self.hidden

    def turn_left(self, **kwargs):
        self.direction = (self.direction + 1) % 4
        return self.direction

    def turn_right(self, **kwargs):
        self.direction = (self.direction - 1 + 4) % 4
        return self.direction

    def move_forward_delta(self):
        if self.direction == 0:
            delta_x, delta_y = 1, 0
        elif self.direction == 1:
            delta_x, delta_y = 0, -1
        elif self.direction == 2:
            delta_x, delta_y = -1, 0
        elif self.direction == 3:
            delta_x, delta_y = 0, 1
        else:
            assert self.direction in range(4), 'wrong direction'

        return delta_x, delta_y

    def move_left_delta(self):
        if self.direction == 0:
            delta_x, delta_y = 0, -1
        elif self.direction == 1:
            delta_x, delta_y = -1, 0
        elif self.direction == 2:
            delta_x, delta_y = 0, 1
        elif self.direction == 3:
            delta_x, delta_y = 1, 0
        else:
            assert self.direction in range(4), 'wrong direction'

        return delta_x, delta_y

    def move_forward(self, env_x_size, env_y_size):
        delta_x, delta_y = self.move_forward_delta()

        self.x = self.x + delta_x if self.x + delta_x >= 0 and self.x + delta_x <= env_x_size - 1 else self.x
        self.y = self.y + delta_y if self.y + delta_y >= 0 and self.y + delta_y <= env_y_size - 1 else self.y
        return self.x, self.y

    def move_backward(self, env_x_size, env_y_size):
        forward_delta_x, forward_delta_y = self.move_forward_delta()
        delta_x, delta_y = -forward_delta_x, -forward_delta_y

        self.x = self.x + delta_x if self.x + delta_x >= 0 and self.x + delta_x <= env_x_size - 1 else self.x
        self.y = self.y + delta_y if self.y + delta_y >= 0 and self.y + delta_y <= env_y_size - 1 else self.y
        return self.x, self.y

    def move_left(self, env_x_size, env_y_size):
        delta_x, delta_y = self.move_left_delta()

        self.x = self.x + delta_x if self.x + delta_x >= 0 and self.x + delta_x <= env_x_size - 1 else self.x
        self.y = self.y + delta_y if self.y + delta_y >= 0 and self.y + delta_y <= env_y_size - 1 else self.y
        return self.x, self.y

    def move_right(self, env_x_size, env_y_size):
        left_delta_x, left_delta_y = self.move_left_delta()
        delta_x, delta_y = -left_delta_x, -left_delta_y

        self.x = self.x + delta_x if self.x + delta_x >= 0 and self.x + delta_x <= env_x_size - 1 else self.x
        self.y = self.y + delta_y if self.y + delta_y >= 0 and self.y + delta_y <= env_y_size - 1 else self.y
        return self.x, self.y

    def stay(self, **kwargs):
        pass

    def beam(self, env_x_size, env_y_size):
        if self.direction == 0:
            beam_set = [(i + 1, self.y) for i in range(self.x, env_x_size - 1)]
        elif self.direction == 1:
            beam_set = [(self.x, i - 1) for i in range(self.y, 0, -1)]
        elif self.direction == 2:
            beam_set = [(i - 1, self.y) for i in range(self.x, 0, -1)]
        elif self.direction == 3:
            beam_set = [(self.x, i + 1) for i in range(self.y, env_y_size - 1)]
        else:
            assert self.direction in range(4), 'wrong direction'
        return beam_set

    def get_front_player(self, env_x_size, env_y_size):
        if self.direction == 0:
            if self.x < env_x_size-1:
                front = (self.x + 1, self.y)
            else:
                front = (self.x, self.y)
        elif self.direction == 1:
            if self.y < env_y_size-1:
                front = (self.x, self.y + 1)
            else:
                front = (self.x, self.y)
        elif self.direction == 2:
            if self.x > 0:
                front = (self.x - 1, self.y)
            else:
                front = (self.x, self.y)
        elif self.direction == 3:
            if self.y > 0:
                front = (self.x, self.y - 1)
            else:
                front = (self.x, self.y)
        return front

    def partial_observation(self, env_x_size, env_y_size, grid):
        grid[self.x][self.y] = CellType.PLAYER
        obs = np.full([10, 11], "#", dtype=object)
        if self.direction == 0:
            if (env_x_size-10-self.x) > 0:
                if (self.y-5) < 0:
                    obs[:,5-self.y:11]=grid[self.x:self.x+10, 0:self.y+6]
                elif (self.y+5) > (env_y_size-1):
                    obs[:,:5+env_y_size-self.y]=grid[self.x:self.x+10, self.y-5:]
            else:
                if (self.y-5) < 0:
                    obs[:env_x_size - self.x, 5-self.y:11] = grid[self.x:,0:self.y+6]
                elif (self.y+5) > (env_y_size-1):
                    obs[:env_x_size - self.x, :5 + env_y_size - self.y] = grid[self.x:, self.y - 5:]
        elif self.direction == 1:
            if (self.x-5) < 0:
                obs[:self.y + 1, 5 - self.x:11] = np.flip(grid[:self.x+6,:self.y+1],1).T
            elif (self.x+5) > (env_x_size-1):
                obs[:self.y + 1, :5 + env_x_size - self.x] = np.flip(grid[self.x - 5:, :self.y + 1], 1).T
            else:
                obs[:self.y + 1, :] = np.flip(grid[self.x - 5:self.x + 6, :self.y + 1], 1).T
        elif self.direction == 2:
            if (self.x-10) < 0:
                if (self.y-5) < 0:
                    obs[:self.x + 1, :11 - 5 + self.y] = np.flip(grid[:self.x + 1, :self.y + 6])
                elif (self.y+10) > (env_y_size-1):
                    obs[:self.x + 1, 6 - env_y_size + self.y: 11] = np.flip(grid[:self.x + 1, self.y - 5:])
            else:
                if (self.y-5) < 0:
                    obs[:, :11 - 5 + self.y] = np.flip(grid[self.x - 9:self.x + 1, :self.y + 6])
                elif (self.y+10) > (env_y_size-1):
                    obs[:, 6 - env_y_size + self.y: 11] = np.flip(grid[self.x - 9:self.x + 1, self.y - 5:])
        elif self.direction == 3:
            if (self.x - 5) < 0:
                obs[:env_y_size - self.y, :self.x + 5 + 1] = np.flip(grid[:self.x + 6, self.y:], 0).T
            elif (self.x+5) > (env_x_size-1):
                obs[:env_y_size - self.y, 6 - env_x_size + self.x:11] = np.flip(grid[self.x - 5:, self.y:], 0).T
            else:
                obs[:env_y_size - self.y, :] = np.flip(grid[self.x - 5:self.x + 6, self.y:], 0).T
        else:
            assert self.direction in range(4), 'wrong direction'

        return obs


