grammar d18;
start : instructions+=dig_instruction+ EOF;
dig_instruction : dir=DIR dist=ID '(#' real_direction=ID ')' '\n';


fragment DIGIT: [0-9];
fragment HEX: [a-f];
ID : (DIGIT | HEX)+;
DIR : 'U' | 'D' | 'L' | 'R';
WS : [ \r\t]+ -> skip ;
