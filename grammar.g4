grammar day08;
start : lr=LR '\n'+ nodes+=node+ EOF;
node: base=ID '=' '(' left=ID ',' right=ID ')' '\n'?;


LR : ('L' | 'R')+;
ID: [0-9A-Z][0-9A-Z][0-9A-Z];
WS : [ \r\t]+ -> skip ;
