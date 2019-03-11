

from environment import *

episode = 0
max_episode_len = 10
gameovers = 0

while episode < 10:
    env = GameEnv()
    episode += 1
    obs_n = env.reset()
    env.render_env()
    print(obs_n)

    agent1_reward = 0

    step = 0
    gameover = False
    while not gameover:
        step += 1
        env.render_env()
        #action_n = [agent.action(obs) for agent, obs in zip(trainers, obs_n)]

        # take a random action
        action_n = [np.random.randint(8)]
        #action_n = [action1, action2, action3]

        rew_n, new_obs_n, done = env.step(action_n)

        agent1_reward += rew_n

        terminal = (step >= max_episode_len)

        if done or terminal:
            gameovers += 1
            print(step, 'gameovers:', gameovers)
            gameover = True  # gameover for everyone, called when all apples are collected
        #for i, agent in enumerate(trainers):
         #   agent.experience(obs_n[i], action_n[i], rew_n[i], new_obs_n[i], done_n[i], terminal)
        obs_n = new_obs_n

    print(step, 'agent1 cumulative reward: ', agent1_reward)