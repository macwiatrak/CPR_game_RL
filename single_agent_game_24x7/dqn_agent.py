import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.optimizers import Adam
from keras import layers

GAMMA = 0.99
LEARNING_RATE = 0.00025

MEMORY_SIZE = 1000000
BATCH_SIZE = 32

EPS_MAX = 1.0
EPS_MIN = 0.1
EPS_DECAY_LEN = 100000
EPS_LEARNING_START = 500
EXPLORATION_DECAY = 0.995


class DQNAgent:

    def __init__(self, action_space):
        self.exploration_rate = EPS_MAX

        self.action_space = action_space
        self.memory = deque(maxlen=MEMORY_SIZE)

        self.model = Sequential()
        self.model.add(layers.Dense(32, input_shape=(3*5*13,), activation="relu"))
        self.model.add(layers.Dense(32, activation="relu"))
        self.model.add(layers.Dense(self.action_space, activation="softmax"))
        self.model.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE))

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() < self.exploration_rate:
            return random.randrange(self.action_space)
        q_values = self.model.predict(np.expand_dims(state, axis=0))
        return np.argmax(q_values[0])

    def experience_replay(self, step_overall):
        if len(self.memory) < BATCH_SIZE:
            return
        batch = random.sample(self.memory, BATCH_SIZE)
        for state, action, reward, state_next, terminal in batch:
            q_update = reward
            if not terminal:
                q_update = (reward + GAMMA * np.amax(self.model.predict(np.expand_dims(state_next, axis=0))[0]))
            q_values = self.model.predict(np.expand_dims(state, axis=0))
            q_values[0][action] = q_update
            self.model.fit(np.expand_dims(state, axis=0), q_values, verbose=0)
        self.exploration_rate = EPS_MIN + max(0., (EPS_MAX-EPS_MIN) *
                                        (EPS_DECAY_LEN - max(0., step_overall - EPS_LEARNING_START)) / EPS_DECAY_LEN)