grammar d19;
start : rules+=rule+ '\n' parts+=part+ EOF;
part: '{x=' xval=INT ',m='  mval=INT ',a='  aval=INT ',s='  sval=INT '}\n' ;

rule : name=ID '{' clauses+=clause_list '}\n';
clause_list: clause (',' clause)*;
clause: comparison | token;
comparison: attribute=('x' | 'm' | 'a' | 's') op=OPERATOR rval=INT ':' val=token ;
token: 'R' | 'A' | ID;

fragment DIGIT: [0-9];
OPERATOR : '<' | '>';
INT : DIGIT+;
ID : [a-z]+;
WS : [ \r\t]+ -> skip ;
