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


def check_constant_outcome(workflows: dict):
  # if a workflow can only end in one outcome, it can be deleted,
  # and all references to it can be replaced with that outcome, disregarding any of the comparisons along the way.
  can_be_removed = dict()
  for name, instructions in workflows.items():
    outcome = None
    for i in instructions:
      if outcome is None:
        if i[0] in 'AR':
          outcome = i[0]
        elif i[0] == 'cmp':
          outcome = i[4]
        elif i[0] == 'call':
          outcome = i[1]
      else:
        if i[0] in 'AR' and i[0] != outcome or \
            i[0] == 'cmp' and i[4] != outcome or \
            i[0] == 'call' and i[1] != outcome:
          pass
        else:
          can_be_removed[name] = outcome

  return can_be_removed


def solve(workflows: dict):
  answer = 0

  # step 1: remove unnecessary workflows
  can_be_removed = check_constant_outcome(workflows)
  while can_be_removed:
    for rm_name, new_op in can_be_removed.items():
      del workflows[rm_name]
      for name, instructions in workflows.items():
        for i in instructions:
          if i[0] == 'cmp' and i[4] == rm_name:
            i[4] = new_op
          elif i[0] == 'call' and i[1] == rm_name:
            i[0] = new_op
            del i[1]

    can_be_removed = check_constant_outcome(workflows)

  return answer


class d19_VisitorInterpP2(d19Visitor):
  def __init__(self):
    self.root = None
    self.workflows = dict()
    self.current_workflow = []
    self.answer = None

  # Visit a parse tree produced by d19Parser#start.
  def visitStart(self, ctx: d19Parser.StartContext):
    self.visitChildren(ctx)
    self.answer = solve(self.workflows)

  # Visit a parse tree produced by d19Parser#rule.
  def visitRule(self, ctx: d19Parser.RuleContext):
    self.current_workflow = []
    # workflow_steps = []
    # for i in range(ctx.getChildCount()):
    #   workflow_steps.append(self.visit(ctx.getChild(i)))
    self.workflows[ctx.name.text] = self.current_workflow
    return self.visitChildren(ctx)

  # Visit a parse tree produced by d19Parser#clause_list.
  def visitClause_list(self, ctx: d19Parser.Clause_listContext):
    return self.visitChildren(ctx)

  # Visit a parse tree produced by d19Parser#clause.
  def visitClause(self, ctx: d19Parser.ClauseContext):
    return self.visitChildren(ctx)

  # Visit a parse tree produced by d19Parser#comparison.
  def visitComparison(self, ctx: d19Parser.ComparisonContext):
    val = ctx.val.getChild(0).getText()
    self.current_workflow.append(["cmp", ctx.attribute.text, ctx.op.text, int(ctx.rval.text), val])
    self.visitChildren(ctx)

  # Visit a parse tree produced by d19Parser#token.
  def visitToken(self, ctx: d19Parser.TokenContext):
    return self.visitChildren(ctx)

  def visitToken_clause(self, ctx: d19Parser.Token_clauseContext):
    token = ctx.getChild(0).getText()
    if token in 'AR':
      self.current_workflow.append([token])
    else:
      self.current_workflow.append(["call", token])

    return self.visitChildren(ctx)
