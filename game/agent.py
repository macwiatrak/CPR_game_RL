

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
            if (env_x_size-20-self.x) > 0:
                if (self.y-2) < 0:
                    beam_set = [(i + 1, self.y + j) for i in range(self.x, self.x + 20) for j in
                                range(-self.y, 3)]
                elif (self.y+2) > (env_y_size-1):
                    beam_set = [(i + 1, self.y + j) for i in range(self.x, self.x + 20) for j in
                                range(-2, env_y_size - self.y)]
                else:
                    beam_set = [(i + 1, self.y+j) for i in range(self.x, self.x + 20) for j in range(-2, 3)]
            else:
                if (self.y-2) < 0:
                    beam_set = [(i + 1, self.y + j) for i in range(self.x, env_x_size-1) for j in
                                range(-self.y, 3)]
                elif (self.y+2) > (env_y_size-1):
                    beam_set = [(i + 1, self.y + j) for i in range(self.x, env_x_size - 1) for j in
                                range(-2, env_y_size - self.y)]
                else:
                    beam_set = [(i + 1, self.y + j) for i in range(self.x, env_x_size-1) for j in
                                range(-2, 3)]
        elif self.direction == 1:
            if (self.x-2) < 0:
                beam_set = [(self.x+j, i - 1) for i in range(self.y, 0, -1) for j in
                                range(-self.x, 3)]
            elif (self.x+2) > (env_x_size-1):
                beam_set = [(self.x + j, i - 1) for i in range(self.y, 0, -1) for j in
                                range(-2, env_x_size - self.x)]
            else:
                beam_set = [(self.x + j, i - 1) for i in range(self.y, 0, -1) for j in
                                range(-2, 3)]
        elif self.direction == 2:
            if (self.x-20) < 0:
                if (self.y-2) < 0:
                    beam_set = [(i - 1, self.y + j) for i in range(self.x, 0, -1) for j in
                                range(-self.y, 3)]
                elif (self.y+2) > (env_y_size-1):
                    beam_set = [(i - 1, self.y + j) for i in range(self.x, 0, -1) for j in
                                range(-2, env_y_size - self.y)]
                else:
                    beam_set = [(i - 1, self.y + j) for i in range(self.x, 0, -1) for j in
                                range(-2, 3)]
            else:
                if (self.y-2) < 0:
                    beam_set = [(i - 1, self.y + j) for i in range(self.x - 20, self.x+1) for j in
                                range(-self.y, 3)]
                elif (self.y+2) > (env_y_size-1):
                    beam_set = [(i - 1, self.y + j) for i in range(self.x - 20, self.x+1) for j in
                                range(-2, env_y_size - self.y)]
                else:
                    beam_set = [(i - 1, self.y + j) for i in range(self.x - 20, self.x+1) for j in
                                range(-2, 3)]
        elif self.direction == 3:
            if (self.x - 2) < 0:
                beam_set = [(self.x + j, i + 1) for i in range(self.y, env_y_size - 1) for j in
                                range(-self.x, 3)]
            elif (self.x+2) > (env_x_size-1):
                beam_set = [(self.x + j, i + 1) for i in range(self.y, env_y_size - 1) for j in
                                range(-2, env_x_size - self.x)]
            else:
                beam_set = [(self.x + j, i + 1) for i in range(self.y, env_y_size-1) for j in
                                range(-2, 3)]
        else:
            assert self.direction in range(4), 'wrong direction'
        return beam_set

    def get_observation(self, env_x_size, env_y_size):
        if self.direction == 0:
            if (env_x_size-20-self.x) > 0:
                if (self.y-10) < 0:
                    obs = [(i, self.y + j) for i in range(self.x, self.x + 20) for j in
                                range(-self.y, 11)]
                elif (self.y+10) > (env_y_size-1):
                    obs = [(i, self.y + j) for i in range(self.x, self.x + 20) for j in
                                range(-10, env_y_size - self.y)]
                else:
                    obs = [(i, self.y+j) for i in range(self.x, self.x + 20) for j in range(-10, 11)]
            else:
                if (self.y-10) < 0:
                    obs = [(i, self.y + j) for i in range(self.x, env_x_size-1) for j in
                                range(-self.y, 11)]
                elif (self.y+10) > (env_y_size-1):
                    obs = [(i, self.y + j) for i in range(self.x, env_x_size - 1) for j in
                                range(-10, env_y_size - self.y)]
                else:
                    obs = [(i, self.y + j) for i in range(self.x, env_x_size-1) for j in
                                range(-10, 11)]
        elif self.direction == 1:
            if (self.x-10) < 0:
                obs = [(self.x+j, i) for i in range(self.y, 0, -1) for j in
                                range(-self.x, 11)]
            elif (self.x+10) > (env_x_size-1):
                obs = [(self.x + j, i) for i in range(self.y, 0, -1) for j in
                                range(-10, env_x_size - self.x)]
            else:
                obs = [(self.x + j, i) for i in range(self.y, 0, -1) for j in
                                range(-10, 11)]
        elif self.direction == 2:
            if (self.x-20) < 0:
                if (self.y-10) < 0:
                    obs = [(i, self.y + j) for i in range(self.x, 0, -1) for j in
                                range(-self.y, 11)]
                elif (self.y+10) > (env_y_size-1):
                    obs = [(i, self.y + j) for i in range(self.x, 0, -1) for j in
                                range(-10, env_y_size - self.y)]
                else:
                    obs = [(i, self.y + j) for i in range(self.x, 0, -1) for j in
                                range(-10, 11)]
            else:
                if (self.y-10) < 0:
                    obs = [(i, self.y + j) for i in range(self.x - 20, self.x+1) for j in
                                range(-self.y, 11)]
                elif (self.y+10) > (env_y_size-1):
                    obs = [(i, self.y + j) for i in range(self.x - 20, self.x+1) for j in
                                range(-10, env_y_size - self.y)]
                else:
                    obs = [(i, self.y + j) for i in range(self.x - 20, self.x+1) for j in
                                range(-10, 11)]
        elif self.direction == 3:
            if (self.x - 10) < 0:
                obs = [(self.x + j, i) for i in range(self.y, env_y_size - 1) for j in
                                range(-self.x, 11)]
            elif (self.x+10) > (env_x_size-1):
                obs = [(self.x + j, i) for i in range(self.y, env_y_size - 1) for j in
                                range(-10, env_x_size - self.x)]
            else:
                obs = [(self.x + j, i) for i in range(self.y, env_y_size-1) for j in
                                range(-10, 11)]
        else:
            assert self.direction in range(4), 'wrong direction'
        return obs