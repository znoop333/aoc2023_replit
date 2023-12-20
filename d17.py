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
    s += ' '.join([str(x) for x in r])
    s += '\n'
  print(s)


def neighbors4_simple(row: int, col: int, graph: np.array):
  height, width = graph.shape
  for dr, dc, dir in [(0, 1, 'D'), (0, -1, 'U'), (1, 0, 'R'), (-1, 0, 'L')]:
    ii = row + dr
    jj = col + dc
    if 0 <= ii < height and 0 <= jj < width:
      yield ii, jj, dir


def min_heat_loss(factory_map):
  rows, cols = factory_map.shape
  value = 0
  dist = np.inf * np.ones((rows, cols), dtype=int)
  visited = np.zeros((rows, cols), dtype=int)

  # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Using_a_priority_queue

  # minheap format: distance so far, the source tile, direction being traveled, travel counter.
  h = [(factory_map[rows - 1, cols - 1], rows - 1, cols - 1, '', 0)]

  while h:
    d, r, c, dir, travel_counter = heapq.heappop(h)

    if r == 0 and c == 0:
      # we found the shortest path to the start!
      value = d
      break

    if visited[r, c]:
      continue

    visited[r, c] = 1
    dist[r, c] = d

    # print_factory_map(dist)
    # print_factory_map(visited)

    for neighbor_r, neighbor_c, neighbor_dir in neighbors4_simple(r, c, factory_map):
      # determine if travel_counter should increase
      if dir == neighbor_dir:
        tc = travel_counter + 1
      else:
        tc = 0

      if travel_counter >= 3:
        # cannot add this edge:
        # to satisfy the rule that 3 moves in the same direction are illegal, we'll pretend there's no edge after travel counter is 2.
        continue

      alt = d + factory_map[neighbor_r, neighbor_c]
      if alt < dist[neighbor_r, neighbor_c]:
        heapq.heappush(h, (alt, neighbor_r, neighbor_c, neighbor_dir, tc))

  print_factory_map(dist)
  print_factory_map(visited)
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
