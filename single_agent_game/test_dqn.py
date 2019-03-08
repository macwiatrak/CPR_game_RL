import matplotlib.pyplot as plt

from environment import *
from dqn_agent import *
episode = 0
max_episode_len = 1000
gameovers = 0
DQN_agent = DQNAgent(8)

while episode < 2000:
    env = GameEnv()
    episode += 1
    obs_n = env.reset()
    obs_n = obs_n.reshape(1, obs_n.shape[0], obs_n.shape[1], obs_n.shape[2])
    #env.render_env()

    agent1_reward = 0

    step = 0
    gameover = False
    while not gameover:
        step += 1
        #env.render_env()
        #action_n = [agent.action(obs) for agent, obs in zip(trainers, obs_n)]

        # take a random action
        #obs_n[0] = obs_n[0].reshape(1, obs_n[0].shape[0], obs_n[0].shape[1], obs_n[0].shape[2])
        action1 = DQN_agent.act(obs_n)
        #action_n = [np.random.randint(8) for agent in range(3)]
        action_n = [action1]

        rew_n, new_obs_n, done = env.step(action_n)
        new_obs_n = new_obs_n.reshape(1, new_obs_n.shape[0], new_obs_n.shape[1], new_obs_n.shape[2])

        agent1_reward += rew_n

        terminal = (step >= max_episode_len)
        DQN_agent.remember(obs_n, action1, rew_n, new_obs_n, terminal)
        if done or terminal:
            gameovers += 1
            print(step, 'gameovers:', gameovers)
            gameover = True  # gameover for everyone, called when all apples are collected
        #for i, agent in enumerate(trainers):
         #   agent.experience(obs_n[i], action_n[i], rew_n[i], new_obs_n[i], done_n[i], terminal)
        obs_n = new_obs_n
        DQN_agent.experience_replay()

    print(step, 'agent1 cumulative reward: ', agent1_reward)