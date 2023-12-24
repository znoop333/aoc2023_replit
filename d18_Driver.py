import sys
from antlr4 import *
from gen.d18Lexer import d18Lexer
from gen.d18Parser import d18Parser
from d18_VisitorInterp import d18_VisitorInterp


def main(argv):
  input_stream = FileStream('d18_test_input.txt', encoding='utf-8')
  # input_stream = FileStream('d18_input.txt', encoding='utf-8')

  lexer = d18Lexer(input_stream)
  stream = CommonTokenStream(lexer)
  parser = d18Parser(stream)
  tree = parser.start()
  if parser.getNumberOfSyntaxErrors() > 0:
    print("syntax errors")
  else:
    vinterp = d18_VisitorInterp()
    vinterp.visit(tree)
    print(vinterp.answer)
    print(952408144115 - vinterp.answer)


if __name__ == '__main__':
  main(sys.argv)
