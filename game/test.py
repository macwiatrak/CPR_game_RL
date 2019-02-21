import matplotlib.pyplot as plt

from environment import *

for i in range(3):
    env = GameEnv()
    env.reset()

    temp = env.render_env()
    i = 0
    agent1_reward = 0
    agent2_reward = 0
    agent3_reward = 0

    #while True:
    for i in range(5):
        temp = env.render_env()
        #plt.imshow(temp)
        #plt.show(block=False)
        #plt.pause(0.01)
        #plt.clf()
        action1 = np.random.randint(8)
        action2 = np.random.randint(8)
        action3 = np.random.randint(8)

        r1, r2, r3, obs_1, obs_2, obs_3 = env.step(action1, action2, action3)
        i += 1
        agent1_reward += r1
        agent2_reward += r2
        agent2_reward += r3

        if r1 or r2 or r3:
            print(i, 'agent1 action: ', action1, 'agent2 action: ', action2, 'agent3 action: ', action3)
            #print(i, 'agent1 reward: ', r1, 'agent2 reward', r2)
        print(obs_1)
    print(i, 'agent1 cumulative reward: ', agent1_reward, 'agent2 cumulative reward: ', agent2_reward)