/*
FODTL grammar
Copyright (C) 2016 Walid Benghabrit

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

grammar FODTL;

//-------------------------------------------------------//
//----------------- Lexer rules ------------------------//
//------------------------------------------------------//
O_not    : '~' | 'not';
O_and    : '&';
O_or     : '|';
O_imply  : '->'  | '=>';
true     : 'true';
false    : 'false';

O_always   : 'G';
O_next     : 'X';
O_future   : 'F';
O_until    : 'U';
O_release  : 'R';

ID        : (('a'..'z')|('A'..'Z')) (('a'..'z')|('A'..'Z')| INT | '_')*;
INT       : '0'..'9'+;
NEWLINE   : '\r'?'\n' -> channel(HIDDEN);
WS        : (' '|'\t'|'\n'|'\r')+ -> skip;
BLANK     : (' ')+;
STRING    : ('"' (.)*? '"');
COMMENT   : '%' (.)*? '\n' -> channel(HIDDEN);

H_lpar    : '(';
H_rpar    : ')';
H_lbar    : '[';
H_rbar    : ']';
H_dot     : '.';
H_colon   : ':';
H_equal   : '=';
H_comma   : ',';
H_quote   : '\'';
H_qmark   : '?';
H_emark   : '!';
H_at      : '@';

//-------------------------------------------------------//
//----------------- Parser rules -----------------------//
//------------------------------------------------------//
main    : formula;
formula : true | false //| constant | variable |
        | predicate NEWLINE* | negation NEWLINE*
        | formula NEWLINE* (O_and | O_or | O_imply) NEWLINE* formula NEWLINE*
        | uQuant formula NEWLINE* | eQuant formula NEWLINE*
        | formula btOperators formula NEWLINE* | utOperators formula NEWLINE*
        | H_lpar formula H_rpar NEWLINE*
        | remote;

// Classical logic
predicate   : ID H_lpar (arg (H_comma arg)*)? H_rpar;
arg         : variable | constant | regexp | predicate;
variable    : ID;
constant    : H_quote (ID | INT) H_quote;
regexp      : 'r' STRING;
negation    : O_not formula;

// Temporal operators
utOperators : O_always | O_next | O_future;
btOperators : O_until | O_release;

// First order
vartype : ID;
vardec  : ID H_colon vartype;
uQuant  : H_emark H_lbar vardec+ H_rbar ;
eQuant  : H_qmark H_lbar vardec+ H_rbar;

// Distributed operators
remote   : H_at ID H_lpar formula H_rpar;

