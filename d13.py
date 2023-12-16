import numpy as np
from collections import defaultdict, deque
from math import prod, sqrt, floor, ceil

PART_2 = False


def parse_input(input: str):
  puzzles = []
  current_puzzle = None
  for row, line in enumerate(input.split('\n')):
    if len(line):
      if current_puzzle is None:
        current_puzzle = np.array([[c for c in line]])
      else:
        current_puzzle = np.append(current_puzzle, [[c for c in line]], axis=0)
    else:
      puzzles.append(current_puzzle)
      current_puzzle = None
  return puzzles


def reflect_ud(puzzle):
  rows, cols = puzzle.shape
  ud_mirrors = 0
  for r in range(0, rows - 1):
    if np.all(puzzle[r, :] == puzzle[r + 1, :]):
      if r == 0:
        ud_mirrors = 1
        continue

      max_rows = min(r, rows - r - 2)
      # print(f'max_rows: {max_rows} must check {range(r - 1, r - max_rows - 1, -1)} against {range(r + 2, r + max_rows + 2, 1)}')
      for i, j in zip(range(r - 1, r - max_rows - 1, -1),
                      range(r + 2, r + max_rows + 2, 1), strict=True):
        if np.any(puzzle[i, :] != puzzle[j, :]):
          break
      else:
        ud_mirrors = r + 1
  return ud_mirrors


def reflect_lr(puzzle):
  return reflect_ud(puzzle.T)


def main():
  with open("d13_input.txt", "r") as f:
  # with open("d13_test_input.txt", "r") as f:
    input = f.read()

  puzzles = parse_input(input)
  print(puzzles[0])

  answer = 0
  for p in puzzles:
    answer += 100 * reflect_ud(p) + reflect_lr(p)
    print(reflect_ud(p), reflect_lr(p))

  print(f'answer is {answer}')


if __name__ == '__main__':
  main()
