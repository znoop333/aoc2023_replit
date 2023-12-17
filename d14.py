import numpy as np
from collections import defaultdict, deque
from math import prod, sqrt, floor, ceil

PART_2 = False

def sum_to_i(i: int) -> int:
  return i*(i+1)//2

def sum_contig_int(lb: int, ub: int) -> int:
  # inclusive bounds
  return sum_to_i(ub) - sum_to_i(lb - 1) 

def test_sums():
  assert sum_to_i(4) == 10
  assert sum_to_i(1) == 1
  assert sum_contig_int(2, 4) == 9



def parse_input(input: str):
  first_line = input.split()[0]
  width = len(first_line)
  height = len(input.split())
  platform = np.array([ch for ln in input.split() for ch in ln])
  platform = platform.reshape([height, width])

  return platform


def roll_north(platform):
  rows, cols = platform.shape
  total = 0

  for c in range(cols):
    last_square = -1
    load_size = 0
    
    for r in range(rows):
      if platform[r, c] == '#':
        if load_size > 0:
          load_begin = rows - last_square - 1
          load_end = load_begin - load_size + 1
          additional_load = sum_contig_int(load_end, load_begin)
          total += additional_load
  
        last_square = r
        load_size = 0
      elif platform[r, c] == 'O':
        load_size += 1

    # we might get to the end of a column without encountering a '#' at the end
    if load_size > 0:
      load_begin = rows - last_square - 1
      load_end = load_begin - load_size + 1
      additional_load = sum_contig_int(load_end, load_begin)
      total += additional_load
      
  return total
  
  

def main():
  with open("d14_input.txt", "r") as f:
  # with open("d14_test_input.txt", "r") as f:
    input = f.read()

  platform = parse_input(input)
  print(platform)
  answer = roll_north(platform)

  print(f'answer is {answer}')


if __name__ == '__main__':
  test_sums()
  main()
