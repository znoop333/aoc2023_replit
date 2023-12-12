import numpy as np
from collections import defaultdict, deque
from math import prod, sqrt, floor, ceil


def parse_input(input: str):
  first_line = input.split()[0]
  width = len(first_line)
  height = len(input.split())
  graph = np.array([ch for ln in input.split() for ch in ln])
  graph = graph.reshape([height, width])
  return graph


def neighbors4(row: int, col: int, graph: np.array):
  # yield the in-bounds 4-connectivity neighbors for any position [row,col] in a 2d grid
  height, width = graph.shape
  node = graph[row][col]

  offsets = {
      'F': [(0, 1), (1, 0)],
      '7': [(0, -1), (1, 0)],
      'J': [(0, -1), (-1, 0)],
      'L': [(0, 1), (-1, 0)],
      '-': [(0, 1), (0, -1)],
      '|': [(-1, 0), (1, 0)],
      'S': [(-1, 0), (1, 0), (0, 1), (0, -1)],
      '.': [],
  }

  # 'S' is very special! it can connect to two pipes in any direction, but only if the target direction is a valid
  # connector. e.g., if 'S' is acting like 'F', it can connect on the right to '7', '-', 'J', but not 'L', '|', or '.'
  # I'll check this requirement for all nodes, even though only 'S' really requires it if the graph is valid.
  # an invalid graph might have something like 'LLL' which should be illegal because adjacent 'L' cannot connect.

  valid_targets = {
      (0, 1): ['7', '-', 'J'],
      (0, -1): ['L', '-', 'F'],
      (1, 0): ['L', '|', 'J'],
      (-1, 0): ['7', '|', 'F'],
  }

  for dr, dc in offsets[node]:
    ii = row + dr
    jj = col + dc
    if 0 <= ii < height and 0 <= jj < width and graph[ii, jj] in valid_targets[
        (dr, dc)]:
      yield graph[ii, jj], ii, jj


def neighbors4_simple(row: int, col: int, graph: np.array):
  height, width = graph.shape
  for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    ii = row + dr
    jj = col + dc
    if 0 <= ii < height and 0 <= jj < width:
      yield ii, jj


def floodfill(graph: np.array) -> int:
  height, width = graph.shape
  # we'll keep track of both which nodes have been visited and their distances using a new matrix, rather than
  # modifying the existing one in-place. This sacrifices memory in favor of speed.
  unvisited_dist = -1
  dist = unvisited_dist * np.ones((height, width), dtype=int)
  seed_r, seed_c = np.argwhere(graph == 'S')[0]
  dist[seed_r, seed_c] = 0

  q = deque()
  for ng, nr, nc in neighbors4(seed_r, seed_c, graph):
    q.append((nr, nc, 1))

  while len(q):
    node_r, node_c, node_d = q.popleft()
    if dist[node_r, node_c] == unvisited_dist:
      dist[node_r, node_c] = node_d
    else:
      dist[node_r, node_c] = min(dist[node_r, node_c], node_d)

    for ng, nr, nc in neighbors4(node_r, node_c, graph):
      prev_unvisited = dist[nr, nc] == unvisited_dist
      if prev_unvisited:
        q.append((nr, nc, node_d + 1))

  return np.max(dist), dist


def clean_graph(graph: np.array, dist: np.array) -> np.array:
  # get rid of all junk tiles. if any pipe tile was not reachable from 'S', it's junk.
  unvisited_dist = -1
  unvisited_r, unvisited_c = np.nonzero(dist == unvisited_dist)
  print_graph(graph)
  # print_graph(dist)
  for ii in range(len(unvisited_r)):
    graph[unvisited_r[ii], unvisited_c[ii]] = '.'

  print('After cleaning: ')
  print_graph(graph)

  return graph


def print_graph(graph: np.array):
  height, width = graph.shape
  s = ''
  for ii in range(height):
    s += ''.join(graph[ii, :]) + '\n'
  print(s)


def pad_graph(graph: np.array) -> np.array:
  # to make this easier to reason about, I'll pad in-between tiles so that all "exterior" regions are connected.

  # padding in-between tiles:
  # left-right: '-x' tiles become '--x' (extend the pipe left-right) for any other 'x' character (not '-')
  # 'Fx' becomes 'F-x', 'Lx' -> 'L-x', 'x7' -> 'x-7', 'xJ' -> 'x-J'
  # any other left-right characters 'xy' pad to 'x*y'. '*' will be used in the flood fill, but doesn't count as '.'

  # warning! 'S' was not working correctly with the logic above because it can be any of 'FLJ7'!
  # The mistake showed up later in remove_exterior_dots() e.g., 'S' above '|' should add a '|'. Fixed!

  height, width = graph.shape
  lr_padded = np.empty((height, 2 * width), dtype='<U1')
  for c in range(width):
    lr_padded[:, 2 * c] = graph[:, c]
    for r in range(height):
      if graph[r, c] in ('F', 'L',
                         '-') or c < width - 1 and graph[r, c +
                                                         1] in ('-', '7', 'J'):
        lr_padded[r, 2 * c + 1] = '-'
      else:
        lr_padded[r, 2 * c + 1] = ' '

  # vertical padding is similar: additional '|' characters are used to extend the pipes, and other areas
  # are filled in with '*'.
  padded = np.empty((2 * height, 2 * width), dtype='<U1')
  for r in range(height):
    padded[2 * r, :] = lr_padded[r, :]
    for c in range(2 * width):
      if lr_padded[r, c] in (
          'F', '7',
          '|') or r < height - 1 and lr_padded[r + 1, c] in ('|', 'L', 'J'):
        padded[2 * r + 1, c] = '|'
      else:
        padded[2 * r + 1, c] = ' '

  # I'll also pad 1 tile around all edges, which will connect any islands created by the pipe cutting all
  # the way across the graph.
  graph = np.pad(padded, (1, 1), mode='constant', constant_values=(' ', ' '))

  return graph


def remove_exterior_dots(graph: np.array) -> np.array:
  # use a floodfill-style algorithm: any tile reachable from the upper-left (padded edge) will be removed if it can be reached with 4-neighbor connectivity on '.' and ' ' tiles.
  # once these tiles are removed, the remaining '.' are interior by definition.

  height, width = graph.shape

  visited_tile = '*'
  seed_r, seed_c = 0, 0
  graph[seed_r, seed_c] = visited_tile

  q = deque()
  for nr, nc in neighbors4_simple(seed_r, seed_c, graph):
    if graph[nr, nc] in '. ':
      q.append((nr, nc))

  while len(q):
    node_r, node_c = q.popleft()
    if graph[node_r, node_c] == visited_tile:
      continue

    if graph[node_r, node_c] in '. ':
      print(
          f'Marking ({node_r}, {node_c}) as visited; it was {graph[node_r, node_c]}'
      )
      graph[node_r, node_c] = visited_tile
      if node_r == 2 and node_c == 4:
        1

    for nr, nc in neighbors4_simple(node_r, node_c, graph):
      if graph[nr, nc] in '. ' and graph[nr, nc] != visited_tile:
        if nr == 2 and nc == 4:
          1
        q.append((nr, nc))

  return graph


def count_dots(graph: np.array) -> int:

  return np.count_nonzero(graph == '.')


def main():
  # with open("input.txt", "r") as f:
  # with open("test_input.txt", "r") as f:
  # with open("test_input3.txt", "r") as f:
  # input = f.read()
  input = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

  graph = parse_input(input)
  answer, dist = floodfill(graph)
  graph = clean_graph(graph, dist)
  graph = pad_graph(graph)
  print_graph(graph)
  graph = remove_exterior_dots(graph)
  answer = count_dots(graph)
  print_graph(graph)

  print(f'The answer is {answer}.')


if __name__ == '__main__':
  main()
