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


def neighbors4_simple(row: int, col: int, graph: np.array):
  height, width = graph.shape
  for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    ii = row + dr
    jj = col + dc
    if 0 <= ii < height and 0 <= jj < width:
      yield ii, jj


class d18_VisitorInterp(d18Visitor):
  def __init__(self):
    self.root = None
    self.lagoon = None
    self.instructions = []
    self.answer = None

  # Visit a parse tree produced by d18Parser#start.
  def visitStart(self, ctx: d18Parser.StartContext):
    self.visitChildren(ctx)

    # determine how big the lagoon is
    M0, M1, N0, N1 = 0, 0, 0, 0
    r, c = 0, 0
    for dir_, dist, rgb in self.instructions:
      if dir_ == 'U':
        r -= dist
      elif dir_ == 'D':
        r += dist
      elif dir_ == 'R':
        c += dist
      elif dir_ == 'L':
        c -= dist
      M0 = min(M0, r)
      M1 = max(M1, r)
      N0 = min(N0, c)
      N1 = max(N1, c)

    # python counts from 0
    M = M1 - M0 + 1
    N = N1 - N0 + 1
    self.lagoon = np.zeros((M, N), dtype=int)

    # fill in the perimeter
    r, c = M0, N0
    for dir_, dist, rgb in self.instructions:
      if not (0 <= r - M0 < M) or not (0 <= c - N0 < N):
        # this should never happen!
        1
      if dir_ == 'U':
        r1 = r - dist
        self.lagoon[r1 - M0:r - M0, c - N0] = 1
        r = r1
      elif dir_ == 'D':
        r1 = r + dist
        self.lagoon[r - M0:r1 + 1 - M0, c - N0] = 1
        r = r1
      elif dir_ == 'R':
        c1 = c + dist
        self.lagoon[r - M0, c - N0:c1 - N0 + 1] = 1
        c = c1
      elif dir_ == 'L':
        c1 = c - dist
        self.lagoon[r - M0, c1 - N0:c - N0 + 1] = 1
        c = c1

    print(self.lagoon)
    self.answer = self.flood_interior()

  # Visit a parse tree produced by d18Parser#dig_instruction.
  def visitDig_instruction(self, ctx: d18Parser.Dig_instructionContext):
    self.instructions.append((ctx.dir_.text, int(ctx.dist.text), ctx.rgb.text))
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
