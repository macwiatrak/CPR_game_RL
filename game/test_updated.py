import matplotlib.pyplot as plt

from environment import *

episode = 0
max_episode_len = 200
gameovers = 0

while episode < 4:
    env = GameEnv()
    episode += 1
    obs_n = env.reset()
    temp = env.render_env()

    agent1_reward = 0
    agent2_reward = 0
    agent3_reward = 0

    step = 0
    gameover = False
    while not gameover:
    #while step <= max_episode_len:
        step += 1
        temp = env.render_env()
        plt.imshow(temp)
        plt.show(block=False)
        plt.pause(0.01)
        plt.clf()

        #action_n = [agent.action(obs) for agent, obs in zip(trainers, obs_n)]

        action1 = np.random.randint(8)
        action2 = np.random.randint(8)
        action3 = np.random.randint(8)
        action_n = [action1, action2, action3]

        rew_n, new_obs_n, done = env.step(action_n)
        agent1_reward += rew_n[0]
        agent2_reward += rew_n[1]
        agent3_reward += rew_n[2]

        if done:
            gameovers += 1
            print(step, 'gameovers:', gameovers)
            gameover = True  # gameover for everyone, called when all apples are collected

        if step == max_episode_len:
            gameover = True

        terminal = (step >= max_episode_len)
        #for i, agent in enumerate(trainers):
         #   agent.experience(obs_n[i], action_n[i], rew_n[i], new_obs_n[i], done_n[i], terminal)
        obs_n = new_obs_n

    print(step, 'agent1 cumulative reward: ', agent1_reward, 'agent2 cumulative reward: ', agent2_reward,
          'agent3 cumulative reward:', agent3_reward)