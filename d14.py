import numpy as np
from collections import defaultdict, deque
from math import prod, sqrt, floor, ceil

PART_2 = False


def parse_input(input: str):
  first_line = input.split()[0]
  width = len(first_line)
  height = len(input.split())
  platform = np.array([ch for ln in input.split() for ch in ln])
  platform = platform.reshape([height, width])

  return platform


def roll_north(platform):
  rows, cols = platform.shape


def main():
  # with open("d14_input.txt", "r") as f:
  with open("d14_test_input.txt", "r") as f:
    input = f.read()

  platform = parse_input(input)
  print(platform)

  answer = 0

  print(f'answer is {answer}')


if __name__ == '__main__':
  main()
