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
    self.parts = []
    self.answer = None

  # Visit a parse tree produced by d19Parser#start.
  def visitStart(self, ctx: d19Parser.StartContext):
    self.visitChildren(ctx)

    print('int main(void) {')
    print('int total = 0;')
    for p in self.parts:
      print(f'    total += fn_in({p["x"]}, {p["m"]}, {p["a"]}, {p["s"]}, {p["total"]});')
    print('printf("%d", total);')
    print('}')

  # Visit a parse tree produced by d19Parser#part.
  def visitPart(self, ctx: d19Parser.PartContext):
    part = {'x': int(ctx.xval.text), 'm': int(ctx.mval.text), 'a': int(ctx.aval.text), 's': int(ctx.sval.text)}
    part['total'] = part['x'] + part['m'] + part['a'] + part['s']
    self.parts.append(part)

  # Visit a parse tree produced by d19Parser#rule.
  def visitRule(self, ctx: d19Parser.RuleContext):
    print(f'int fn_{ctx.name.text}(int x, int m, int a, int s, int total) ' + '{')
    self.visitChildren(ctx)
    print('}\n')

  # Visit a parse tree produced by d19Parser#clause_list.
  def visitClause_list(self, ctx: d19Parser.Clause_listContext):
    return self.visitChildren(ctx)

  # Visit a parse tree produced by d19Parser#clause.
  def visitClause(self, ctx: d19Parser.ClauseContext):
    return self.visitChildren(ctx)

  # Visit a parse tree produced by d19Parser#comparison.
  def visitComparison(self, ctx: d19Parser.ComparisonContext):
    self.visitChildren(ctx)
    val = ctx.val.getChild(0).getText()
    s = f'if ({ctx.attribute.text} {ctx.op.text} {ctx.rval.text}) '
    if val == 'R':
      s += 'return 0;'
    elif val == 'A':
      s += 'return total;'
    else:
      s += f'return fn_{val}(x, m, a, s, total);'
    print(s)

  # Visit a parse tree produced by d19Parser#token.
  def visitToken(self, ctx: d19Parser.TokenContext):
    return self.visitChildren(ctx)

  def visitToken_clause(self, ctx: d19Parser.Token_clauseContext):
    val = ctx.getChild(0).getText()
    s = ''
    if val == 'R':
      s += 'return 0;'
    elif val == 'A':
      s += 'return total;'
    else:
      s += f'return fn_{val}(x, m, a, s, total);'
    print(s)
    # self.visitChildren(ctx)
