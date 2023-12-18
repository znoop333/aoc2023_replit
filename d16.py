import numpy as np
from collections import defaultdict, deque
from math import prod, sqrt, floor, ceil

PART_2 = True

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
  

def trace_grid(contraption, init_beam=(0, 0, 'R')):
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
  queue.append(init_beam)

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

  if not PART_2:
    print_contraption(visit_map)

  return np.count_nonzero(visit_map)


def try_every_entry(contraption):
  rows, cols = contraption.shape
  max_tiles = 0

  for r in range(rows):
    # must try every edge: left edge, heading right
    max_tiles = max(max_tiles, trace_grid(contraption, (r, 0, 'R')))
    # right edge, heading left
    max_tiles = max(max_tiles, trace_grid(contraption, (r, cols-1, 'L')))

  for c in range(cols):
    # top edge, heading down
    max_tiles = max(max_tiles, trace_grid(contraption, (0, c, 'D')))
    # bottom edge, heading up
    max_tiles = max(max_tiles, trace_grid(contraption, (rows-1, c, 'U')))

  return max_tiles



def main():
  with open("d16_input.txt", "r") as f:
  # with open("d16_test_input.txt", "r") as f:
    input = f.read()

  contraption = parse_input(input)
  print(contraption)

  if not PART_2:
    answer = trace_grid(contraption)
  else:
    answer = try_every_entry(contraption)
  
  print(f'answer is {answer}')

if __name__ == '__main__':
  main()
