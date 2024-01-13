import numpy as np
from collections import defaultdict, deque
from math import prod, sqrt, floor, ceil

PART_2 = False
# PART_2 = True

"""
PART_2: 
In each pattern, fix the smudge and find the different line of reflection. What number do you get after summarizing the
new reflection line in each pattern in your notes?

Does that mean I must determine which line had the original solution in part1 and make sure I do not use that line for
the part2 solution?

Or does it mean that UD and LR must both use the same smudge?
"""


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
  if not PART_2:
    max_smudges = 0
  else:
    max_smudges = 1

  for r in range(0, rows - 1):
    smudges = np.count_nonzero(puzzle[r, :] != puzzle[r + 1, :])
    if smudges > max_smudges:
      continue

    if r == 0 and smudges == max_smudges:
      if smudges == 1:
        smudge_location = 0, np.nonzero(puzzle[r, :] != puzzle[r + 1, :])[0][0]
        yield 1, smudge_location
        continue
      else:
        yield 1, None
        continue

    max_rows = min(r, rows - r - 2)
    # print(f'max_rows: {max_rows} must check {range(r - 1, r - max_rows - 1, -1)} against {range(r + 2, r + max_rows + 2, 1)}')
    for i, j in zip(range(r - 1, r - max_rows - 1, -1),
                    range(r + 2, r + max_rows + 2, 1),
                    strict=True):
      num_errors = np.count_nonzero(puzzle[i, :] != puzzle[j, :])

      if num_errors == 1:
        smudge_location = r, np.nonzero(puzzle[i, :] != puzzle[j, :])[0][0]
      else:
        smudge_location = None

      if smudges + num_errors > max_smudges:
        break
      smudges += num_errors
    else:
      yield r + 1, smudge_location


def reflect_lr(puzzle):
  return reflect_ud(puzzle.T)


def main():
  # with open("d13_input.txt", "r") as f:
  with open("d13_test_input.txt", "r") as f:
    input = f.read()

  puzzles = parse_input(input)

  answer = 0
  for p in puzzles:
    for ud_, smudge_loc in reflect_ud(p):
      ud = ud_

    for lr_, smudge_loc in reflect_lr(p):
      lr = lr_

    answer += 100 * ud + lr

    # print(p)
    print(ud, lr)

  print(f'answer is {answer}')


if __name__ == '__main__':
  main()
