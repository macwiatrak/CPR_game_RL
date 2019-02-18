from keras import layers
from keras import models

model = models.Sequential()
model.add(layers.Dense(32, activation='relu', input_shape=(X_TO_INPUT)))
mmodel.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(8)) # output layer, 1 output for each action

DISCOUNT_RATE = 0.99
BATCH_SIZE = 128
EPSILON_GREEDY_START = 1.0
EPSILON_GREEDY_STOP = 0.1
MEMORY_SIZE = 10000