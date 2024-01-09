import numpy as np
from collections import defaultdict, deque
from math import prod, sqrt, floor, ceil

# PART_2 = False
PART_2 = True


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
  if not PART_2:
    max_smudges = 0
  else:
    max_smudges = 1

  for r in range(0, rows - 1):
    smudges = np.count_nonzero(puzzle[r, :] != puzzle[r + 1, :])
    if smudges > max_smudges:
      continue

    if r == 0:
      ud_mirrors = 1
      break

    max_rows = min(r, rows - r - 2)
    # print(f'max_rows: {max_rows} must check {range(r - 1, r - max_rows - 1, -1)} against {range(r + 2, r + max_rows + 2, 1)}')
    for i, j in zip(range(r - 1, r - max_rows - 1, -1),
                    range(r + 2, r + max_rows + 2, 1),
                    strict=True):
      smudges += np.count_nonzero(puzzle[i, :] != puzzle[j, :])
      if smudges > max_smudges:
        break
    else:
      ud_mirrors = r + 1
      break
  return ud_mirrors


def reflect_lr(puzzle):
  return reflect_ud(puzzle.T)


def main():
  with open("d13_input.txt", "r") as f:
  # with open("d13_test_input.txt", "r") as f:
    input = f.read()

  puzzles = parse_input(input)

  answer = 0
  for p in puzzles:
    ud = reflect_ud(p)
    lr = reflect_lr(p)
    if not PART_2:
      answer += 100 * ud + lr
    else:
      answer += 100 * ud

    # print(p)
    print(ud, lr)

  print(f'answer is {answer}')


if __name__ == '__main__':
  main()
