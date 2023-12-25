import dataclasses
import sys
from antlr4 import *
from gen.d19Lexer import d19Lexer
from gen.d19Parser import d19Parser
from gen.d19Visitor import d19Visitor
import numpy as np
from dataclasses import dataclass
from typing import List, Dict
import datetime
import time
from math import prod, lcm
from collections import defaultdict, deque
import functools

PART2 = False
# PART2 = True


class d19_VisitorInterp(d19Visitor):
  def __init__(self):
    self.root = None
    self.lagoon = None
    self.instructions = []
    self.answer = None

    # Visit a parse tree produced by d19Parser#start.
    def visitStart(self, ctx:d19Parser.StartContext):
      return self.visitChildren(ctx)


    # Visit a parse tree produced by d19Parser#part.
    def visitPart(self, ctx:d19Parser.PartContext):
      return self.visitChildren(ctx)


    # Visit a parse tree produced by d19Parser#rule.
    def visitRule(self, ctx:d19Parser.RuleContext):
      return self.visitChildren(ctx)


    # Visit a parse tree produced by d19Parser#clause_list.
    def visitClause_list(self, ctx:d19Parser.Clause_listContext):
      return self.visitChildren(ctx)


    # Visit a parse tree produced by d19Parser#clause.
    def visitClause(self, ctx:d19Parser.ClauseContext):
      return self.visitChildren(ctx)


    # Visit a parse tree produced by d19Parser#comparison.
    def visitComparison(self, ctx:d19Parser.ComparisonContext):
      return self.visitChildren(ctx)


    # Visit a parse tree produced by d19Parser#token.
    def visitToken(self, ctx:d19Parser.TokenContext):
      return self.visitChildren(ctx)

