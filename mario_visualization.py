#!/usr/bin/env python3

import os
import sys

from pyboy import PyBoy, WindowEvent

# # Makes us able to import PyBoy from the directory below
# file_path = os.path.dirname(os.path.realpath(__file__))
# sys.path.insert(0, file_path + "/..")
#
# # Check if the ROM is given through argv
# if len(sys.argv) > 1:
#     filename = sys.argv[1]
# else:
#     print("Usage: python mario_boiler_plate.py [ROM file]")
#     exit(1)

filename="Super Mario Land (World).gb"
quiet=False

# quiet = "--quiet" in sys.argv
pyboy = PyBoy(filename, window_type="headless" if quiet else "SDL2", window_scale=3, debug=not quiet, game_wrapper=True)
pyboy.set_emulation_speed(1)
assert pyboy.cartridge_title() == "SUPER MARIOLAN"

mario = pyboy.game_wrapper()
pyboy.openai_gym()
mario.start_game()

pyboy.openai_gym.PyBoyGymEnv(mario)


assert mario.score == 0
assert mario.lives_left == 2
assert mario.time_left == 400
assert mario.world == (1, 1)
assert mario.fitness == 0 # A built-in fitness score for AI development
last_fitness = 0

print(mario)
for _ in range(200):
    last_fitness = mario.fitness
    pyboy.tick()
    print(mario)


pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
for _ in range(1000):
    assert mario.fitness >= last_fitness
    last_fitness = mario.fitness

    pyboy.tick()
    if mario.lives_left == 1:
        assert last_fitness == 27700
        assert mario.fitness == 17700 # Loosing a live, means 10.000 points in this fitness scoring
        print(mario)
        break
    else:
        print("Mario didn't die?")
        exit(2)

mario.reset_game()
assert mario.lives_left == 2

pyboy.stop()

import gym
env = gym.make('CartPole-v0')
env.reset()
for _ in range(1000):
    env.render()
    env.step(env.action_space.sample()) # take a random action
env.close()

import gym
env = gym.make('CartPole-v0')
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
