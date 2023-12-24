import dataclasses
import sys
from antlr4 import *
from gen.d18Lexer import d18Lexer
from gen.d18Parser import d18Parser
from gen.d18Visitor import d18Visitor
import numpy as np
from dataclasses import dataclass
from typing import List, Dict
import datetime
import time
from math import prod, lcm
from collections import defaultdict, deque
import functools

PART2 = True


def neighbors4_simple(row: int, col: int, graph: np.array):
  height, width = graph.shape
  for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    ii = row + dr
    jj = col + dc
    if 0 <= ii < height and 0 <= jj < width:
      yield ii, jj


def print_lagoon(lagoon):
  rows, cols = lagoon.shape
  s = ''
  for r in lagoon:
    for x in r:
      if x:
        s += f'{x:d}'
      else:
        s += ' '
    s += '\n'
  print(s)


def solve_sparse_lagoon(instructions):
  # determine how big the lagoon is
  area = 0
  y0, y1, x0, x1 = 0, 0, 0, 0
  x, y = 0, 0
  for _, _, dir_, dist in instructions:
    if dir_ == 'U':
      y += dist
    elif dir_ == 'D':
      y -= dist
    elif dir_ == 'R':
      x += dist
    elif dir_ == 'L':
      x -= dist
    y0 = min(y0, y)
    y1 = max(y1, y)
    x0 = min(x0, x)
    x1 = max(x1, x)

  # see d18_notes.txt for ideas behind the implementation below
  x, y = 0, 0
  perimeter = 0
  # for _, _, dir_, dist in instructions:
  for dir_, dist, _, _ in instructions:
    if dir_ == 'U':
      area -= (x - x0) * dist
      y += dist
      perimeter += dist
    elif dir_ == 'D':
      area += (x - x0) * (dist - 1)
      y -= dist
      perimeter += dist
    elif dir_ == 'R':
      # area += dist
      x += dist
      perimeter += dist
    elif dir_ == 'L':
      # area += dist
      x -= dist
      perimeter += dist

  print(f'perimeter {perimeter}')
  return area + perimeter


class d18_VisitorInterp(d18Visitor):
  def __init__(self):
    self.root = None
    self.lagoon = None
    self.instructions = []
    self.answer = None

  # Visit a parse tree produced by d18Parser#start.
  def visitStart(self, ctx: d18Parser.StartContext):
    self.visitChildren(ctx)

    if PART2:
      # Part 2 requires a totally different strategy. Solving Part 1 with a flood fill is OK because
      # the dimensions aren't too big, but for Part 2, just allocating the lagoon memory is > 5 TiB for the test case
      # input, and probably much bigger than that for the real input!
      self.answer = solve_sparse_lagoon(self.instructions)
      return

    # determine how big the lagoon is
    y0, y1, x0, x1 = 0, 0, 0, 0
    x, y = 0, 0
    for dir_, dist, _, _ in self.instructions:
      if dir_ == 'U':
        y += dist
      elif dir_ == 'D':
        y -= dist
      elif dir_ == 'R':
        x += dist
      elif dir_ == 'L':
        x -= dist
      y0 = min(y0, y)
      y1 = max(y1, y)
      x0 = min(x0, x)
      x1 = max(x1, x)

    # python counts from 0
    M = y1 - y0 + 1
    N = x1 - x0 + 1

    self.lagoon = np.zeros((M, N), dtype=int)

    x2col = lambda xx: xx - x0
    y2row = lambda yy: -yy + y1

    # fill in the perimeter
    x, y = 0, 0
    for dir_, dist, _, _ in self.instructions:
      if dir_ == 'U':
        self.lagoon[y2row(y + dist): y2row(y) + 1, x2col(x)] = 1
        y += dist
      elif dir_ == 'D':
        self.lagoon[y2row(y): y2row(y - dist) + 1, x2col(x)] = 1
        y -= dist
      elif dir_ == 'R':
        self.lagoon[y2row(y), x2col(x): x2col(x + dist)] = 1
        x += dist
      elif dir_ == 'L':
        self.lagoon[y2row(y), x2col(x - dist): x2col(x)] = 1
        x -= dist

      if not (0 <= x2col(x) <= M and 0 <= y2row(y) <= N):
        # this should never happen!
        print(
          f'Drawing went out of bounds with instruction {dir_, dist} at {x, y} resulting in {y2row(y), x2col(x)}')

    print_lagoon(self.lagoon)
    self.answer = self.flood_interior()

  # Visit a parse tree produced by d18Parser#dig_instruction.
  def visitDig_instruction(self, ctx: d18Parser.Dig_instructionContext):
    hex_to_dir = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
    real_dir = hex_to_dir[ctx.real_direction.text[-1]]
    real_dist = int(ctx.real_direction.text[:-1], 16)
    self.instructions.append((ctx.dir_.text, int(ctx.dist.text), real_dir, real_dist))
    return self.visitChildren(ctx)

  def flood_interior(self):
    # to make this easier to reason about, I'll pad the edges so that all "exterior" regions are connected.
    # I need to use a different value for the padding (-1) than the perimeter (1s) or other parts (0s) because
    # at the end, I want to count the number of interior 0s and also all 1s, but none of the padding
    lagoon = np.pad(self.lagoon, (1, 1), mode='constant', constant_values=(-1, -1))

    # flood fill the exterior, replacing all exterior 0s with -1, then count the number of 1s and 0s remaining
    q = deque()
    q.append([0, 0])
    while len(q):
      node_r, node_c = q.popleft()
      if lagoon[node_r, node_c] == -2:
        # already visited
        continue
      lagoon[node_r, node_c] = -2
      for nr, nc in neighbors4_simple(node_r, node_c, lagoon):
        if lagoon[nr, nc] in (-1, 0):
          q.append([nr, nc])

    lagoon[lagoon == 0] = 1
    print(lagoon)
    return np.count_nonzero(lagoon == 1)
