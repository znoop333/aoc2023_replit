import dataclasses
import sys
from antlr4 import *
from gen.d19Lexer import d19Lexer
from gen.d19Parser import d19Parser
from gen.d19Visitor import d19Visitor
from copy import copy
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
          break
    else:
      can_be_removed[name] = outcome

  return can_be_removed


def remove_unnecessary_workflows(workflows: dict):
  n_removed = 0
  can_be_removed = check_constant_outcome(workflows)
  while can_be_removed:
    for rm_name, new_op in can_be_removed.items():
      del workflows[rm_name]
      n_removed += 1
      for name, instructions in workflows.items():
        for i in instructions:
          if i[0] == 'cmp' and i[4] == rm_name:
            i[4] = new_op
          elif i[0] == 'call' and i[1] == rm_name:
            i[0] = new_op
            del i[1]

    can_be_removed = check_constant_outcome(workflows)

  return n_removed


def remove_redundant_if(workflows: dict):
  # example:
  # kxq{x<2775:R,x>2923:A,A}
  # the clause x>2923:A,A  can be replaced with A because the value of X doesn't actually matter
  # pv{x<3403:R,m>1175:A,x<3663:A,A}  -- similar for x<3663:A,A
  n_simplified = 0

  for name, instructions in workflows.items():
    current_instructions = copy(instructions)
    for n in range(len(current_instructions) - 1, 0, -1):
      i = current_instructions[n]
      if i[0] in 'AR' and instructions[n - 1][0] == 'cmp' and instructions[n - 1][4] == i[0]:
        # print(f'Simplifying {name} at {instructions[n - 1]} and {instructions[n]} to {i[0]}')
        instructions[n - 1] = [i[0]]
        del instructions[n]
        n_simplified += 1

  # print(f'{n_simplified} simplifications total')
  return n_simplified


def get_constraints(clause: list):
  if clause[0] != 'cmp':
    return {'val': clause[1]}, {'val': clause[1]}
  if clause[2] == '>':
    constraint_true = {clause[1]: range(clause[3] + 1, 4000), 'val': clause[4]}
    constraint_false = {clause[1]: range(1, clause[3]), 'val': None}
  else:
    constraint_true = {clause[1]: range(1, clause[3] - 1), 'val': clause[4]}
    constraint_false = {clause[1]: range(clause[3], 4000), 'val': None}
  return constraint_true, constraint_false


def intersect_constraints(c1: dict, c2: dict):
  # if there are multiple ways to reach 'A', the output is an OR of ANDs:
  # from 'vjd' : [['cmp', 'm', '>', 3232, 'A'], ['cmp', 'm', '>', 3185, 'A'], ['R']]
  # this should produce two constraints, either of which will work:
  # {'m': range(3233, 4001)}  OR
  # {'m': range(1, 3232) AND range(3186, 4000) } ==> {'m': range(3186, 3231)}
  intersected = {}
  for w in 'xmas':
    if w in c1 and w in c2:
      lb = max(c1[w].start, c2[w].start)
      ub = min(c1[w].stop, c2[w].stop)
      if lb <= ub:
        intersected[w] = range(lb, ub)
      else:
        intersected[w] = None
    elif w in c1:
      intersected[w] = c1[w]
    elif w in c2:
      intersected[w] = c2[w]
  return intersected


def count_valid_solutions(c1: dict):
  # I'm going to abuse the range() by treating the upper bound as inclusive
  # even though python doesn't treat it as such. the main effect is that len(range(1,10))
  # returns 9, but I want to treat it as length 10.
  counted = 1
  for w in 'xmas':
    if w in c1:
      if c1[w] is None:
        return 0
      counted *= len(c1[w]) + 1
    else:
      counted *= 4000
  return counted


def workflow_constraint_solver(wf: dict):
  # convert a workflow from instructions into a set of constraints leading to an 'A'.
  # e.g., from 'cm' : [['cmp', 'm', '<', 151, 'R'], ['cmp', 's', '>', 3876, 'R'], ['A']]
  # should become {'m': range(151, 4000), 's': range(1, 3876)}
  # because the only way to reach 'A' is for the first and second cmps to both be false.
  # from that constraint, the number of valid inputs is the product of the ranges.
  # if there were no conditions in the constraint, the number would be 4000**4

  num_solutions = 0

  queue = deque()
  queue.append(('in', {}))

  while queue:
    wf_name, current_constraints = queue.popleft()
    if wf_name == 'R':
      print(f'Rejecting at {current_constraints}!')
      continue
    elif wf_name == 'A':
      print(f'Accepting at {current_constraints}!')
      num_solutions += count_valid_solutions(current_constraints)
      continue

    clauses = wf[wf_name]
    for clause in clauses:
      if_true, if_false = get_constraints(clause)
      current_constraints1 = intersect_constraints(current_constraints, if_true)
      if not count_valid_solutions(current_constraints1):
        print(f'Impossible to continue with {current_constraints1} from if_true {if_true} and {current_constraints}')
      else:
        if clause[0] == 'cmp':
          queue.append((clause[4], current_constraints1))
        elif clause[0] in 'AR':
          queue.append((clause[0], current_constraints1))
        elif clause[0] == 'call':
          queue.append((clause[1], current_constraints1))

      current_constraints2 = intersect_constraints(current_constraints, if_false)
      if not count_valid_solutions(current_constraints2):
        print(f'Impossible to continue with {current_constraints2} from if_false {if_false} and {current_constraints}')
      else:
        # continue with the next clause under the constraint that the current clause was false
        current_constraints = current_constraints2

  return num_solutions


def solve(workflows: dict):
  answer = 0

  while True:
    # step 1: remove unnecessary workflows
    n_removed = remove_unnecessary_workflows(workflows)
    if n_removed:
      print(f'Removed {n_removed} unnecessary workflows')

    # step 2: simplify redundant conditions
    n_simplified = remove_redundant_if(workflows)
    if n_simplified:
      print(f'Simplified {n_simplified} clauses')

    if not n_removed and not n_simplified:
      break

  answer = workflow_constraint_solver(workflows)

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
