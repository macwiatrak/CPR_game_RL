import numpy as np
import scipy.misc
import random
import math

from agent import *
from foodobj import *
from constant import *
from celltype import *

class GameEnv:
    def __init__(self, width=40, height=20, agent_hidden=25):
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
        self.agent1 = AgentObj(coordinates=(0, 1), type=0, name='agent1')
        self.agent2 = AgentObj(coordinates=(38, 17), type=0, name='agent2', direction=1)
        self.agent3 = AgentObj(coordinates=(35, 15), type=0, name='agent2', direction=2)
        self.agent1_actions = [self.agent1.move_forward, self.agent1.move_backward, self.agent1.move_left,
                               self.agent1.move_right,
                               self.agent1.turn_left, self.agent1.turn_right, self.agent1.beam, self.agent1.stay]
        self.agent2_actions = [self.agent2.move_forward, self.agent2.move_backward, self.agent2.move_left,
                               self.agent2.move_right,
                               self.agent2.turn_left, self.agent2.turn_right, self.agent2.beam, self.agent2.stay]
        self.agent3_actions = [self.agent3.move_forward, self.agent3.move_backward, self.agent3.move_left,
                               self.agent3.move_right,
                               self.agent3.turn_left, self.agent3.turn_right, self.agent3.beam, self.agent3.stay]
        self.agent1_beam_set = []
        self.agent2_beam_set = []
        self.agent3_beam_set = []

        agent1_obs = self.agent1.partial_observation(env_x_size=40, env_y_size=20)
        agent2_obs = self.agent2.partial_observation(env_x_size=40, env_y_size=20)
        agent3_obs = self.agent3.partial_observation(env_x_size=40, env_y_size=20)


        self.food_objects = []

        #for x in foodList:
         #   self.food_objects.append(FoodObj(x))

        for x in test1:
            self.food_objects.append(FoodObj(x))

        def convert_observation_to_rgb(obs):
            observation_rgb = np.zeros([obs.shape[0], obs.shape[1], 3], 'int')
            for x in np.arange(obs.shape[0]):
                for y in np.arange(obs.shape[1]):
                    if obs[x, y] == CellType.EMPTY:
                        observation_rgb[x, y, :] = Colors.SCREEN_BACKGROUND
                    else:
                        observation_rgb[x, y, :] = Colors.CELL_TYPE[obs[x, y]]
            return np.uint8(observation_rgb)

        for m in range(agent1_obs.shape[0]):
            for n in range(agent1_obs.shape[1]):
                if agent1_obs[m][n] == (self.agent1.x, self.agent1.y):
                    agent1_obs[m][n] = CellType.PLAYER
                elif agent1_obs[m][n] == (self.agent2.x, self.agent2.y):
                    agent1_obs[m][n] = CellType.OPPONENT
                elif agent1_obs[m][n] == (self.agent3.x, self.agent3.y):
                    agent1_obs[m][n] = CellType.OPPONENT
                elif agent1_obs[m][n] == self.agent1.get_front_player():
                    agent1_obs[m][n] = CellType.AGENT_FRONT
                elif agent1_obs[m][n] == self.agent2.get_front_player():
                    agent1_obs[m][n] = CellType.AGENT_FRONT
                elif agent1_obs[m][n] == self.agent3.get_front_player():
                    agent1_obs[m][n] = CellType.AGENT_FRONT
                elif agent1_obs[m][n] in foodList:
                    agent1_obs[m][n] = CellType.APPLE
                elif agent1_obs[m][n] in self.agent1_beam_set:
                    agent1_obs[m][n] = CellType.BEAM
                elif agent1_obs[m][n] in self.agent2_beam_set:
                    agent1_obs[m][n] = CellType.BEAM
                elif agent1_obs[m][n] in self.agent3_beam_set:
                    agent1_obs[m][n] = CellType.BEAM
                elif agent1_obs[m][n] == 0:
                    agent1_obs[m][n] = CellType.WALL
                else:
                    agent1_obs[m][n] = CellType.EMPTY

        for m in range(agent2_obs.shape[0]):
            for n in range(agent2_obs.shape[1]):
                if agent2_obs[m][n] == (self.agent2.x, self.agent2.y):
                    agent2_obs[m][n] = CellType.PLAYER
                elif agent2_obs[m][n] == (self.agent1.x, self.agent1.y):
                    agent2_obs[m][n] = CellType.OPPONENT
                elif agent2_obs[m][n] == (self.agent3.x, self.agent3.y):
                    agent2_obs[m][n] = CellType.OPPONENT
                elif agent2_obs[m][n] == self.agent1.get_front_player():
                    agent2_obs[m][n] = CellType.AGENT_FRONT
                elif agent2_obs[m][n] == self.agent2.get_front_player():
                    agent2_obs[m][n] = CellType.AGENT_FRONT
                elif agent2_obs[m][n] == self.agent3.get_front_player():
                    agent2_obs[m][n] = CellType.AGENT_FRONT
                elif agent2_obs[m][n] in foodList:
                    agent2_obs[m][n] = CellType.APPLE
                elif agent2_obs[m][n] in self.agent1_beam_set:
                    agent2_obs[m][n] = CellType.BEAM
                elif agent2_obs[m][n] in self.agent2_beam_set:
                    agent2_obs[m][n] = CellType.BEAM
                elif agent2_obs[m][n] in self.agent3_beam_set:
                    agent2_obs[m][n] = CellType.BEAM
                elif agent2_obs[m][n] == 0:
                    agent2_obs[m][n] = CellType.WALL
                else:
                    agent2_obs[m][n] = CellType.EMPTY

        for m in range(agent3_obs.shape[0]):
            for n in range(agent3_obs.shape[1]):
                if agent3_obs[m][n] == (self.agent3.x, self.agent3.y):
                    agent3_obs[m][n] = CellType.PLAYER
                elif agent3_obs[m][n] == (self.agent1.x, self.agent1.y):
                    agent3_obs[m][n] = CellType.OPPONENT
                elif agent3_obs[m][n] == (self.agent2.x, self.agent2.y):
                    agent3_obs[m][n] = CellType.OPPONENT
                elif agent3_obs[m][n] == self.agent1.get_front_player():
                    agent3_obs[m][n] = CellType.AGENT_FRONT
                elif agent3_obs[m][n] == self.agent2.get_front_player():
                    agent3_obs[m][n] = CellType.AGENT_FRONT
                elif agent3_obs[m][n] == self.agent3.get_front_player():
                    agent3_obs[m][n] = CellType.AGENT_FRONT
                elif agent3_obs[m][n] in foodList:
                    agent3_obs[m][n] = CellType.APPLE
                elif agent3_obs[m][n] in self.agent1_beam_set:
                    agent3_obs[m][n] = CellType.BEAM
                elif agent3_obs[m][n] in self.agent2_beam_set:
                    agent3_obs[m][n] = CellType.BEAM
                elif agent3_obs[m][n] in self.agent3_beam_set:
                    agent3_obs[m][n] = CellType.BEAM
                elif agent3_obs[m][n] == 0:
                    agent3_obs[m][n] = CellType.WALL
                else:
                    agent3_obs[m][n] = CellType.EMPTY

        agent1_obs = convert_observation_to_rgb(agent1_obs)
        agent2_obs = convert_observation_to_rgb(agent2_obs)
        agent3_obs = convert_observation_to_rgb(agent3_obs)

        return [agent1_obs, agent2_obs, agent3_obs]

    def step(self, action_n):


        assert action_n[0] in range(8), 'agent1 take wrong action'
        assert action_n[1] in range(8), 'agent2 take wrong action'
        assert action_n[2] in range(8), 'agent1 take wrong action'

        agent1_old_x, agent1_old_y = self.agent1.x, self.agent1.y
        agent2_old_x, agent2_old_y = self.agent2.x, self.agent2.y
        agent3_old_x, agent3_old_y = self.agent3.x, self.agent3.y

        self.agent1.sub_hidden()
        self.agent2.sub_hidden()
        self.agent3.sub_hidden()

        self.agent1_beam_set = []
        self.agent2_beam_set = []
        self.agent3_beam_set = []

        if not self.agent1.is_hidden():
            agent1_action_return = self.agent1_actions[action_n[0]](env_x_size=self.size_x, env_y_size=self.size_y)
            self.agent1_beam_set = [] if action_n[0] != 6 else agent1_action_return
        if not self.agent2.is_hidden():
            agent2_action_return = self.agent2_actions[action_n[1]](env_x_size=self.size_x, env_y_size=self.size_y)
            self.agent2_beam_set = [] if action_n[1] != 6 else agent2_action_return
        if not self.agent3.is_hidden():
            agent3_action_return = self.agent3_actions[action_n[2]](env_x_size=self.size_x, env_y_size=self.size_y)
            self.agent3_beam_set = [] if action_n[2] != 6 else agent3_action_return

        if not self.agent1.is_hidden() and not self.agent2.is_hidden() and \
                ((self.agent1.x == self.agent2.x and self.agent1.y == self.agent2.y) or
                 (self.agent1.x == agent2_old_x and self.agent1.y == agent2_old_y and
                  self.agent2.x == agent1_old_x and self.agent2.y == agent1_old_y)):
            self.agent1.x, self.agent1.y = agent1_old_x, agent1_old_y
            self.agent2.x, self.agent2.y = agent2_old_x, agent2_old_y

        if not self.agent1.is_hidden() and not self.agent3.is_hidden() and \
                ((self.agent1.x == self.agent3.x and self.agent1.y == self.agent3.y) or
                 (self.agent1.x == agent3_old_x and self.agent1.y == agent3_old_y and
                  self.agent3.x == agent1_old_x and self.agent3.y == agent1_old_y)):
            self.agent1.x, self.agent1.y = agent1_old_x, agent1_old_y
            self.agent3.x, self.agent3.y = agent3_old_x, agent3_old_y

        if not self.agent2.is_hidden() and not self.agent3.is_hidden() and \
                ((self.agent2.x == self.agent3.x and self.agent2.y == self.agent3.y) or
                 (self.agent2.x == agent3_old_x and self.agent2.y == agent3_old_y and
                  self.agent3.x == agent2_old_x and self.agent3.y == agent2_old_y)):
            self.agent2.x, self.agent2.y = agent2_old_x, agent2_old_y
            self.agent3.x, self.agent3.y = agent3_old_x, agent3_old_y

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
        agent3_reward = 0

        #food_not_coll = foodList_1.copy()
        food_not_coll = test2.copy()


        for food in self.food_objects:
            if food.is_collected:
                food_not_coll.remove((food.x, food.y))

        if not food_not_coll:
            done = True
        else:
            done = False

        '''if not food_not_coll:
            done = 'gameover'
        else:
            done = 'play'''

        for food in self.food_objects:
            if food.is_collected:

                nr_of_food_around = 0
                pt = (food.x, food.y)

                food_around = []
                for i in food_not_coll:
                    if distance(pt, i) <= 2:
                        food_around.append(i)
                        nr_of_food_around += 1

                respawn_prob(nr_of_food_around, food)

            if not food.is_collected:
                if not self.agent1.is_hidden() and food.x == self.agent1.x and food.y == self.agent1.y:
                    agent1_reward = food.eat()
                elif not self.agent2.is_hidden() and food.x == self.agent2.x and food.y == self.agent2.y:
                    agent2_reward = food.eat()
                elif not self.agent3.is_hidden() and food.x == self.agent3.x and food.y == self.agent3.y:
                    agent3_reward = food.eat()

        if (self.agent1.x, self.agent1.y) in (self.agent2_beam_set or self.agent3_beam_set):
            self.agent1.add_mark(self.agent_hidden)
        if (self.agent2.x, self.agent2.y) in (self.agent1_beam_set or self.agent3_beam_set):
            self.agent2.add_mark(self.agent_hidden)
        if (self.agent3.x, self.agent3.y) in (self.agent1_beam_set or self.agent2_beam_set):
            self.agent3.add_mark(self.agent_hidden)

        agent1_obs = self.agent1.partial_observation(env_x_size=40, env_y_size=20)
        agent2_obs = self.agent2.partial_observation(env_x_size=40, env_y_size=20)
        agent3_obs = self.agent3.partial_observation(env_x_size=40, env_y_size=20)


        def convert_observation_to_rgb(obs):
            observation_rgb = np.zeros([obs.shape[0], obs.shape[1], 3], 'int')
            for x in np.arange(obs.shape[0]):
                for y in np.arange(obs.shape[1]):
                    if obs[x, y] == CellType.EMPTY:
                        observation_rgb[x, y, :] = Colors.SCREEN_BACKGROUND
                    else:
                        observation_rgb[x, y, :] = Colors.CELL_TYPE[obs[x, y]]
            return np.uint8(observation_rgb)

        for m in range(agent1_obs.shape[0]):
            for n in range(agent1_obs.shape[1]):
                if agent1_obs[m][n] == (self.agent1.x, self.agent1.y):
                    agent1_obs[m][n] = CellType.PLAYER
                elif agent1_obs[m][n] == (self.agent2.x, self.agent2.y):
                    agent1_obs[m][n] = CellType.OPPONENT
                elif agent1_obs[m][n] == (self.agent3.x, self.agent3.y):
                    agent1_obs[m][n] = CellType.OPPONENT
                elif agent1_obs[m][n] == self.agent1.get_front_player():
                    agent1_obs[m][n] = CellType.AGENT_FRONT
                elif agent1_obs[m][n] == self.agent2.get_front_player():
                    agent1_obs[m][n] = CellType.AGENT_FRONT
                elif agent1_obs[m][n] == self.agent3.get_front_player():
                    agent1_obs[m][n] = CellType.AGENT_FRONT
                elif agent1_obs[m][n] in food_not_coll:
                    agent1_obs[m][n] = CellType.APPLE
                elif agent1_obs[m][n] in self.agent1_beam_set:
                    agent1_obs[m][n] = CellType.BEAM
                elif agent1_obs[m][n] in self.agent2_beam_set:
                    agent1_obs[m][n] = CellType.BEAM
                elif agent1_obs[m][n] in self.agent3_beam_set:
                    agent1_obs[m][n] = CellType.BEAM
                elif agent1_obs[m][n] == 0:
                    agent1_obs[m][n] = CellType.WALL
                else:
                    agent1_obs[m][n] = CellType.EMPTY

        for m in range(agent2_obs.shape[0]):
            for n in range(agent2_obs.shape[1]):
                if agent2_obs[m][n] == (self.agent2.x, self.agent2.y):
                    agent2_obs[m][n] = CellType.PLAYER
                elif agent2_obs[m][n] == (self.agent1.x, self.agent1.y):
                    agent2_obs[m][n] = CellType.OPPONENT
                elif agent2_obs[m][n] == (self.agent3.x, self.agent3.y):
                    agent2_obs[m][n] = CellType.OPPONENT
                elif agent2_obs[m][n] == self.agent1.get_front_player():
                    agent2_obs[m][n] = CellType.AGENT_FRONT
                elif agent2_obs[m][n] == self.agent2.get_front_player():
                    agent2_obs[m][n] = CellType.AGENT_FRONT
                elif agent2_obs[m][n] == self.agent3.get_front_player():
                    agent2_obs[m][n] = CellType.AGENT_FRONT
                elif agent2_obs[m][n] in food_not_coll:
                    agent2_obs[m][n] = CellType.APPLE
                elif agent2_obs[m][n] in self.agent1_beam_set:
                    agent2_obs[m][n] = CellType.BEAM
                elif agent2_obs[m][n] in self.agent2_beam_set:
                    agent2_obs[m][n] = CellType.BEAM
                elif agent2_obs[m][n] in self.agent3_beam_set:
                    agent2_obs[m][n] = CellType.BEAM
                elif agent2_obs[m][n] == 0:
                    agent2_obs[m][n] = CellType.WALL
                else:
                    agent2_obs[m][n] = CellType.EMPTY

        for m in range(agent3_obs.shape[0]):
            for n in range(agent3_obs.shape[1]):
                if agent3_obs[m][n] == (self.agent3.x, self.agent3.y):
                    agent3_obs[m][n] = CellType.PLAYER
                elif agent3_obs[m][n] == (self.agent1.x, self.agent1.y):
                    agent3_obs[m][n] = CellType.OPPONENT
                elif agent3_obs[m][n] == (self.agent2.x, self.agent2.y):
                    agent3_obs[m][n] = CellType.OPPONENT
                elif agent3_obs[m][n] == self.agent1.get_front_player():
                    agent3_obs[m][n] = CellType.AGENT_FRONT
                elif agent3_obs[m][n] == self.agent2.get_front_player():
                    agent3_obs[m][n] = CellType.AGENT_FRONT
                elif agent3_obs[m][n] == self.agent3.get_front_player():
                    agent3_obs[m][n] = CellType.AGENT_FRONT
                elif agent3_obs[m][n] in food_not_coll:
                    agent3_obs[m][n] = CellType.APPLE
                elif agent3_obs[m][n] in self.agent1_beam_set:
                    agent3_obs[m][n] = CellType.BEAM
                elif agent3_obs[m][n] in self.agent2_beam_set:
                    agent3_obs[m][n] = CellType.BEAM
                elif agent3_obs[m][n] in self.agent3_beam_set:
                    agent3_obs[m][n] = CellType.BEAM
                elif agent3_obs[m][n] == 0:
                    agent3_obs[m][n] = CellType.WALL
                else:
                    agent3_obs[m][n] = CellType.EMPTY

        agent1_obs = convert_observation_to_rgb(agent1_obs)
        agent2_obs = convert_observation_to_rgb(agent2_obs)
        agent3_obs = convert_observation_to_rgb(agent3_obs)

        rew_n = [agent1_reward, agent2_reward, agent3_reward]
        obs_n = [agent1_obs, agent2_obs, agent3_obs]

        return rew_n, obs_n, done

    def contribute_matrix(self):
        a = np.ones([self.size_y + 2, self.size_x + 2, 3])
        a[1:-1, 1:-1, :] = 0

        for x, y in self.agent1_beam_set:
            a[y + 1, x + 1, 0] = 1
            a[y + 1, x + 1, 1] = 1
            a[y + 1, x + 1, 2] = 1
        for x, y in self.agent2_beam_set:
            a[y + 1, x + 1, 0] = 1
            a[y + 1, x + 1, 1] = 1
            a[y + 1, x + 1, 2] = 1
        for x, y in self.agent3_beam_set:
            a[y + 1, x + 1, 0] = 1
            a[y + 1, x + 1, 1] = 1
            a[y + 1, x + 1, 2] = 1

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
            if not self.agent3.is_hidden():
                delta_x, delta_y = self.agent3.move_forward_delta()
                a[self.agent3.y + 1 + delta_y, self.agent3.x + 1 + delta_x, i] = 0.5
            if not self.agent1.is_hidden():
                a[self.agent1.y + 1, self.agent1.x + 1, i] = 1 if i == self.agent1.type else 0
            if not self.agent2.is_hidden():
                a[self.agent2.y + 1, self.agent2.x + 1, i] = 1 if i == self.agent2.type else 0
            if not self.agent3.is_hidden():
                a[self.agent3.y + 1, self.agent3.x + 1, i] = 1 if i == self.agent3.type else 0

        return a

    def render_env(self):
        a = self.contribute_matrix()

        b = scipy.misc.imresize(a[:, :, 0], [5 * self.size_y, 5 * self.size_x, 1], interp='nearest')
        c = scipy.misc.imresize(a[:, :, 1], [5 * self.size_y, 5 * self.size_x, 1], interp='nearest')
        d = scipy.misc.imresize(a[:, :, 2], [5 * self.size_y, 5 * self.size_x, 1], interp='nearest')

        a = np.stack([b, c, d], axis=2)
        return a

    def train_render(self):
        a = self.contribute_matrix()

        b = scipy.misc.imresize(a[:, :, 0], [84, 84, 1], interp='nearest')
        c = scipy.misc.imresize(a[:, :, 1], [84, 84, 1], interp='nearest')
        d = scipy.misc.imresize(a[:, :, 2], [84, 84, 1], interp='nearest')

        a = np.stack([b, c, d], axis=2)
        return a


