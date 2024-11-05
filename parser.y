%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylex();
extern int yyparse();
extern FILE* yyin;

int yylval;
%}

%token WHILE LPAREN RPAREN LBRACE RBRACE NUMBER IDENTIFIER

%%
program: statement
        | program statement

statement: while_statement
        | expression

while_statement: WHILE LPAREN expression RPAREN LBRACE statement RBRACE {
    printf("LABEL L%d\n", ++label_count);
    printf("IF %s GOTO L%d\n", $3, label_count + 1);
    printf("GOTO L%d\n", ++label_count);
    printf("LABEL L%d\n", label_count - 1);
    printf("%s = %s + 1\n", $3, $3); // Simple increment for demonstration
    printf("GOTO L%d\n", label_count - 2);
    printf("LABEL L%d\n", label_count);
}

expression: IDENTIFIER
        | NUMBER
        | expression '+' expression
        | expression '-' expression
        | expression '*' expression
        | expression '/' expression
        | expression '<' expression
        | expression '>' expression
        | expression "==" expression
        | expression "!=" expression
        | expression "<=" expression
        | expression ">=" expression
        | '(' expression ')'
%%

int label_count = 0;

int main(int argc, char** argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);
        return 1;
    }

    FILE* input_file = fopen(argv[1], "r");
    if (!input_file) {
        perror("Error opening input file");
        return 1;
    }

    yyin = input_file;

    yyparse();

    fclose(input_file);

    return 0;
}
