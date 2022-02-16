import gym
print(gym.envs.registry.all())
env=gym.make('Acrobot-v1')
for i_episode in range(20):
    observation = env.reset()
    for t in range(1000):
        env.render()
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()
