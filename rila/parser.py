from rply import ParserGenerator

import ast


pg = ParserGenerator(
    ["SEMICOLON", "NUMBER", "ADD", "SUB", "MULT", "DIV"],
    precedence=[
        ("left", ["ADD", "SUB"]),
        ("left", ["MULT", "DIV"])
    ]
)


@pg.production("statements : statements statement")
def statements(s):
    return ast.Block(s[0].getastlist() + [s[1]])


@pg.production("statements : statement")
def statements_statement(s):
    return ast.Block([s[0]])


@pg.production("statement : expression SEMICOLON")
def statement_expression(s):
    return ast.Statement(s[0])


@pg.production("expression : NUMBER")
def expression_number(s):
    return ast.Number(int(s[0].getstr()))


@pg.production("expression : expression ADD expression")
@pg.production("expression : expression SUB expression")
@pg.production("expression : expression MULT expression")
@pg.production("expression : expression DIV expression")
def expression_binop(s):
    return ast.BinaryOp(s[1].getstr(), s[0], s[2])


parser = pg.build()