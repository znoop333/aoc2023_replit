import numpy as np
from collections import defaultdict, deque
from math import prod, sqrt, floor, ceil

PART_2 = False

def parse_input(input: str):
  first_line = input.split()[0]
  width = len(first_line)
  height = len(input.split())
  contraption = np.array([ch for ln in input.split() for ch in ln])
  contraption = contraption.reshape([height, width])

  return contraption


def trace_grid(contraption):
  value = 0

  return value



def main():
  # with open("d16_input.txt", "r") as f:
  with open("d16_test_input.txt", "r") as f:
    input = f.read()

  contraption = parse_input(input)
  print(contraption)

  answer = 0

  print(f'answer is {answer}')


if __name__ == '__main__':
  main()
