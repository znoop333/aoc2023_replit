import sys
from antlr4 import *
from gen.d19Lexer import d19Lexer
from gen.d19Parser import d19Parser
from d19_VisitorInterp import d19_VisitorInterp


def main(argv):
  input_stream = FileStream('d19_test_input.txt', encoding='utf-8')
  # input_stream = FileStream('d19_test_input4.txt', encoding='utf-8')
  # input_stream = FileStream('d19_input.txt', encoding='utf-8')

  lexer = d19Lexer(input_stream)
  stream = CommonTokenStream(lexer)
  parser = d19Parser(stream)
  tree = parser.start()
  if parser.getNumberOfSyntaxErrors() > 0:
    print("syntax errors")
  else:
    with open("d19_src.c", "w") as f:
      vinterp = d19_VisitorInterp(f)
      vinterp.visit(tree)


if __name__ == '__main__':
  main(sys.argv)
