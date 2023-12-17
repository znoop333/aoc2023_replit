import numpy as np
from collections import defaultdict, deque
from math import prod, sqrt, floor, ceil

PART_2 = False

def parse_input(input: str):
  steps = []
  for instruction in input.split(','):
    steps.append(instruction)

  return steps


def hash_instruction(instruction):
  value = 0
  for c in instruction:
    value = (value+ ord(c))*17 % 256

  return value



def main():
  with open("d15_input.txt", "r") as f:
  # with open("d15_test_input.txt", "r") as f:
    input = f.read()

  steps = parse_input(input)
  # print(steps)
  
  answer = 0
  for instruction in steps:
    answer += hash_instruction(instruction)

  print(f'answer is {answer}')


if __name__ == '__main__':
  main()
