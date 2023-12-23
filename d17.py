import numpy as np
from collections import defaultdict, deque
import heapq
from math import prod, sqrt, floor, ceil

PART_2 = False


def parse_input(input: str):
  first_line = input.split()[0]
  width = len(first_line)
  height = len(input.split())
  factory_map = np.array([int(ch) for ln in input.split() for ch in ln], dtype=int)
  factory_map = factory_map.reshape([height, width])

  return factory_map


def print_factory_map(contraption):
  rows, cols = contraption.shape
  s = ''
  for r in contraption:
    for x in r:
      x = min(x, 999)
      s += f' {x:03d}'
    s += '\n'
  print(s)


def print_path(contraption, prev):
  rows, cols = contraption.shape
  r, c, direction = [(r_, c_, d_) for r_, c_, d_ in prev.keys() if r_ == rows - 1 and c_ == cols - 1][0]
  path_visited = set()
  while not (r, c) == (0, 0):
    path_visited.add((r, c))
    r, c, direction = prev[(r, c, direction)]

  path_visited.add((0, 0))

  s = ''
  for r in range(rows):
    for c in range(cols):
      if (r, c) in path_visited:
        s += ' ' + str(contraption[r, c])
      else:
        s += ' .'
    s += '\n'
  print(s)


def neighbors4_simple(row: int, col: int, graph: np.array):
  height, width = graph.shape
  for dr, dc, direction in [(0, 1, 'R'), (0, -1, 'L'), (1, 0, 'D'), (-1, 0, 'U')]:
    ii = row + dr
    jj = col + dc
    if 0 <= ii < height and 0 <= jj < width:
      yield ii, jj, direction


def min_heat_loss(factory_map):
  rows, cols = factory_map.shape
  value = 0
  dist = dict()
  visited = set()
  prev = {}

  # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Using_a_priority_queue

  # minheap format: distance so far, the source tile, direction being traveled, travel counter.
  h = [(0, 0, 0, '', 0)]

  while h:
    d, r, c, direction, travel_counter = heapq.heappop(h)

    if r == rows - 1 and c == cols - 1:
      # we found the shortest path to the target!
      value = d
      break

    visited.add((r, c, direction))
    dist[(r, c, direction)] = d

    # print_factory_map(dist)

    for neighbor_r, neighbor_c, neighbor_dir in neighbors4_simple(r, c, factory_map):
      # determine if travel_counter should increase
      if direction == neighbor_dir:
        tc = travel_counter + 1
      else:
        tc = 0

      if tc >= 2:
        # cannot add this edge:
        # to satisfy the rule that 3 moves in the same direction are illegal, we'll pretend there's no edge after travel counter is 2.
        continue

      next_node = neighbor_r, neighbor_c, neighbor_dir
      if next_node in visited:
        continue

      alt = d + factory_map[neighbor_r, neighbor_c]
      if next_node not in dist or alt < dist[next_node]:
        if next_node not in prev:
          prev[next_node] = r, c, direction
          heapq.heappush(h, (alt, neighbor_r, neighbor_c, neighbor_dir, tc))

  # print_factory_map(dist)
  print_path(factory_map, prev)
  return value


def main():
  # with open("d17_input.txt", "r") as f:
  with open("d17_test_input.txt", "r") as f:
    input = f.read()

  input = """112999
911111"""

  factory_map = parse_input(input)
  print_factory_map(factory_map)

  answer = min_heat_loss(factory_map)

  print(f'answer is {answer}')


if __name__ == '__main__':
  main()
