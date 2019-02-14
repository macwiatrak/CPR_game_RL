import numpy as np
import scipy.misc
import random
import math


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
            beam_set = [(i + 1, self.y) for i in range(self.x, 20)]
        elif self.direction == 1:
            beam_set = [(self.x, i - 1) for i in range(self.y, 20)]
        elif self.direction == 2:
            beam_set = [(i - 1, self.y) for i in range(self.x, 20)]
        elif self.direction == 3:
            beam_set = [(self.x, i + 1) for i in range(self.y, 20)]
        else:
            assert self.direction in range(4), 'wrong direction'
        return beam_set


class FoodObj:
    def __init__(self, coordinates, type=1, reward=1):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.type = type
        # self.hidden = hidden
        self.is_collected = False
        self.reward = reward

    # def is_hidden(self):
    #   return self.hidden > 0

    def eat(self):
        self.is_collected = True
        return self.reward

    def respawn(self):
        self.is_collected = False


class GameEnv:
    def __init__(self, width=40, height=20, agent_hidden=5):
        self.size_x = width
        self.size_y = height
        self.objects = []
        self.agent_hidden = agent_hidden
        # self.food_hidden = food_hidden

        # 0: forward, 1: backward, 2: left, 3: right
        # 4: turn lelf, 5:turn right, 6: beam, 7: stay
        self.action_num = 8

        self.reset()

    def reset(self):
        self.agent1 = AgentObj(coordinates=(0, 1), type=2, name='agent1')
        self.agent2 = AgentObj(coordinates=(38, 17), type=0, name='agent2', direction=2)
        self.agent1_actions = [self.agent1.move_forward, self.agent1.move_backward, self.agent1.move_left,
                               self.agent1.move_right,
                               self.agent1.turn_left, self.agent1.turn_right, self.agent1.beam, self.agent1.stay]
        self.agent2_actions = [self.agent2.move_forward, self.agent2.move_backward, self.agent2.move_left,
                               self.agent2.move_right,
                               self.agent2.turn_left, self.agent2.turn_right, self.agent2.beam, self.agent2.stay]
        self.agent1_beam_set = []
        self.agent2_beam_set = []

        self.food_objects = []

        foodList = [(0, 4), (0, 15), (1, 3), (1, 4), (1, 5), (1, 11), (1, 18), (2, 4), (2, 6), (2, 8), (2, 10), (2, 11),
                    (2, 12),
                    (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 11), (3, 13), (3, 15), (4, 3), (4, 6), (4, 8), (4, 12),
                    (4, 13),
                    (4, 14), (4, 15), (4, 16), (5, 2), (5, 3), (5, 4), (5, 10), (5, 13), (5, 15), (5, 17), (6, 3),
                    (6, 5), (6, 9), (6, 10),
                    (6, 11), (6, 16), (6, 17), (6, 18), (7, 2), (7, 4), (7, 5), (7, 6), (7, 10), (7, 12), (7, 17),
                    (8, 1), (8, 2),
                    (8, 3), (8, 5), (8, 9), (8, 11), (8, 12), (8, 13), (8, 15), (9, 2), (9, 8), (9, 9), (9, 10),
                    (9, 12), (10, 16),
                    (10, 9), (11, 5), (11, 15), (11, 16), (11, 17), (12, 0), (12, 1), (12, 2), (12, 4), (12, 5),
                    (12, 6), (12, 18), (12, 16),
                    (12, 14), (13, 1), (13, 2), (13, 3), (13, 5), (13, 7), (13, 11), (13, 19), (13, 18), (13, 17),
                    (14, 2), (14, 6),
                    (14, 7), (14, 8), (14, 10), (14, 11), (14, 12), (14, 15), (14, 18), (15, 4), (15, 7), (15, 9),
                    (15, 11), (15, 13),
                    (15, 14), (15, 15), (15, 16), (16, 3), (16, 4), (16, 5), (16, 12), (16, 13), (16, 15), (16, 17),
                    (17, 4), (17, 6),
                    (17, 10), (17, 13), (17, 14), (17, 16), (17, 17), (17, 18), (18, 3), (18, 5), (18, 6), (18, 7),
                    (18, 9), (18, 10),
                    (18, 11), (18, 14), (18, 15), (18, 17), (19, 0), (19, 2), (19, 3), (19, 4), (19, 6), (19, 10),
                    (19, 12), (19, 14),
                    (20, 0), (20, 3), (20, 9), (20, 11), (20, 12), (20, 13), (21, 0), (21, 9), (21, 10), (21, 12),
                    (22, 0), (22, 4),
                    (22, 9), (23, 0), (23, 1), (23, 3), (23, 4), (23, 5), (23, 15), (24, 1), (24, 2), (24, 4), (24, 16),
                    (24, 15), (24, 14),
                    (24, 6), (25, 1), (25, 5), (25, 6), (25, 7), (25, 13), (25, 15), (25, 17), (26, 3), (26, 6),
                    (26, 18), (26, 17), (26, 16),
                    (27, 2), (27, 3), (27, 4), (27, 17), (27, 14), (28, 3), (28, 5), (28, 10), (28, 13), (28, 14),
                    (28, 15), (29, 2),
                    (29, 4), (29, 5), (29, 6), (29, 9), (29, 10), (29, 11), (29, 14), (29, 16), (30, 2), (30, 3),
                    (30, 5), (30, 8), (30, 10),
                    (30, 12), (30, 13), (30, 15), (30, 16), (30, 17), (31, 2), (31, 11), (31, 12), (31, 13), (31, 14),
                    (31, 16),
                    (32, 9), (32, 12), (32, 13), (33, 2), (33, 9), (33, 10), (34, 1), (34, 2), (34, 3), (34, 5),
                    (34, 9), (34, 11),
                    (35, 0), (35, 2), (35, 5), (35, 6), (35, 8), (35, 10), (35, 11), (35, 12), (36, 2), (36, 3),
                    (36, 6), (36, 7), (36, 8),
                    (36, 9), (36, 11), (37, 1), (37, 4), (37, 5), (37, 6), (37, 8), (38, 5)]

        for x in foodList:
            self.food_objects.append(FoodObj(x))

    def move(self, agent1_action, agent2_action):
        assert agent1_action in range(8), 'agent1 take wrong action'
        assert agent2_action in range(8), 'agent2 take wrong action'

        agent1_old_x, agent1_old_y = self.agent1.x, self.agent1.y
        agent2_old_x, agent2_old_y = self.agent2.x, self.agent2.y

        self.agent1.sub_hidden()
        self.agent2.sub_hidden()

        self.agent1_beam_set = []
        self.agent2_beam_set = []
        if not self.agent1.is_hidden():
            agent1_action_return = self.agent1_actions[agent1_action](env_x_size=self.size_x, env_y_size=self.size_y)
            self.agent1_beam_set = [] if agent1_action != 6 else agent1_action_return
        if not self.agent2.is_hidden():
            agent2_action_return = self.agent2_actions[agent2_action](env_x_size=self.size_x, env_y_size=self.size_y)
            self.agent2_beam_set = [] if agent2_action != 6 else agent2_action_return

        if not self.agent1.is_hidden() and not self.agent2.is_hidden() and \
                ((self.agent1.x == self.agent2.x and self.agent1.y == self.agent2.y) or
                 (self.agent1.x == agent2_old_x and self.agent1.y == agent2_old_y and
                  self.agent2.x == agent1_old_x and self.agent2.y == agent1_old_y)):
            self.agent1.x, self.agent1.y = agent1_old_x, agent1_old_y
            self.agent2.x, self.agent2.y = agent2_old_x, agent2_old_y

        def distance(point1, point2):
            return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

        def respawn_prob(food_around_nr, food):
            random_nr = random.uniform(0, 100)
            if food_around_nr > 4 and random_nr <= 10:
                food.respawn()
            elif food_around_nr >= 3 and random_nr <= 5:
                food.respawn()
            elif food_around_nr >= 1 and random_nr <= 1:
                food.respawn()

        agent1_reward = 0
        agent2_reward = 0

        foodList_not_collected = [(0, 4), (0, 15), (1, 3), (1, 4), (1, 5), (1, 11), (1, 18), (2, 4), (2, 6), (2, 8),
                                  (2, 10), (2, 11), (2, 12),
                                  (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 11), (3, 13), (3, 15), (4, 3), (4, 6),
                                  (4, 8), (4, 12), (4, 13),
                                  (4, 14), (4, 15), (4, 16), (5, 2), (5, 3), (5, 4), (5, 10), (5, 13), (5, 15), (5, 17),
                                  (6, 3), (6, 5), (6, 9), (6, 10),
                                  (6, 11), (6, 16), (6, 17), (6, 18), (7, 2), (7, 4), (7, 5), (7, 6), (7, 10), (7, 12),
                                  (7, 17), (8, 1), (8, 2),
                                  (8, 3), (8, 5), (8, 9), (8, 11), (8, 12), (8, 13), (8, 15), (9, 2), (9, 8), (9, 9),
                                  (9, 10), (9, 12), (10, 16),
                                  (10, 9), (11, 5), (11, 15), (11, 16), (11, 17), (12, 0), (12, 1), (12, 2), (12, 4),
                                  (12, 5), (12, 6), (12, 18), (12, 16),
                                  (12, 14), (13, 1), (13, 2), (13, 3), (13, 5), (13, 7), (13, 11), (13, 19), (13, 18),
                                  (13, 17), (14, 2), (14, 6),
                                  (14, 7), (14, 8), (14, 10), (14, 11), (14, 12), (14, 15), (14, 18), (15, 4), (15, 7),
                                  (15, 9), (15, 11), (15, 13),
                                  (15, 14), (15, 15), (15, 16), (16, 3), (16, 4), (16, 5), (16, 12), (16, 13), (16, 15),
                                  (16, 17), (17, 4), (17, 6),
                                  (17, 10), (17, 13), (17, 14), (17, 16), (17, 17), (17, 18), (18, 3), (18, 5), (18, 6),
                                  (18, 7), (18, 9), (18, 10),
                                  (18, 11), (18, 14), (18, 15), (18, 17), (19, 0), (19, 2), (19, 3), (19, 4), (19, 6),
                                  (19, 10), (19, 12), (19, 14),
                                  (20, 0), (20, 3), (20, 9), (20, 11), (20, 12), (20, 13), (21, 0), (21, 9), (21, 10),
                                  (21, 12), (22, 0), (22, 4),
                                  (22, 9), (23, 0), (23, 1), (23, 3), (23, 4), (23, 5), (23, 15), (24, 1), (24, 2),
                                  (24, 4), (24, 16), (24, 15), (24, 14),
                                  (24, 6), (25, 1), (25, 5), (25, 6), (25, 7), (25, 13), (25, 15), (25, 17), (26, 3),
                                  (26, 6), (26, 18), (26, 17), (26, 16),
                                  (27, 2), (27, 3), (27, 4), (27, 17), (27, 14), (28, 3), (28, 5), (28, 10), (28, 13),
                                  (28, 14), (28, 15), (29, 2),
                                  (29, 4), (29, 5), (29, 6), (29, 9), (29, 10), (29, 11), (29, 14), (29, 16), (30, 2),
                                  (30, 3), (30, 5), (30, 8), (30, 10),
                                  (30, 12), (30, 13), (30, 15), (30, 16), (30, 17), (31, 2), (31, 11), (31, 12),
                                  (31, 13), (31, 14), (31, 16),
                                  (32, 9), (32, 12), (32, 13), (33, 2), (33, 9), (33, 10), (34, 1), (34, 2), (34, 3),
                                  (34, 5), (34, 9), (34, 11),
                                  (35, 0), (35, 2), (35, 5), (35, 6), (35, 8), (35, 10), (35, 11), (35, 12), (36, 2),
                                  (36, 3), (36, 6), (36, 7), (36, 8),
                                  (36, 9), (36, 11), (37, 1), (37, 4), (37, 5), (37, 6), (37, 8), (38, 5)]

        for food in self.food_objects:
            if food.is_collected:
                foodList_not_collected.remove((food.x, food.y))

        for food in self.food_objects:
            if food.is_collected:

                nr_of_food_around = 0
                pt = (food.x, food.y)

                food_around = []
                for i in foodList_not_collected:
                    if distance(pt, i) <= 2:
                        food_around.append(i)
                        nr_of_food_around += 1

                respawn_prob(nr_of_food_around, food)

            if not food.is_collected:
                if not self.agent1.is_hidden() and food.x == self.agent1.x and food.y == self.agent1.y:
                    agent1_reward = food.eat()
                elif not self.agent2.is_hidden() and food.x == self.agent2.x and food.y == self.agent2.y:
                    agent2_reward = food.eat()

        if (self.agent1.x, self.agent1.y) in self.agent2_beam_set:
            self.agent1.add_mark(self.agent_hidden)
        if (self.agent2.x, self.agent2.y) in self.agent1_beam_set:
            self.agent2.add_mark(self.agent_hidden)

        return agent1_reward, agent2_reward

    def contribute_metrix(self):
        a = np.ones([self.size_y + 2, self.size_x + 2, 3])
        a[1:-1, 1:-1, :] = 0

        for x, y in self.agent1_beam_set:
            a[y + 1, x + 1, 0] = 0.5
            a[y + 1, x + 1, 1] = 0.5
            a[y + 1, x + 1, 2] = 0.5
        for x, y in self.agent2_beam_set:
            a[y + 1, x + 1, 0] = 0.5
            a[y + 1, x + 1, 1] = 0.5
            a[y + 1, x + 1, 2] = 0.5

        for food in self.food_objects:
            if not food.is_collected:
                for i in range(3):
                    a[food.y + 1, food.x + 1, i] = 1 if i == food.type else 0

        for i in range(3):
            if not self.agent1.is_hidden():
                delta_x, delta_y = self.agent1.move_forward_delta()
                a[self.agent1.y + 1 + delta_y, self.agent1.x + 1 + delta_x, i] = 0.5
            if not self.agent2.is_hidden():
                delta_x, delta_y = self.agent2.move_forward_delta()
                a[self.agent2.y + 1 + delta_y, self.agent2.x + 1 + delta_x, i] = 0.5
            if not self.agent1.is_hidden():
                a[self.agent1.y + 1, self.agent1.x + 1, i] = 1 if i == self.agent1.type else 0
            if not self.agent2.is_hidden():
                a[self.agent2.y + 1, self.agent2.x + 1, i] = 1 if i == self.agent2.type else 0

        return a

    def render_env(self):
        a = self.contribute_metrix()

        b = scipy.misc.imresize(a[:, :, 0], [5 * self.size_y, 5 * self.size_x, 1], interp='nearest')
        c = scipy.misc.imresize(a[:, :, 1], [5 * self.size_y, 5 * self.size_x, 1], interp='nearest')
        d = scipy.misc.imresize(a[:, :, 2], [5 * self.size_y, 5 * self.size_x, 1], interp='nearest')

        a = np.stack([b, c, d], axis=2)
        return a

    def train_render(self):
        a = self.contribute_metrix()

        b = scipy.misc.imresize(a[:, :, 0], [84, 84, 1], interp='nearest')
        c = scipy.misc.imresize(a[:, :, 1], [84, 84, 1], interp='nearest')
        d = scipy.misc.imresize(a[:, :, 2], [84, 84, 1], interp='nearest')

        a = np.stack([b, c, d], axis=2)
        return a