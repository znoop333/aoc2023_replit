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

def print_contraption(contraption):
  rows, cols = contraption.shape
  s = ''
  for r in contraption:
    s += ''.join([str(x) for x in r])
    s += '\n'
  print(s)
  

def trace_grid(contraption):
  rows, cols = contraption.shape
  value = 0

  # We need to keep track of the current state (row, col, direction) for a ray 
  # until it passes out of bounds. Every node it visits needs to be marked as visited,
  # and the final value is the count of the number of nodes visited. Visiting the 
  # same node multiple times does not count more than once.
  visited = set()
  queue = deque()
  visit_map = np.zeros((rows, cols), dtype=int)

  # the beam starts in the top-left (0,0) heading right ('R'), which we'll represent
  # as entering (0, 0) while heading 'R'.
  queue.append((0, 0, 'R'))

  # default directions, used for '.' and some other cases
  directions = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1,0)}
  
  while queue:
    row, col, direction = queue.popleft()
    if not (0 <= row < rows and 0 <= col < cols):
      continue

    if (row, col, direction) in visited:
      continue

    visit_map[row, col] = 1
    visited.add((row, col, direction))
      
    # the default is to continue in the same direction
    dr, dc = directions[direction]
    
    if contraption[row, col] == '.':
      # continue in the same direction
      queue.append((row + dr, col + dc, direction))
    elif contraption[row, col] == '|':
      if direction in 'UD':
        queue.append((row + dr, col + dc, direction))
      elif direction in 'RL':
        queue.append((row - 1, col, 'U'))
        queue.append((row + 1, col, 'D'))
    elif contraption[row, col] == '-':
      if direction in 'RL':
        queue.append((row + dr, col + dc, direction))
      elif direction in 'UD':
        queue.append((row, col+1, 'R'))
        queue.append((row, col-1, 'L'))
    elif contraption[row, col] == '/':
      if direction == 'R':
        queue.append((row - 1, col, 'U'))
      elif direction == 'L':
        queue.append((row + 1, col, 'D'))
      elif direction == 'U':
        queue.append((row, col+1, 'R'))
      elif direction == 'D':
        queue.append((row, col-1, 'L'))
    elif contraption[row, col] == '\\':
        if direction == 'R':
          queue.append((row + 1, col, 'D'))
        elif direction == 'L':
          queue.append((row - 1, col, 'U'))
        elif direction == 'U':
          queue.append((row, col-1, 'L'))
        elif direction == 'D':
          queue.append((row, col+1, 'R'))
  
  print_contraption(visit_map)

  return np.count_nonzero(visit_map)



def main():
  with open("d16_input.txt", "r") as f:
  # with open("d16_test_input.txt", "r") as f:
    input = f.read()

  contraption = parse_input(input)
  print(contraption)

  answer = trace_grid(contraption)

  print(f'answer is {answer}')


if __name__ == '__main__':
  main()
