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
from collections import defaultdict
import functools


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
    M, N = 0, 0
    r, c = 0, 0
    for dir_, dist, rgb in self.instructions:
      if dir_ == 'U':
        r -= dist
        M = max(M, r)
      elif dir_ == 'D':
        r += dist
        M = max(M, r)
      elif dir_ == 'R':
        c += dist
        N = max(N, c)
      elif dir_ == 'L':
        c -= dist
        N = max(N, c)

    # python counts from 0
    M += 1
    N += 1
    self.lagoon = np.zeros((M, N), dtype=int)

    # fill in the perimeter
    r, c = 0, 0
    for dir_, dist, rgb in self.instructions:
      if dir_ == 'U':
        r1 = r - dist
        self.lagoon[r1:r+1, c] = 1
        r = r1
      elif dir_ == 'D':
        r1 = r + dist
        self.lagoon[r1:r, c] = 1
        r = r1
      elif dir_ == 'R':
        c1 = c + dist
        self.lagoon[r, c:c1+1] = 1
        c = c1
      elif dir_ == 'L':
        c1 = c - dist
        self.lagoon[r, c1:c+1] = 1
        c = c1

    print(self.lagoon)
    1

  # Visit a parse tree produced by d18Parser#dig_instruction.
  def visitDig_instruction(self, ctx: d18Parser.Dig_instructionContext):
    self.instructions.append((ctx.dir_.text, int(ctx.dist.text), ctx.rgb.text))
    return self.visitChildren(ctx)
