"""
AST Generation test cases for TyC compiler.
"""

import pytest
from tests.utils import ASTGenerator


# ── Helper ────────────────────────────────────────────────────────────
def ast(source: str) -> str:
    return str(ASTGenerator(source).generate())


# ══════════════════════════════════════════════════════════════════════
# 1. Program-level tests
# ══════════════════════════════════════════════════════════════════════

def test_empty_program():
    assert ast("") == "Program([])"


def test_single_void_main():
    assert ast("void main() {}") == "Program([FuncDecl(VoidType(), main, [], [])])"


def test_two_functions():
    src = "void foo() {} void bar() {}"
    assert ast(src) == "Program([FuncDecl(VoidType(), foo, [], []), FuncDecl(VoidType(), bar, [], [])])"


# ══════════════════════════════════════════════════════════════════════
# 2. Struct declarations
# ══════════════════════════════════════════════════════════════════════

def test_empty_struct():
    assert ast("struct Empty {};") == "Program([StructDecl(Empty, [])])"


def test_struct_one_member():
    assert ast("struct S { int x; };") == "Program([StructDecl(S, [MemberDecl(IntType(), x)])])"


def test_struct_multiple_members():
    src = "struct P { int x; float y; string s; };"
    assert ast(src) == "Program([StructDecl(P, [MemberDecl(IntType(), x), MemberDecl(FloatType(), y), MemberDecl(StringType(), s)])])"


def test_struct_with_struct_member():
    src = "struct A { int a; }; struct B { A inner; };"
    assert ast(src) == "Program([StructDecl(A, [MemberDecl(IntType(), a)]), StructDecl(B, [MemberDecl(StructType(A), inner)])])"


def test_struct_and_function():
    src = "struct S { int x; }; void main() {}"
    assert ast(src) == "Program([StructDecl(S, [MemberDecl(IntType(), x)]), FuncDecl(VoidType(), main, [], [])])"


# ══════════════════════════════════════════════════════════════════════
# 3. Function declarations
# ══════════════════════════════════════════════════════════════════════

def test_func_int_return():
    assert ast("int f() {}") == "Program([FuncDecl(IntType(), f, [], [])])"


def test_func_float_return():
    assert ast("float f() {}") == "Program([FuncDecl(FloatType(), f, [], [])])"


def test_func_string_return():
    assert ast("string f() {}") == "Program([FuncDecl(StringType(), f, [], [])])"


def test_func_auto_return():
    """Omitted return type means auto (None)."""
    assert ast("f() {}") == "Program([FuncDecl(auto, f, [], [])])"


def test_func_one_param():
    assert ast("void f(int x) {}") == "Program([FuncDecl(VoidType(), f, [Param(IntType(), x)], [])])"


def test_func_multiple_params():
    src = "void f(int x, float y, string s) {}"
    assert ast(src) == "Program([FuncDecl(VoidType(), f, [Param(IntType(), x), Param(FloatType(), y), Param(StringType(), s)], [])])"


def test_func_struct_param():
    src = "struct P { int x; }; void f(P p) {}"
    result = ast(src)
    assert "Param(StructType(P), p)" in result


def test_func_struct_return():
    src = "struct P { int x; }; P getP() {}"
    result = ast(src)
    assert "FuncDecl(StructType(P), getP, [], [])" in result


# ══════════════════════════════════════════════════════════════════════
# 4. Variable declarations
# ══════════════════════════════════════════════════════════════════════

def test_vardecl_int():
    src = "void main() { int x; }"
    assert "VarDecl(IntType(), x)" in ast(src)


def test_vardecl_float_init():
    src = "void main() { float y = 3.14; }"
    assert "VarDecl(FloatType(), y = FloatLiteral(3.14))" in ast(src)


def test_vardecl_string_init():
    src = 'void main() { string s = "hi"; }'
    assert "VarDecl(StringType(), s = StringLiteral('hi'))" in ast(src)


def test_vardecl_auto_int():
    src = "void main() { auto x = 5; }"
    assert "VarDecl(auto, x = IntLiteral(5))" in ast(src)


def test_vardecl_auto_no_init():
    src = "void main() { auto x; }"
    assert "VarDecl(auto, x)" in ast(src)


def test_vardecl_struct_type():
    src = "struct S { int a; }; void main() { S s; }"
    assert "VarDecl(StructType(S), s)" in ast(src)


def test_vardecl_struct_init():
    src = "struct S { int a; }; void main() { S s = {1}; }"
    result = ast(src)
    assert "VarDecl(StructType(S), s = StructLiteral({IntLiteral(1)}))" in result


# ══════════════════════════════════════════════════════════════════════
# 5. If statements
# ══════════════════════════════════════════════════════════════════════

def test_if_simple():
    src = "void main() { if (1) {} }"
    assert "IfStmt(if IntLiteral(1) then BlockStmt([]))" in ast(src)


def test_if_else():
    src = "void main() { if (1) {} else {} }"
    assert "IfStmt(if IntLiteral(1) then BlockStmt([]), else BlockStmt([]))" in ast(src)


def test_if_nested():
    src = "void main() { if (1) { if (0) {} } }"
    result = ast(src)
    assert "IfStmt(if IntLiteral(1)" in result
    assert "IfStmt(if IntLiteral(0)" in result


# ══════════════════════════════════════════════════════════════════════
# 6. While statements
# ══════════════════════════════════════════════════════════════════════

def test_while_simple():
    src = "void main() { while (1) {} }"
    assert "WhileStmt(while IntLiteral(1) do BlockStmt([]))" in ast(src)


def test_while_with_body():
    src = "void main() { while (1) { break; } }"
    assert "WhileStmt(while IntLiteral(1) do BlockStmt([BreakStmt()]))" in ast(src)


# ══════════════════════════════════════════════════════════════════════
# 7. For statements
# ══════════════════════════════════════════════════════════════════════

def test_for_full():
    src = "void main() { for (int i = 0; i < 10; i++) {} }"
    result = ast(src)
    assert "ForStmt(" in result
    assert "VarDecl(IntType(), i = IntLiteral(0))" in result
    assert "BinaryOp(Identifier(i), <, IntLiteral(10))" in result
    assert "PostfixOp(Identifier(i)++)" in result


def test_for_empty():
    src = "void main() { for (;;) {} }"
    assert "ForStmt(for None; None; None do BlockStmt([]))" in ast(src)


def test_for_auto_init():
    src = "void main() { for (auto i = 0; i < 5; i++) {} }"
    result = ast(src)
    assert "VarDecl(auto, i = IntLiteral(0))" in result


def test_for_expr_init():
    src = "void main() { int i; for (i = 0; i < 5; i++) {} }"
    result = ast(src)
    assert "ExprStmt(AssignExpr(Identifier(i) = IntLiteral(0)))" in result


def test_for_no_update():
    src = "void main() { for (int i = 0; i < 5;) {} }"
    result = ast(src)
    assert "None do BlockStmt([])" in result


# ══════════════════════════════════════════════════════════════════════
# 8. Switch statements
# ══════════════════════════════════════════════════════════════════════

def test_switch_simple():
    src = "void main() { switch (x) { case 1: break; } }"
    result = ast(src)
    assert "SwitchStmt(" in result
    assert "CaseStmt(case IntLiteral(1): [BreakStmt()])" in result


def test_switch_with_default():
    src = "void main() { switch (x) { case 1: break; default: break; } }"
    result = ast(src)
    assert "CaseStmt(case IntLiteral(1): [BreakStmt()])" in result
    assert "default DefaultStmt(default: [BreakStmt()])" in result


def test_switch_multiple_cases():
    src = "void main() { switch (x) { case 1: case 2: break; } }"
    result = ast(src)
    assert "CaseStmt(case IntLiteral(1): [])" in result
    assert "CaseStmt(case IntLiteral(2): [BreakStmt()])" in result


def test_switch_empty():
    src = "void main() { switch (x) {} }"
    result = ast(src)
    assert "SwitchStmt(switch Identifier(x) cases [])" in result


# ══════════════════════════════════════════════════════════════════════
# 9. Break, continue, return
# ══════════════════════════════════════════════════════════════════════

def test_break():
    src = "void main() { while(1) { break; } }"
    assert "BreakStmt()" in ast(src)


def test_continue():
    src = "void main() { while(1) { continue; } }"
    assert "ContinueStmt()" in ast(src)


def test_return_void():
    src = "void main() { return; }"
    assert "ReturnStmt(return)" in ast(src)


def test_return_expr():
    src = "int f() { return 5; }"
    assert "ReturnStmt(return IntLiteral(5))" in ast(src)


def test_return_complex_expr():
    src = "int f(int a, int b) { return a + b; }"
    assert "ReturnStmt(return BinaryOp(Identifier(a), +, Identifier(b)))" in ast(src)


# ══════════════════════════════════════════════════════════════════════
# 10. Expression statements
# ══════════════════════════════════════════════════════════════════════

def test_expr_stmt_func_call():
    src = "void main() { foo(); }"
    assert "ExprStmt(FuncCall(foo, []))" in ast(src)


def test_expr_stmt_assign():
    src = "void main() { int x; x = 5; }"
    assert "ExprStmt(AssignExpr(Identifier(x) = IntLiteral(5)))" in ast(src)


# ══════════════════════════════════════════════════════════════════════
# 11. Literals
# ══════════════════════════════════════════════════════════════════════

def test_int_literal():
    src = "void main() { int x = 42; }"
    assert "IntLiteral(42)" in ast(src)


def test_float_literal():
    src = "void main() { float x = 1.5; }"
    assert "FloatLiteral(1.5)" in ast(src)


def test_float_literal_exponent():
    src = "void main() { float x = 1e4; }"
    assert "FloatLiteral(10000.0)" in ast(src)


def test_string_literal():
    src = 'void main() { string s = "hello"; }'
    assert "StringLiteral('hello')" in ast(src)


def test_string_literal_escape():
    src = 'void main() { string s = "a\\tb"; }'
    result = ast(src)
    assert "StringLiteral(" in result
    assert "a\\\\tb" in result or "a\\tb" in result


def test_string_literal_empty():
    src = 'void main() { string s = ""; }'
    assert "StringLiteral('')" in ast(src)


# ══════════════════════════════════════════════════════════════════════
# 12. Binary operators
# ══════════════════════════════════════════════════════════════════════

def test_add():
    src = "void main() { int x = 1 + 2; }"
    assert "BinaryOp(IntLiteral(1), +, IntLiteral(2))" in ast(src)


def test_subtract():
    src = "void main() { int x = 5 - 3; }"
    assert "BinaryOp(IntLiteral(5), -, IntLiteral(3))" in ast(src)


def test_multiply():
    src = "void main() { int x = 2 * 3; }"
    assert "BinaryOp(IntLiteral(2), *, IntLiteral(3))" in ast(src)


def test_divide():
    src = "void main() { int x = 6 / 2; }"
    assert "BinaryOp(IntLiteral(6), /, IntLiteral(2))" in ast(src)


def test_modulus():
    src = "void main() { int x = 7 % 3; }"
    assert "BinaryOp(IntLiteral(7), %, IntLiteral(3))" in ast(src)


def test_equal():
    src = "void main() { int x = 1 == 1; }"
    assert "BinaryOp(IntLiteral(1), ==, IntLiteral(1))" in ast(src)


def test_not_equal():
    src = "void main() { int x = 1 != 2; }"
    assert "BinaryOp(IntLiteral(1), !=, IntLiteral(2))" in ast(src)


def test_less_than():
    src = "void main() { int x = 1 < 2; }"
    assert "BinaryOp(IntLiteral(1), <, IntLiteral(2))" in ast(src)


def test_less_equal():
    src = "void main() { int x = 1 <= 2; }"
    assert "BinaryOp(IntLiteral(1), <=, IntLiteral(2))" in ast(src)


def test_greater_than():
    src = "void main() { int x = 2 > 1; }"
    assert "BinaryOp(IntLiteral(2), >, IntLiteral(1))" in ast(src)


def test_greater_equal():
    src = "void main() { int x = 2 >= 1; }"
    assert "BinaryOp(IntLiteral(2), >=, IntLiteral(1))" in ast(src)


def test_logical_and():
    src = "void main() { int x = 1 && 0; }"
    assert "BinaryOp(IntLiteral(1), &&, IntLiteral(0))" in ast(src)


def test_logical_or():
    src = "void main() { int x = 0 || 1; }"
    assert "BinaryOp(IntLiteral(0), ||, IntLiteral(1))" in ast(src)


# ══════════════════════════════════════════════════════════════════════
# 13. Operator precedence and associativity
# ══════════════════════════════════════════════════════════════════════

def test_precedence_mul_over_add():
    src = "void main() { int x = 1 + 2 * 3; }"
    assert "BinaryOp(IntLiteral(1), +, BinaryOp(IntLiteral(2), *, IntLiteral(3)))" in ast(src)


def test_precedence_add_left_assoc():
    src = "void main() { int x = 1 + 2 + 3; }"
    assert "BinaryOp(BinaryOp(IntLiteral(1), +, IntLiteral(2)), +, IntLiteral(3))" in ast(src)


def test_precedence_compare_over_logical():
    src = "void main() { int x = 1 < 2 && 3 > 0; }"
    result = ast(src)
    assert "BinaryOp(BinaryOp(IntLiteral(1), <, IntLiteral(2)), &&, BinaryOp(IntLiteral(3), >, IntLiteral(0)))" in result


def test_precedence_or_lowest():
    src = "void main() { int x = 1 || 2 && 3; }"
    assert "BinaryOp(IntLiteral(1), ||, BinaryOp(IntLiteral(2), &&, IntLiteral(3)))" in ast(src)


def test_assign_right_assoc():
    src = "void main() { int a; int b; a = b = 5; }"
    assert "AssignExpr(Identifier(a) = AssignExpr(Identifier(b) = IntLiteral(5)))" in ast(src)


def test_parenthesized_expr():
    src = "void main() { int x = (1 + 2) * 3; }"
    assert "BinaryOp(BinaryOp(IntLiteral(1), +, IntLiteral(2)), *, IntLiteral(3))" in ast(src)


# ══════════════════════════════════════════════════════════════════════
# 14. Unary operators (prefix)
# ══════════════════════════════════════════════════════════════════════

def test_prefix_not():
    src = "void main() { int x = !0; }"
    assert "PrefixOp(!IntLiteral(0))" in ast(src)


def test_prefix_neg():
    src = "void main() { int x = -a; }"
    assert "PrefixOp(-Identifier(a))" in ast(src)


def test_prefix_pos():
    src = "void main() { int x = +a; }"
    assert "PrefixOp(+Identifier(a))" in ast(src)


def test_prefix_inc():
    src = "void main() { int x; ++x; }"
    assert "PrefixOp(++Identifier(x))" in ast(src)


def test_prefix_dec():
    src = "void main() { int x; --x; }"
    assert "PrefixOp(--Identifier(x))" in ast(src)


# ══════════════════════════════════════════════════════════════════════
# 15. Postfix operators
# ══════════════════════════════════════════════════════════════════════

def test_postfix_inc():
    src = "void main() { int x; x++; }"
    assert "PostfixOp(Identifier(x)++)" in ast(src)


def test_postfix_dec():
    src = "void main() { int x; x--; }"
    assert "PostfixOp(Identifier(x)--)" in ast(src)


# ══════════════════════════════════════════════════════════════════════
# 16. Member access
# ══════════════════════════════════════════════════════════════════════

def test_member_access():
    src = "struct S { int x; }; void main() { S s; s.x; }"
    assert "MemberAccess(Identifier(s).x)" in ast(src)


def test_member_access_chain():
    src = "struct A { int a; }; struct B { A inner; }; void main() { B b; b.inner.a; }"
    assert "MemberAccess(MemberAccess(Identifier(b).inner).a)" in ast(src)


def test_member_access_assign():
    src = "struct S { int x; }; void main() { S s; s.x = 5; }"
    assert "AssignExpr(MemberAccess(Identifier(s).x) = IntLiteral(5))" in ast(src)


# ══════════════════════════════════════════════════════════════════════
# 17. Function calls
# ══════════════════════════════════════════════════════════════════════

def test_func_call_no_args():
    src = "void main() { foo(); }"
    assert "FuncCall(foo, [])" in ast(src)


def test_func_call_one_arg():
    src = "void main() { foo(1); }"
    assert "FuncCall(foo, [IntLiteral(1)])" in ast(src)


def test_func_call_multiple_args():
    src = "void main() { foo(1, 2, 3); }"
    assert "FuncCall(foo, [IntLiteral(1), IntLiteral(2), IntLiteral(3)])" in ast(src)


def test_func_call_expr_arg():
    src = "void main() { foo(1 + 2); }"
    assert "FuncCall(foo, [BinaryOp(IntLiteral(1), +, IntLiteral(2))])" in ast(src)


def test_func_call_nested():
    src = "void main() { foo(bar()); }"
    assert "FuncCall(foo, [FuncCall(bar, [])])" in ast(src)


def test_func_call_member_access():
    src = "struct S { int x; }; S getS() {} void main() { getS().x; }"
    assert "MemberAccess(FuncCall(getS, []).x)" in ast(src)


# ══════════════════════════════════════════════════════════════════════
# 18. Struct literals
# ══════════════════════════════════════════════════════════════════════

def test_struct_literal_empty():
    src = "struct S {}; void main() { S s = {}; }"
    assert "StructLiteral({})" in ast(src)


def test_struct_literal_values():
    src = "struct S { int a; int b; }; void main() { S s = {1, 2}; }"
    assert "StructLiteral({IntLiteral(1), IntLiteral(2)})" in ast(src)


def test_struct_literal_nested():
    src = "struct A { int x; }; struct B { A a; int y; }; void main() { B b = {{1}, 2}; }"
    assert "StructLiteral({StructLiteral({IntLiteral(1)}), IntLiteral(2)})" in ast(src)


def test_struct_literal_as_arg():
    src = "struct S { int x; }; void f(S s) {} void main() { f({5}); }"
    assert "FuncCall(f, [StructLiteral({IntLiteral(5)})])" in ast(src)


# ══════════════════════════════════════════════════════════════════════
# 19. Block statements
# ══════════════════════════════════════════════════════════════════════

def test_block_empty():
    src = "void main() { {} }"
    result = ast(src)
    assert "BlockStmt([])" in result


def test_block_multiple_stmts():
    src = "void main() { int x; int y; }"
    assert "VarDecl(IntType(), x), VarDecl(IntType(), y)" in ast(src)


def test_empty_stmt_ignored():
    src = "void main() { ; ; }"
    assert ast(src) == "Program([FuncDecl(VoidType(), main, [], [])])"


# ══════════════════════════════════════════════════════════════════════
# 20. Complex / integration tests
# ══════════════════════════════════════════════════════════════════════

def test_fibonacci():
    src = """
    int fib(int n) {
        if (n <= 1) return n;
        return fib(n - 1) + fib(n - 2);
    }
    """
    result = ast(src)
    assert "FuncDecl(IntType(), fib, [Param(IntType(), n)]" in result
    assert "IfStmt(" in result
    assert "ReturnStmt(" in result
    assert "FuncCall(fib," in result


def test_full_program():
    src = """
    struct Point { int x; int y; };

    int distance(Point p) {
        return p.x + p.y;
    }

    void main() {
        Point p = {3, 4};
        auto d = distance(p);
    }
    """
    result = ast(src)
    assert "StructDecl(Point," in result
    assert "FuncDecl(IntType(), distance," in result
    assert "FuncDecl(VoidType(), main," in result
    assert "MemberAccess(Identifier(p).x)" in result
    assert "FuncCall(distance, [Identifier(p)])" in result


def test_while_with_for():
    src = """
    void main() {
        int sum = 0;
        for (int i = 0; i < 10; i++) {
            sum = sum + i;
        }
        while (sum > 0) {
            sum = sum - 1;
        }
    }
    """
    result = ast(src)
    assert "ForStmt(" in result
    assert "WhileStmt(" in result
    assert "VarDecl(IntType(), sum = IntLiteral(0))" in result


def test_switch_full():
    src = """
    void main() {
        int x = 1;
        switch (x) {
            case 1:
                x = 10;
                break;
            case 2:
                x = 20;
                break;
            default:
                x = 0;
        }
    }
    """
    result = ast(src)
    assert "SwitchStmt(" in result
    assert "CaseStmt(case IntLiteral(1):" in result
    assert "CaseStmt(case IntLiteral(2):" in result
    assert "DefaultStmt(default:" in result


def test_nested_if_else():
    src = """
    void main() {
        int x;
        if (x > 0) {
            if (x > 10) {
                x = 10;
            } else {
                x = x + 1;
            }
        } else {
            x = 0;
        }
    }
    """
    result = ast(src)
    assert result.count("IfStmt(") == 2


def test_complex_expression():
    src = "void main() { int r = (1 + 2) * 3 - 4 / 2; }"
    result = ast(src)
    assert "BinaryOp(" in result


def test_chained_member_postfix():
    src = "struct S { int x; }; void main() { S s; s.x++; }"
    assert "PostfixOp(MemberAccess(Identifier(s).x)++)" in ast(src)


def test_multiple_returns():
    src = """
    int abs(int x) {
        if (x < 0) return -x;
        return x;
    }
    """
    result = ast(src)
    assert result.count("ReturnStmt(") == 2
    assert "PrefixOp(-Identifier(x))" in result
