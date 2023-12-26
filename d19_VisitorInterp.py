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


class d19_VisitorInterp(d19Visitor):
  def __init__(self, filehandle):
    self.root = None
    self.parts = []
    self.answer = None
    self.filehandle = filehandle

  # Visit a parse tree produced by d19Parser#start.
  def visitStart(self, ctx: d19Parser.StartContext):
    self.visitChildren(ctx)

    s = 'int main(void) {\n'
    s += 'int total = 0;\n'
    for p in self.parts:
      s += f'    total += fn_in({p["x"]}, {p["m"]}, {p["a"]}, {p["s"]}, {p["total"]});\n'
    s += 'printf("%d", total);\n}\n'
    self.filehandle.write(s)

  # Visit a parse tree produced by d19Parser#part.
  def visitPart(self, ctx: d19Parser.PartContext):
    part = {'x': int(ctx.xval.text), 'm': int(ctx.mval.text), 'a': int(ctx.aval.text), 's': int(ctx.sval.text)}
    part['total'] = part['x'] + part['m'] + part['a'] + part['s']
    self.parts.append(part)

  # Visit a parse tree produced by d19Parser#rule.
  def visitRule(self, ctx: d19Parser.RuleContext):
    self.filehandle.write(f'int fn_{ctx.name.text}(int x, int m, int a, int s, int total) ' + '\n{\n')
    self.visitChildren(ctx)
    self.filehandle.write('}\n\n')

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
    s = f'if ({ctx.attribute.text} {ctx.op.text} {ctx.rval.text}) \n    '
    if val == 'R':
      s += 'return 0;\n'
    elif val == 'A':
      s += 'return total;\n'
    else:
      s += f'return fn_{val}(x, m, a, s, total);\n'
    self.filehandle.write(s)

  # Visit a parse tree produced by d19Parser#token.
  def visitToken(self, ctx: d19Parser.TokenContext):
    return self.visitChildren(ctx)

  def visitToken_clause(self, ctx: d19Parser.Token_clauseContext):
    val = ctx.getChild(0).getText()
    s = ''
    if val == 'R':
      s += 'return 0;\n'
    elif val == 'A':
      s += 'return total;\n'
    else:
      s += f'return fn_{val}(x, m, a, s, total);\n'
    self.filehandle.write(s)
