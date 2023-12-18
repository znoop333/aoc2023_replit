import numpy as np
from collections import defaultdict, deque
import heapq
from math import prod, sqrt, floor, ceil

PART_2 = False


def parse_input(input: str):
  first_line = input.split()[0]
  width = len(first_line)
  height = len(input.split())
  factory_map = np.array([int(ch) for ln in input.split() for ch in ln])
  factory_map = factory_map.reshape([height, width])

  return factory_map


def print_factory_map(contraption):
  rows, cols = contraption.shape
  s = ''
  for r in contraption:
    s += ''.join([str(x) for x in r])
    s += '\n'
  print(s)


def min_heat_loss(factory_map):
  rows, cols = factory_map.shape
  value = 0
  

  return value


def main():
  # with open("d17_input.txt", "r") as f:
  with open("d17_test_input.txt", "r") as f:
    input = f.read()

  factory_map = parse_input(input)
  print_factory_map(factory_map)

  answer = min_heat_loss(factory_map)

  print(f'answer is {answer}')


if __name__ == '__main__':
  main()
