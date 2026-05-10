"""
Test cases for TyC code generation.
"""

from src.utils.nodes import *
from tests.utils import CodeGenerator


def test_001():
    """Test 1: Hello World - print string"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printString", [StringLiteral("Hello World")]))
            ])
        )
    ])
    expected = "Hello World"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_002():
    """Test 2: Print integer"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [IntLiteral(42)]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_003():
    """Test 3: Print float"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printFloat", [FloatLiteral(3.14)]))
            ])
        )
    ])
    expected = "3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_004():
    """Test 4: Variable declaration and assignment"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(10)),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_005():
    """Test 5: Binary operation - addition"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(IntLiteral(5), "+", IntLiteral(3))
                ]))
            ])
        )
    ])
    expected = "8"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_006():
    """Test 6: Binary operation - multiplication"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(IntLiteral(6), "*", IntLiteral(7))
                ]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_007():
    """Test 7: If statement"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(IntLiteral(1), "<", IntLiteral(2)),
                    ExprStmt(FuncCall("printString", [StringLiteral("yes")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("no")]))
                )
            ])
        )
    ])
    expected = "yes"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_008():
    """Test 8: While loop"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")])),
                        ExprStmt(AssignExpr(
                            Identifier("i"),
                            BinaryOp(Identifier("i"), "+", IntLiteral(1))
                        ))
                    ])
                )
            ])
        )
    ])
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_009():
    """Test 9: Function call with return value"""
    ast = Program([
        FuncDecl(
            IntType(),
            "add",
            [Param(IntType(), "a"), Param(IntType(), "b")],
            BlockStmt([
                ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    FuncCall("add", [IntLiteral(20), IntLiteral(22)])
                ]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_010():
    """Test 10: Multiple statements - arithmetic operations"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(10)),
                VarDecl(IntType(), "y", IntLiteral(20)),
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(Identifier("x"), "+", Identifier("y"))
                ]))
            ])
        )
    ])
    expected = "30"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


# =====================================================================
# Helpers shared by the 100 student-authored tests below
# =====================================================================

def _main_with(stmts):
    return Program([FuncDecl(VoidType(), "main", [], BlockStmt(stmts))])

def _print_int(expr):
    return ExprStmt(FuncCall("printInt", [expr]))

def _print_float(expr):
    return ExprStmt(FuncCall("printFloat", [expr]))

def _print_str(s):
    return ExprStmt(FuncCall("printString", [StringLiteral(s)]))

def _run(ast, expected):
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


# ---------- Literals & variable declarations (011-022) ----------

def test_011():
    _run(_main_with([_print_int(IntLiteral(0))]), "0")

def test_012():
    _run(_main_with([_print_int(IntLiteral(-1))]), "-1")

def test_013():
    _run(_main_with([_print_int(IntLiteral(127))]), "127")

def test_014():
    _run(_main_with([_print_int(IntLiteral(32000))]), "32000")

def test_015():
    _run(_main_with([_print_int(IntLiteral(123456))]), "123456")

def test_016():
    _run(_main_with([_print_float(FloatLiteral(0.0))]), "0.0")

def test_017():
    _run(_main_with([_print_float(FloatLiteral(1.0))]), "1.0")

def test_018():
    _run(_main_with([_print_float(FloatLiteral(2.5))]), "2.5")

def test_019():
    _run(_main_with([_print_str("hi")]), "hi")

def test_020():
    _run(_main_with([
        VarDecl(IntType(), "x", IntLiteral(7)),
        _print_int(Identifier("x")),
    ]), "7")

def test_021():
    _run(_main_with([
        VarDecl(None, "x", IntLiteral(9)),
        _print_int(Identifier("x")),
    ]), "9")

def test_022():
    _run(_main_with([
        VarDecl(StringType(), "s", StringLiteral("hello")),
        ExprStmt(FuncCall("printString", [Identifier("s")])),
    ]), "hello")


# ---------- Arithmetic (023-034) ----------

def test_023():
    _run(_main_with([_print_int(BinaryOp(IntLiteral(10), "-", IntLiteral(4)))]), "6")

def test_024():
    _run(_main_with([_print_int(BinaryOp(IntLiteral(20), "/", IntLiteral(3)))]), "6")

def test_025():
    _run(_main_with([_print_int(BinaryOp(IntLiteral(20), "%", IntLiteral(3)))]), "2")

def test_026():
    _run(_main_with([_print_int(BinaryOp(IntLiteral(-5), "+", IntLiteral(8)))]), "3")

def test_027():
    _run(_main_with([_print_int(BinaryOp(IntLiteral(100), "*", IntLiteral(0)))]), "0")

def test_028():
    _run(_main_with([_print_int(
        BinaryOp(BinaryOp(IntLiteral(2), "+", IntLiteral(3)), "*", IntLiteral(4))
    )]), "20")

def test_029():
    _run(_main_with([_print_int(BinaryOp(IntLiteral(1000), "+", IntLiteral(234)))]), "1234")

def test_030():
    _run(_main_with([_print_int(BinaryOp(IntLiteral(40000), "-", IntLiteral(7950)))]), "32050")

def test_031():
    _run(_main_with([_print_float(BinaryOp(FloatLiteral(1.5), "+", FloatLiteral(2.5)))]), "4.0")

def test_032():
    _run(_main_with([_print_float(BinaryOp(FloatLiteral(6.0), "/", FloatLiteral(2.0)))]), "3.0")

def test_033():
    _run(_main_with([_print_float(BinaryOp(FloatLiteral(2.5), "*", FloatLiteral(4.0)))]), "10.0")

def test_034():
    _run(_main_with([_print_int(BinaryOp(IntLiteral(50), "-", IntLiteral(50)))]), "0")


# ---------- Relational ops (035-046) ----------

def _print_bool(expr):
    return _print_int(expr)

def test_035():
    _run(_main_with([_print_bool(BinaryOp(IntLiteral(3), "<", IntLiteral(5)))]), "1")

def test_036():
    _run(_main_with([_print_bool(BinaryOp(IntLiteral(5), "<", IntLiteral(3)))]), "0")

def test_037():
    _run(_main_with([_print_bool(BinaryOp(IntLiteral(4), "<=", IntLiteral(4)))]), "1")

def test_038():
    _run(_main_with([_print_bool(BinaryOp(IntLiteral(7), ">", IntLiteral(2)))]), "1")

def test_039():
    _run(_main_with([_print_bool(BinaryOp(IntLiteral(2), ">=", IntLiteral(7)))]), "0")

def test_040():
    _run(_main_with([_print_bool(BinaryOp(IntLiteral(9), "==", IntLiteral(9)))]), "1")

def test_041():
    _run(_main_with([_print_bool(BinaryOp(IntLiteral(9), "==", IntLiteral(10)))]), "0")

def test_042():
    _run(_main_with([_print_bool(BinaryOp(IntLiteral(1), "!=", IntLiteral(2)))]), "1")

def test_043():
    _run(_main_with([_print_bool(BinaryOp(FloatLiteral(1.5), "<", FloatLiteral(2.0)))]), "1")

def test_044():
    _run(_main_with([_print_bool(BinaryOp(FloatLiteral(2.5), ">=", FloatLiteral(2.5)))]), "1")

def test_045():
    _run(_main_with([_print_bool(BinaryOp(FloatLiteral(1.0), "==", FloatLiteral(1.0)))]), "1")

def test_046():
    _run(_main_with([_print_bool(BinaryOp(FloatLiteral(1.0), "!=", FloatLiteral(2.0)))]), "1")


# ---------- if / if-else / nested if (047-058) ----------

def test_047():
    _run(_main_with([
        IfStmt(BinaryOp(IntLiteral(1), "==", IntLiteral(1)), _print_str("yes"))
    ]), "yes")

def test_048():
    _run(_main_with([
        IfStmt(BinaryOp(IntLiteral(1), "==", IntLiteral(2)), _print_str("yes"))
    ]), "")

def test_049():
    _run(_main_with([
        IfStmt(BinaryOp(IntLiteral(3), ">", IntLiteral(2)),
               _print_str("hi"),
               _print_str("lo"))
    ]), "hi")

def test_050():
    _run(_main_with([
        IfStmt(BinaryOp(IntLiteral(3), "<", IntLiteral(2)),
               _print_str("hi"),
               _print_str("lo"))
    ]), "lo")

def test_051():
    _run(_main_with([
        VarDecl(IntType(), "x", IntLiteral(10)),
        IfStmt(BinaryOp(Identifier("x"), ">", IntLiteral(5)),
               _print_int(IntLiteral(1)),
               _print_int(IntLiteral(0)))
    ]), "1")

def test_052():
    _run(_main_with([
        IfStmt(BinaryOp(IntLiteral(1), "==", IntLiteral(1)),
               BlockStmt([_print_str("a"), _print_str("b")]))
    ]), "ab")

def test_053():
    _run(_main_with([
        IfStmt(BinaryOp(IntLiteral(1), "==", IntLiteral(1)),
               IfStmt(BinaryOp(IntLiteral(2), "==", IntLiteral(2)),
                      _print_str("nested"),
                      _print_str("else")))
    ]), "nested")

def test_054():
    _run(_main_with([
        IfStmt(BinaryOp(IntLiteral(1), "==", IntLiteral(2)),
               _print_str("then"),
               IfStmt(BinaryOp(IntLiteral(2), "==", IntLiteral(2)),
                      _print_str("inner-then"),
                      _print_str("inner-else")))
    ]), "inner-then")

def test_055():
    _run(_main_with([
        VarDecl(IntType(), "x", IntLiteral(0)),
        IfStmt(BinaryOp(Identifier("x"), "==", IntLiteral(0)),
               ExprStmt(AssignExpr(Identifier("x"), IntLiteral(42)))),
        _print_int(Identifier("x")),
    ]), "42")

def test_056():
    _run(_main_with([
        IfStmt(BinaryOp(FloatLiteral(3.0), ">", FloatLiteral(2.0)),
               _print_str("ok"))
    ]), "ok")

def test_057():
    _run(_main_with([
        VarDecl(IntType(), "n", IntLiteral(15)),
        IfStmt(BinaryOp(BinaryOp(Identifier("n"), "%", IntLiteral(2)), "==", IntLiteral(0)),
               _print_str("even"),
               _print_str("odd"))
    ]), "odd")

def test_058():
    _run(_main_with([
        VarDecl(IntType(), "x", IntLiteral(5)),
        IfStmt(BinaryOp(Identifier("x"), ">", IntLiteral(0)),
               BlockStmt([
                   _print_str("p"),
                   IfStmt(BinaryOp(Identifier("x"), ">", IntLiteral(10)),
                          _print_str("big"),
                          _print_str("small"))
               ]))
    ]), "psmall")


# ---------- while loops (059-070) ----------

def _while_count_to(n):
    return _main_with([
        VarDecl(IntType(), "i", IntLiteral(0)),
        WhileStmt(
            BinaryOp(Identifier("i"), "<", IntLiteral(n)),
            BlockStmt([
                _print_int(Identifier("i")),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"), "+", IntLiteral(1))))
            ])
        )
    ])

def test_059():
    _run(_while_count_to(1), "0")

def test_060():
    _run(_while_count_to(5), "01234")

def test_061():
    _run(_while_count_to(0), "")

def test_062():
    # sum 1..5 = 15
    _run(_main_with([
        VarDecl(IntType(), "i", IntLiteral(1)),
        VarDecl(IntType(), "s", IntLiteral(0)),
        WhileStmt(
            BinaryOp(Identifier("i"), "<=", IntLiteral(5)),
            BlockStmt([
                ExprStmt(AssignExpr(Identifier("s"),
                    BinaryOp(Identifier("s"), "+", Identifier("i")))),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"), "+", IntLiteral(1)))),
            ])
        ),
        _print_int(Identifier("s"))
    ]), "15")

def test_063():
    # factorial of 5
    _run(_main_with([
        VarDecl(IntType(), "i", IntLiteral(1)),
        VarDecl(IntType(), "f", IntLiteral(1)),
        WhileStmt(
            BinaryOp(Identifier("i"), "<=", IntLiteral(5)),
            BlockStmt([
                ExprStmt(AssignExpr(Identifier("f"),
                    BinaryOp(Identifier("f"), "*", Identifier("i")))),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"), "+", IntLiteral(1)))),
            ])
        ),
        _print_int(Identifier("f"))
    ]), "120")

def test_064():
    # countdown
    _run(_main_with([
        VarDecl(IntType(), "i", IntLiteral(3)),
        WhileStmt(
            BinaryOp(Identifier("i"), ">", IntLiteral(0)),
            BlockStmt([
                _print_int(Identifier("i")),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"), "-", IntLiteral(1))))
            ])
        )
    ]), "321")

def test_065():
    # nested while
    _run(_main_with([
        VarDecl(IntType(), "i", IntLiteral(0)),
        WhileStmt(
            BinaryOp(Identifier("i"), "<", IntLiteral(2)),
            BlockStmt([
                VarDecl(IntType(), "j", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("j"), "<", IntLiteral(2)),
                    BlockStmt([
                        _print_int(Identifier("j")),
                        ExprStmt(AssignExpr(Identifier("j"),
                            BinaryOp(Identifier("j"), "+", IntLiteral(1))))
                    ])
                ),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"), "+", IntLiteral(1))))
            ])
        )
    ]), "0101")

def test_066():
    # while with no iteration prints nothing
    _run(_main_with([
        VarDecl(IntType(), "i", IntLiteral(10)),
        WhileStmt(
            BinaryOp(Identifier("i"), "<", IntLiteral(5)),
            _print_str("never")
        ),
        _print_str("done")
    ]), "done")

def test_067():
    # double-step counter
    _run(_main_with([
        VarDecl(IntType(), "i", IntLiteral(0)),
        WhileStmt(
            BinaryOp(Identifier("i"), "<", IntLiteral(10)),
            BlockStmt([
                _print_int(Identifier("i")),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"), "+", IntLiteral(2))))
            ])
        )
    ]), "02468")

def test_068():
    # sum 1..10
    _run(_main_with([
        VarDecl(IntType(), "i", IntLiteral(1)),
        VarDecl(IntType(), "s", IntLiteral(0)),
        WhileStmt(
            BinaryOp(Identifier("i"), "<=", IntLiteral(10)),
            BlockStmt([
                ExprStmt(AssignExpr(Identifier("s"),
                    BinaryOp(Identifier("s"), "+", Identifier("i")))),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"), "+", IntLiteral(1)))),
            ])
        ),
        _print_int(Identifier("s"))
    ]), "55")

def test_069():
    # find first multiple of 7 >= 50
    _run(_main_with([
        VarDecl(IntType(), "x", IntLiteral(50)),
        WhileStmt(
            BinaryOp(BinaryOp(Identifier("x"), "%", IntLiteral(7)), "!=", IntLiteral(0)),
            ExprStmt(AssignExpr(Identifier("x"),
                BinaryOp(Identifier("x"), "+", IntLiteral(1))))
        ),
        _print_int(Identifier("x"))
    ]), "56")

def test_070():
    # power of 2: 2^10
    _run(_main_with([
        VarDecl(IntType(), "n", IntLiteral(10)),
        VarDecl(IntType(), "p", IntLiteral(1)),
        WhileStmt(
            BinaryOp(Identifier("n"), ">", IntLiteral(0)),
            BlockStmt([
                ExprStmt(AssignExpr(Identifier("p"),
                    BinaryOp(Identifier("p"), "*", IntLiteral(2)))),
                ExprStmt(AssignExpr(Identifier("n"),
                    BinaryOp(Identifier("n"), "-", IntLiteral(1)))),
            ])
        ),
        _print_int(Identifier("p"))
    ]), "1024")


# ---------- for loops, break, continue (071-082) ----------

def test_071():
    _run(_main_with([
        ForStmt(
            VarDecl(IntType(), "i", IntLiteral(0)),
            BinaryOp(Identifier("i"), "<", IntLiteral(3)),
            AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
            _print_int(Identifier("i"))
        )
    ]), "012")

def test_072():
    # for with empty body block
    _run(_main_with([
        VarDecl(IntType(), "s", IntLiteral(0)),
        ForStmt(
            VarDecl(IntType(), "i", IntLiteral(1)),
            BinaryOp(Identifier("i"), "<=", IntLiteral(4)),
            AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
            ExprStmt(AssignExpr(Identifier("s"),
                BinaryOp(Identifier("s"), "+", Identifier("i"))))
        ),
        _print_int(Identifier("s"))
    ]), "10")

def test_073():
    # break exits early
    _run(_main_with([
        ForStmt(
            VarDecl(IntType(), "i", IntLiteral(0)),
            BinaryOp(Identifier("i"), "<", IntLiteral(10)),
            AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
            BlockStmt([
                IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(3)),
                       BreakStmt()),
                _print_int(Identifier("i"))
            ])
        )
    ]), "012")

def test_074():
    # continue skips even numbers
    _run(_main_with([
        ForStmt(
            VarDecl(IntType(), "i", IntLiteral(0)),
            BinaryOp(Identifier("i"), "<", IntLiteral(6)),
            AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
            BlockStmt([
                IfStmt(BinaryOp(BinaryOp(Identifier("i"), "%", IntLiteral(2)), "==", IntLiteral(0)),
                       ContinueStmt()),
                _print_int(Identifier("i"))
            ])
        )
    ]), "135")

def test_075():
    # nested for: 3x3 grid sum
    _run(_main_with([
        VarDecl(IntType(), "s", IntLiteral(0)),
        ForStmt(
            VarDecl(IntType(), "i", IntLiteral(0)),
            BinaryOp(Identifier("i"), "<", IntLiteral(3)),
            AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
            ForStmt(
                VarDecl(IntType(), "j", IntLiteral(0)),
                BinaryOp(Identifier("j"), "<", IntLiteral(3)),
                AssignExpr(Identifier("j"), BinaryOp(Identifier("j"), "+", IntLiteral(1))),
                ExprStmt(AssignExpr(Identifier("s"),
                    BinaryOp(Identifier("s"), "+", IntLiteral(1))))
            )
        ),
        _print_int(Identifier("s"))
    ]), "9")

def test_076():
    # for prints sequence 5..9
    _run(_main_with([
        ForStmt(
            VarDecl(IntType(), "k", IntLiteral(5)),
            BinaryOp(Identifier("k"), "<", IntLiteral(10)),
            AssignExpr(Identifier("k"), BinaryOp(Identifier("k"), "+", IntLiteral(1))),
            _print_int(Identifier("k"))
        )
    ]), "56789")

def test_077():
    # for with no init
    _run(_main_with([
        VarDecl(IntType(), "i", IntLiteral(10)),
        ForStmt(
            None,
            BinaryOp(Identifier("i"), "<", IntLiteral(13)),
            AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
            _print_int(Identifier("i"))
        )
    ]), "101112")

def test_078():
    # break out of nested for inner loop only
    _run(_main_with([
        ForStmt(
            VarDecl(IntType(), "i", IntLiteral(0)),
            BinaryOp(Identifier("i"), "<", IntLiteral(2)),
            AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
            BlockStmt([
                ForStmt(
                    VarDecl(IntType(), "j", IntLiteral(0)),
                    BinaryOp(Identifier("j"), "<", IntLiteral(5)),
                    AssignExpr(Identifier("j"), BinaryOp(Identifier("j"), "+", IntLiteral(1))),
                    BlockStmt([
                        IfStmt(BinaryOp(Identifier("j"), "==", IntLiteral(2)),
                               BreakStmt()),
                        _print_int(Identifier("j"))
                    ])
                ),
                _print_str("|")
            ])
        )
    ]), "01|01|")

def test_079():
    # countdown for
    _run(_main_with([
        ForStmt(
            VarDecl(IntType(), "i", IntLiteral(3)),
            BinaryOp(Identifier("i"), ">", IntLiteral(0)),
            AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "-", IntLiteral(1))),
            _print_int(Identifier("i"))
        )
    ]), "321")

def test_080():
    # accumulate squares 1..4
    _run(_main_with([
        VarDecl(IntType(), "s", IntLiteral(0)),
        ForStmt(
            VarDecl(IntType(), "i", IntLiteral(1)),
            BinaryOp(Identifier("i"), "<=", IntLiteral(4)),
            AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
            ExprStmt(AssignExpr(Identifier("s"),
                BinaryOp(Identifier("s"),
                         "+",
                         BinaryOp(Identifier("i"), "*", Identifier("i")))))
        ),
        _print_int(Identifier("s"))
    ]), "30")

def test_081():
    # break immediately
    _run(_main_with([
        ForStmt(
            VarDecl(IntType(), "i", IntLiteral(0)),
            BinaryOp(Identifier("i"), "<", IntLiteral(5)),
            AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
            BreakStmt()
        ),
        _print_str("done")
    ]), "done")

def test_082():
    # continue every iteration prints nothing
    _run(_main_with([
        ForStmt(
            VarDecl(IntType(), "i", IntLiteral(0)),
            BinaryOp(Identifier("i"), "<", IntLiteral(3)),
            AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
            BlockStmt([ContinueStmt(), _print_int(Identifier("i"))])
        ),
        _print_str("end")
    ]), "end")


# ---------- switch (083-092) ----------

def _sw(value, cases, default=None):
    """Build switch around variable x = value."""
    return _main_with([
        VarDecl(IntType(), "x", IntLiteral(value)),
        SwitchStmt(Identifier("x"), cases, default)
    ])

def test_083():
    # match first case
    _run(_sw(1, [
        CaseStmt(IntLiteral(1), [_print_str("one"), BreakStmt()]),
        CaseStmt(IntLiteral(2), [_print_str("two"), BreakStmt()]),
    ]), "one")

def test_084():
    # match second case
    _run(_sw(2, [
        CaseStmt(IntLiteral(1), [_print_str("one"), BreakStmt()]),
        CaseStmt(IntLiteral(2), [_print_str("two"), BreakStmt()]),
    ]), "two")

def test_085():
    # default executes when no match
    _run(_sw(9, [
        CaseStmt(IntLiteral(1), [_print_str("one"), BreakStmt()]),
    ], DefaultStmt([_print_str("other")])), "other")

def test_086():
    # fall-through: no break in case 1, falls into 2
    _run(_sw(1, [
        CaseStmt(IntLiteral(1), [_print_str("a")]),
        CaseStmt(IntLiteral(2), [_print_str("b"), BreakStmt()]),
        CaseStmt(IntLiteral(3), [_print_str("c"), BreakStmt()]),
    ]), "ab")

def test_087():
    # fall-through cascades through cases until break
    _run(_sw(1, [
        CaseStmt(IntLiteral(1), [_print_str("a")]),
        CaseStmt(IntLiteral(2), [_print_str("b")]),
        CaseStmt(IntLiteral(3), [_print_str("c"), BreakStmt()]),
        CaseStmt(IntLiteral(4), [_print_str("d"), BreakStmt()]),
    ]), "abc")

def test_088():
    # default-only switch
    _run(_main_with([
        VarDecl(IntType(), "x", IntLiteral(7)),
        SwitchStmt(Identifier("x"), [], DefaultStmt([_print_str("def")]))
    ]), "def")

def test_089():
    # default matches when value not handled
    _run(_sw(99, [
        CaseStmt(IntLiteral(1), [_print_str("one"), BreakStmt()]),
        CaseStmt(IntLiteral(2), [_print_str("two"), BreakStmt()]),
    ], DefaultStmt([_print_str("none")])), "none")

def test_090():
    # statement after switch executes
    ast = _main_with([
        VarDecl(IntType(), "x", IntLiteral(2)),
        SwitchStmt(Identifier("x"), [
            CaseStmt(IntLiteral(2), [_print_str("hit"), BreakStmt()]),
        ], None),
        _print_str("after"),
    ])
    _run(ast, "hitafter")

def test_091():
    # switch on computed expression
    _run(_main_with([
        SwitchStmt(BinaryOp(IntLiteral(2), "+", IntLiteral(1)), [
            CaseStmt(IntLiteral(3), [_print_str("three"), BreakStmt()]),
            CaseStmt(IntLiteral(4), [_print_str("four"), BreakStmt()]),
        ], None)
    ]), "three")

def test_092():
    # switch with no default and no match prints nothing
    _run(_main_with([
        VarDecl(IntType(), "x", IntLiteral(50)),
        SwitchStmt(Identifier("x"), [
            CaseStmt(IntLiteral(1), [_print_str("a"), BreakStmt()]),
        ], None),
        _print_str("end")
    ]), "end")


# ---------- Unary operators (093-100) ----------

def test_093():
    _run(_main_with([_print_int(PrefixOp("-", IntLiteral(7)))]), "-7")

def test_094():
    _run(_main_with([_print_int(PrefixOp("+", IntLiteral(8)))]), "8")

def test_095():
    _run(_main_with([_print_int(PrefixOp("!", IntLiteral(0)))]), "1")

def test_096():
    _run(_main_with([_print_int(PrefixOp("!", IntLiteral(5)))]), "0")

def test_097():
    # prefix ++ returns new value
    _run(_main_with([
        VarDecl(IntType(), "x", IntLiteral(4)),
        _print_int(PrefixOp("++", Identifier("x"))),
        _print_str(":"),
        _print_int(Identifier("x")),
    ]), "5:5")

def test_098():
    # prefix -- returns new value
    _run(_main_with([
        VarDecl(IntType(), "x", IntLiteral(4)),
        _print_int(PrefixOp("--", Identifier("x"))),
        _print_str(":"),
        _print_int(Identifier("x")),
    ]), "3:3")

def test_099():
    # postfix ++ returns old value, var becomes new
    _run(_main_with([
        VarDecl(IntType(), "x", IntLiteral(4)),
        _print_int(PostfixOp("++", Identifier("x"))),
        _print_str(":"),
        _print_int(Identifier("x")),
    ]), "4:5")

def test_100():
    # postfix -- returns old value, var becomes new
    _run(_main_with([
        VarDecl(IntType(), "x", IntLiteral(4)),
        _print_int(PostfixOp("--", Identifier("x"))),
        _print_str(":"),
        _print_int(Identifier("x")),
    ]), "4:3")


# ---------- Function calls (101-112) ----------

def test_101():
    # void function called from main
    ast = Program([
        FuncDecl(VoidType(), "greet", [], BlockStmt([_print_str("hi")])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("greet", []))
        ]))
    ])
    _run(ast, "hi")

def test_102():
    # int return
    ast = Program([
        FuncDecl(IntType(), "five", [], BlockStmt([ReturnStmt(IntLiteral(5))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            _print_int(FuncCall("five", []))
        ]))
    ])
    _run(ast, "5")

def test_103():
    # float return
    ast = Program([
        FuncDecl(FloatType(), "pi", [], BlockStmt([ReturnStmt(FloatLiteral(3.0))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            _print_float(FuncCall("pi", []))
        ]))
    ])
    _run(ast, "3.0")

def test_104():
    # string return
    ast = Program([
        FuncDecl(StringType(), "name", [], BlockStmt([ReturnStmt(StringLiteral("Tyc"))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printString", [FuncCall("name", [])]))
        ]))
    ])
    _run(ast, "Tyc")

def test_105():
    # multi-arg
    ast = Program([
        FuncDecl(IntType(), "sub",
                 [Param(IntType(), "a"), Param(IntType(), "b")],
                 BlockStmt([ReturnStmt(BinaryOp(Identifier("a"), "-", Identifier("b")))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            _print_int(FuncCall("sub", [IntLiteral(10), IntLiteral(3)]))
        ]))
    ])
    _run(ast, "7")

def test_106():
    # recursion: factorial (single-return pattern so verifier is happy)
    ast = Program([
        FuncDecl(IntType(), "fact", [Param(IntType(), "n")], BlockStmt([
            VarDecl(IntType(), "r", IntLiteral(1)),
            IfStmt(BinaryOp(Identifier("n"), ">", IntLiteral(1)),
                   ExprStmt(AssignExpr(Identifier("r"),
                       BinaryOp(Identifier("n"), "*",
                           FuncCall("fact", [BinaryOp(Identifier("n"), "-", IntLiteral(1))]))))),
            ReturnStmt(Identifier("r"))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            _print_int(FuncCall("fact", [IntLiteral(6)]))
        ]))
    ])
    _run(ast, "720")

def test_107():
    # recursion: fibonacci (single-return pattern)
    ast = Program([
        FuncDecl(IntType(), "fib", [Param(IntType(), "n")], BlockStmt([
            VarDecl(IntType(), "r", Identifier("n")),
            IfStmt(BinaryOp(Identifier("n"), ">=", IntLiteral(2)),
                   ExprStmt(AssignExpr(Identifier("r"),
                       BinaryOp(
                           FuncCall("fib", [BinaryOp(Identifier("n"), "-", IntLiteral(1))]),
                           "+",
                           FuncCall("fib", [BinaryOp(Identifier("n"), "-", IntLiteral(2))])
                       )))),
            ReturnStmt(Identifier("r"))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            _print_int(FuncCall("fib", [IntLiteral(8)]))
        ]))
    ])
    _run(ast, "21")

def test_108():
    # passes float param
    ast = Program([
        FuncDecl(FloatType(), "double",
                 [Param(FloatType(), "x")],
                 BlockStmt([ReturnStmt(BinaryOp(Identifier("x"), "*", FloatLiteral(2.0)))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            _print_float(FuncCall("double", [FloatLiteral(2.5)]))
        ]))
    ])
    _run(ast, "5.0")

def test_109():
    # void function with side effect via printInt
    ast = Program([
        FuncDecl(VoidType(), "show", [Param(IntType(), "v")], BlockStmt([
            _print_int(Identifier("v")),
            _print_str("!"),
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("show", [IntLiteral(7)])),
            ExprStmt(FuncCall("show", [IntLiteral(8)])),
        ]))
    ])
    _run(ast, "7!8!")

def test_110():
    # mutual call chain (single-return pattern)
    ast = Program([
        FuncDecl(IntType(), "is_even", [Param(IntType(), "n")], BlockStmt([
            VarDecl(IntType(), "r", IntLiteral(1)),
            IfStmt(BinaryOp(Identifier("n"), "!=", IntLiteral(0)),
                   ExprStmt(AssignExpr(Identifier("r"),
                       FuncCall("is_odd",
                           [BinaryOp(Identifier("n"), "-", IntLiteral(1))])))),
            ReturnStmt(Identifier("r"))
        ])),
        FuncDecl(IntType(), "is_odd", [Param(IntType(), "n")], BlockStmt([
            VarDecl(IntType(), "r", IntLiteral(0)),
            IfStmt(BinaryOp(Identifier("n"), "!=", IntLiteral(0)),
                   ExprStmt(AssignExpr(Identifier("r"),
                       FuncCall("is_even",
                           [BinaryOp(Identifier("n"), "-", IntLiteral(1))])))),
            ReturnStmt(Identifier("r"))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            _print_int(FuncCall("is_even", [IntLiteral(6)])),
            _print_int(FuncCall("is_odd", [IntLiteral(6)])),
        ]))
    ])
    _run(ast, "10")


# ---------- Structs (111-116) ----------
# Struct literals must appear in a *typed* VarDecl so visit_var_decl can
# propagate the struct name to visit_struct_literal. Member-LHS assignment
# is unsupported, so tests only read members back via MemberAccess.

def _point_struct():
    return StructDecl("Point", [
        MemberDecl(IntType(), "x"),
        MemberDecl(IntType(), "y"),
    ])

def test_111():
    ast = Program([
        _point_struct(),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Point"), "p",
                    StructLiteral([IntLiteral(3), IntLiteral(4)])),
            _print_int(MemberAccess(Identifier("p"), "x")),
            _print_int(MemberAccess(Identifier("p"), "y")),
        ]))
    ])
    _run(ast, "34")

def test_112():
    ast = Program([
        _point_struct(),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Point"), "p",
                    StructLiteral([IntLiteral(10), IntLiteral(20)])),
            _print_int(BinaryOp(MemberAccess(Identifier("p"), "x"),
                                "+",
                                MemberAccess(Identifier("p"), "y"))),
        ]))
    ])
    _run(ast, "30")

def test_113():
    ast = Program([
        _point_struct(),
        FuncDecl(IntType(), "sum_xy", [Param(StructType("Point"), "p")], BlockStmt([
            ReturnStmt(BinaryOp(MemberAccess(Identifier("p"), "x"),
                                "+",
                                MemberAccess(Identifier("p"), "y")))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Point"), "p",
                    StructLiteral([IntLiteral(7), IntLiteral(8)])),
            _print_int(FuncCall("sum_xy", [Identifier("p")])),
        ]))
    ])
    _run(ast, "15")

def test_114():
    ast = Program([
        _point_struct(),
        StructDecl("Line", [
            MemberDecl(StructType("Point"), "a"),
            MemberDecl(StructType("Point"), "b"),
        ]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Line"), "L",
                    StructLiteral([
                        StructLiteral([IntLiteral(1), IntLiteral(2)]),
                        StructLiteral([IntLiteral(5), IntLiteral(6)]),
                    ])),
            _print_int(MemberAccess(MemberAccess(Identifier("L"), "a"), "x")),
            _print_int(MemberAccess(MemberAccess(Identifier("L"), "b"), "y")),
        ]))
    ])
    _run(ast, "16")

def test_115():
    ast = Program([
        _point_struct(),
        FuncDecl(StructType("Point"), "make", [Param(IntType(), "v")], BlockStmt([
            VarDecl(StructType("Point"), "p",
                    StructLiteral([Identifier("v"), Identifier("v")])),
            ReturnStmt(Identifier("p"))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Point"), "q", FuncCall("make", [IntLiteral(9)])),
            _print_int(MemberAccess(Identifier("q"), "x")),
            _print_int(MemberAccess(Identifier("q"), "y")),
        ]))
    ])
    _run(ast, "99")

def test_116():
    ast = Program([
        StructDecl("A", [MemberDecl(IntType(), "v")]),
        StructDecl("B", [MemberDecl(IntType(), "w")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("A"), "a", StructLiteral([IntLiteral(11)])),
            VarDecl(StructType("B"), "b", StructLiteral([IntLiteral(22)])),
            _print_int(MemberAccess(Identifier("a"), "v")),
            _print_int(MemberAccess(Identifier("b"), "w")),
        ]))
    ])
    _run(ast, "1122")
