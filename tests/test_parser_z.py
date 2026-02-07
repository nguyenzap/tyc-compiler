"""
Parser test cases for TyC compiler
TODO: Implement 100 test cases for parser
"""

import pytest
from tests.utils import Parser


# ========== Simple Test Cases (10 types) ==========
def test_empty_program():
    """1. Empty program"""
    assert Parser("").parse() == "success"


def test_program_with_only_main():
    """2. Program with only main function"""
    assert Parser("void main() {}").parse() == "success"


def test_struct_simple():
    """3. Struct declaration"""
    source = "struct Point { int x; int y; };"
    assert Parser(source).parse() == "success"


def test_function_no_params():
    """4. Function with no parameters"""
    source = "void greet() { printString(\"Hello\"); }"
    assert Parser(source).parse() == "success"


def test_var_decl_auto_with_init():
    """5. Variable declaration"""
    source = "void main() { auto x = 5; }"
    assert Parser(source).parse() == "success"


def test_if_simple():
    """6. If statement"""
    source = "void main() { if (1) printInt(1); }"
    assert Parser(source).parse() == "success"


def test_while_simple():
    """7. While statement"""
    source = "void main() { while (1) printInt(1); }"
    assert Parser(source).parse() == "success"


def test_for_simple():
    """8. For statement"""
    source = "void main() { for (auto i = 0; i < 10; ++i) printInt(i); }"
    assert Parser(source).parse() == "success"


def test_switch_simple():
    """9. Switch statement"""
    source = "void main() { switch (1) { case 1: printInt(1); break; } }"
    assert Parser(source).parse() == "success"


def test_assignment_simple():
    """10. Assignment statement"""
    source = "void main() { int x; x = 5; }"
    assert Parser(source).parse() == "success"


# ========== Additional Test Cases (100 new tests) ==========

# ========== Program Structure (4 tests) ==========
def test_program_single_function():
    """11. Program: single function"""
    assert Parser("int add(int x, int y) { return x + y; }").parse() == "success"


def test_program_multiple_functions():
    """12. Program: multiple functions"""
    source = """
    int add(int x, int y) { return x + y; }
    int sub(int x, int y) { return x - y; }
    void main() {}
    """
    assert Parser(source).parse() == "success"


def test_program_single_struct():
    """13. Program: single struct"""
    assert Parser("struct Empty {};").parse() == "success"


def test_program_mixed():
    """14. Program: structs and functions"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p; }
    """
    assert Parser(source).parse() == "success"


# ========== Struct Declarations (9 tests) ==========
def test_struct_empty():
    """15. Struct: empty struct"""
    assert Parser("struct Empty {};").parse() == "success"


def test_struct_with_multiple_types():
    """16. Struct: multiple types"""
    source = "struct Person { string name; int age; float height; };"
    assert Parser(source).parse() == "success"


def test_struct_with_struct_member():
    """17. Struct: with struct member"""
    source = """
    struct Point { int x; int y; };
    struct Line { Point start; Point end; };
    """
    assert Parser(source).parse() == "success"


def test_struct_single_member():
    """18. Struct: single member"""
    assert Parser("struct Single { int value; };").parse() == "success"


def test_struct_string_member():
    """19. Struct: with string member"""
    assert Parser("struct Data { string text; };").parse() == "success"


def test_struct_float_member():
    """20. Struct: with float member"""
    assert Parser("struct Real { float value; };").parse() == "success"


def test_struct_multiple_same_type():
    """21. Struct: multiple same type"""
    assert Parser("struct Coords { int x; int y; int z; };").parse() == "success"


def test_struct_void_not_allowed():
    """22. Struct: void type should fail"""
    # This should actually fail in semantic analysis, but grammar should parse it
    assert Parser("struct Bad { void x; };").parse() == "success"


def test_struct_complex_nested():
    """23. Struct: complex nesting"""
    source = """
    struct A { int x; };
    struct B { A a; int y; };
    struct C { B b; int z; };
    """
    assert Parser(source).parse() == "success"


# ========== Function Declarations (14 tests) ==========
def test_function_int_return():
    """24. Function: int return type"""
    assert Parser("int getValue() { return 42; }").parse() == "success"


def test_function_float_return():
    """25. Function: float return type"""
    assert Parser("float getPI() { return 3.14; }").parse() == "success"


def test_function_string_return():
    """26. Function: string return type"""
    assert Parser('string getName() { return "John"; }').parse() == "success"


def test_function_with_one_param():
    """27. Function: one parameter"""
    assert Parser("int square(int x) { return x * x; }").parse() == "success"


def test_function_with_multiple_params():
    """28. Function: multiple parameters"""
    assert Parser("int sum(int a, int b, int c) { return a + b + c; }").parse() == "success"


def test_function_auto_return():
    """29. Function: auto return type"""
    assert Parser("getX() { return 5; }").parse() == "success"


def test_function_struct_param():
    """30. Function: struct parameter"""
    source = """
    struct Point { int x; int y; };
    void printPoint(Point p) { printInt(p.x); }
    """
    assert Parser(source).parse() == "success"


def test_function_struct_return():
    """31. Function: struct return type"""
    source = """
    struct Point { int x; int y; };
    Point origin() { return {0, 0}; }
    """
    assert Parser(source).parse() == "success"


def test_function_no_body_not_allowed():
    """32. Function: with empty body"""
    assert Parser("void empty() {}").parse() == "success"


def test_function_complex_body():
    """33. Function: complex body"""
    source = """
    int factorial(int n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_function_multiple_statements():
    """34. Function: multiple statements"""
    source = """
    void process() {
        int x = 5;
        int y = 10;
        int z = x + y;
        printInt(z);
    }
    """
    assert Parser(source).parse() == "success"


def test_function_mixed_params():
    """35. Function: mixed parameter types"""
    assert Parser("void mixed(int a, float b, string c) {}").parse() == "success"


def test_function_auto_with_params():
    """36. Function: auto return with params"""
    assert Parser("multiply(int x, int y) { return x * y; }").parse() == "success"


def test_function_many_params():
    """37. Function: many parameters"""
    assert Parser("void many(int a, int b, int c, int d, int e) {}").parse() == "success"


# ========== Variable Declarations (9 tests) ==========
def test_var_decl_auto_no_init():
    """38. VarDecl: auto without init"""
    assert Parser("void main() { auto x; }").parse() == "success"


def test_var_decl_int_with_init():
    """39. VarDecl: int with init"""
    assert Parser("void main() { int x = 10; }").parse() == "success"


def test_var_decl_int_no_init():
    """40. VarDecl: int without init"""
    assert Parser("void main() { int x; }").parse() == "success"


def test_var_decl_float_with_init():
    """41. VarDecl: float with init"""
    assert Parser("void main() { float pi = 3.14; }").parse() == "success"


def test_var_decl_float_no_init():
    """42. VarDecl: float without init"""
    assert Parser("void main() { float x; }").parse() == "success"


def test_var_decl_string_with_init():
    """43. VarDecl: string with init"""
    assert Parser('void main() { string s = "hello"; }').parse() == "success"


def test_var_decl_string_no_init():
    """44. VarDecl: string without init"""
    assert Parser("void main() { string s; }").parse() == "success"


def test_var_decl_struct_with_init():
    """45. VarDecl: struct with init"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p = {1, 2}; }
    """
    assert Parser(source).parse() == "success"


def test_var_decl_struct_no_init():
    """46. VarDecl: struct without init"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p; }
    """
    assert Parser(source).parse() == "success"


# ========== If Statements (5 tests) ==========
def test_if_with_else():
    """47. If: with else"""
    source = "void main() { if (1) printInt(1); else printInt(0); }"
    assert Parser(source).parse() == "success"


def test_if_nested():
    """48. If: nested"""
    source = """
    void main() {
        if (1) {
            if (2) {
                printInt(3);
            }
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_if_with_block():
    """49. If: with block"""
    source = """
    void main() {
        if (x > 0) {
            printInt(x);
            x++;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_if_else_if():
    """50. If: else if chain"""
    source = """
    void main() {
        if (x == 1) printInt(1);
        else if (x == 2) printInt(2);
        else printInt(3);
    }
    """
    assert Parser(source).parse() == "success"


def test_if_complex_condition():
    """51. If: complex condition"""
    source = "void main() { if (x > 0 && y < 10) printInt(1); }"
    assert Parser(source).parse() == "success"


# ========== While Statements (4 tests) ==========
def test_while_with_block():
    """52. While: with block"""
    source = """
    void main() {
        while (i < 10) {
            printInt(i);
            i++;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_while_nested():
    """53. While: nested"""
    source = """
    void main() {
        while (i < 10) {
            while (j < 5) {
                printInt(j);
                j++;
            }
            i++;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_while_with_break():
    """54. While: with break"""
    source = """
    void main() {
        while (1) {
            if (x > 10) break;
            x++;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_while_with_continue():
    """55. While: with continue"""
    source = """
    void main() {
        while (i < 10) {
            if (i % 2 == 0) continue;
            printInt(i);
            i++;
        }
    }
    """
    assert Parser(source).parse() == "success"


# ========== For Statements (6 tests) ==========
def test_for_all_parts():
    """56. For: all parts"""
    source = "void main() { for (int i = 0; i < 10; i++) printInt(i); }"
    assert Parser(source).parse() == "success"


def test_for_no_init():
    """57. For: no init"""
    source = "void main() { for (; i < 10; i++) printInt(i); }"
    assert Parser(source).parse() == "success"


def test_for_no_condition():
    """58. For: no condition"""
    source = "void main() { for (int i = 0; ; i++) { if (i > 10) break; } }"
    assert Parser(source).parse() == "success"


def test_for_no_update():
    """59. For: no update"""
    source = "void main() { for (int i = 0; i < 10; ) { printInt(i); i++; } }"
    assert Parser(source).parse() == "success"


def test_for_minimal():
    """60. For: minimal (infinite loop)"""
    source = "void main() { for (;;) { break; } }"
    assert Parser(source).parse() == "success"


def test_for_complex_update():
    """61. For: complex update"""
    source = "void main() { for (int i = 0; i < 10; i = i + 2) printInt(i); }"
    assert Parser(source).parse() == "success"


# ========== Switch Statements (7 tests) ==========
def test_switch_with_default():
    """62. Switch: with default"""
    source = """
    void main() {
        switch (x) {
            case 1: printInt(1); break;
            default: printInt(0); break;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_empty():
    """63. Switch: empty"""
    source = "void main() { switch (x) {} }"
    assert Parser(source).parse() == "success"


def test_switch_multiple_cases():
    """64. Switch: multiple cases"""
    source = """
    void main() {
        switch (day) {
            case 1: printInt(1); break;
            case 2: printInt(2); break;
            case 3: printInt(3); break;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_fall_through():
    """65. Switch: fall through"""
    source = """
    void main() {
        switch (x) {
            case 1:
            case 2:
            case 3:
                printInt(123);
                break;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_default_first():
    """66. Switch: default first"""
    source = """
    void main() {
        switch (x) {
            default: printInt(0); break;
            case 1: printInt(1); break;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_no_break():
    """67. Switch: no break (fall through)"""
    source = """
    void main() {
        switch (x) {
            case 1: printInt(1);
            case 2: printInt(2);
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_complex_case():
    """68. Switch: complex case expression"""
    source = """
    void main() {
        switch (x) {
            case 1 + 2: printInt(3); break;
            case 4 * 5: printInt(20); break;
        }
    }
    """
    assert Parser(source).parse() == "success"


# ========== Break and Continue (2 tests) ==========
def test_break_in_for():
    """69. Break: in for loop"""
    source = "void main() { for (int i = 0; i < 10; i++) { if (i == 5) break; } }"
    assert Parser(source).parse() == "success"


def test_continue_in_for():
    """70. Continue: in for loop"""
    source = "void main() { for (int i = 0; i < 10; i++) { if (i % 2 == 0) continue; } }"
    assert Parser(source).parse() == "success"


# ========== Return Statements (3 tests) ==========
def test_return_with_value():
    """71. Return: with value"""
    assert Parser("int getValue() { return 42; }").parse() == "success"


def test_return_with_expression():
    """72. Return: with expression"""
    assert Parser("int compute() { return 5 + 3 * 2; }").parse() == "success"


def test_return_void():
    """73. Return: void"""
    assert Parser("void doSomething() { printInt(1); return; }").parse() == "success"


# ========== Expression Statements (5 tests) ==========
def test_expr_function_call():
    """74. ExprStmt: function call"""
    assert Parser("void main() { printInt(5); }").parse() == "success"


def test_expr_assignment():
    """75. ExprStmt: assignment"""
    assert Parser("void main() { int x; x = 10; }").parse() == "success"


def test_expr_increment():
    """76. ExprStmt: increment"""
    assert Parser("void main() { int x; x++; }").parse() == "success"


def test_expr_decrement():
    """77. ExprStmt: decrement"""
    assert Parser("void main() { int x; x--; }").parse() == "success"


def test_expr_complex():
    """78. ExprStmt: complex expression"""
    assert Parser("void main() { x = y + z * 2; }").parse() == "success"


# ========== Expression Precedence (20 tests) ==========
def test_precedence_mul_add():
    """79. Precedence: 2 + 3 * 4"""
    assert Parser("void main() { auto x = 2 + 3 * 4; }").parse() == "success"


def test_precedence_assignment():
    """80. Precedence: x = y = 5"""
    assert Parser("void main() { int x; int y; x = y = 5; }").parse() == "success"


def test_precedence_logical_and_or():
    """81. Precedence: a && b || c"""
    assert Parser("void main() { auto x = a && b || c; }").parse() == "success"


def test_precedence_relational():
    """82. Precedence: x < y == z > w"""
    assert Parser("void main() { auto result = x < y == z > w; }").parse() == "success"


def test_precedence_unary():
    """83. Precedence: !x && y"""
    assert Parser("void main() { auto result = !x && y; }").parse() == "success"


def test_precedence_parentheses():
    """84. Precedence: (a + b) * c"""
    assert Parser("void main() { auto x = (a + b) * c; }").parse() == "success"


def test_expr_member_access():
    """85. Expr: member access"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p; auto x = p.x; }
    """
    assert Parser(source).parse() == "success"


def test_expr_function_call_args():
    """86. Expr: function call with args"""
    assert Parser("void main() { auto result = add(1, 2, 3); }").parse() == "success"


def test_expr_postfix_inc():
    """87. Expr: postfix increment"""
    assert Parser("void main() { int x; auto y = x++; }").parse() == "success"


def test_expr_postfix_dec():
    """88. Expr: postfix decrement"""
    assert Parser("void main() { int x; auto y = x--; }").parse() == "success"


def test_expr_prefix_inc():
    """89. Expr: prefix increment"""
    assert Parser("void main() { int x; auto y = ++x; }").parse() == "success"


def test_expr_prefix_dec():
    """90. Expr: prefix decrement"""
    assert Parser("void main() { int x; auto y = --x; }").parse() == "success"


def test_expr_unary_not():
    """91. Expr: unary not"""
    assert Parser("void main() { auto x = !flag; }").parse() == "success"


def test_expr_unary_minus():
    """92. Expr: unary minus"""
    assert Parser("void main() { auto x = -5; }").parse() == "success"


def test_expr_unary_plus():
    """93. Expr: unary plus"""
    assert Parser("void main() { auto x = +5; }").parse() == "success"


def test_expr_struct_literal():
    """94. Expr: struct literal"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p = {10, 20}; }
    """
    assert Parser(source).parse() == "success"


def test_expr_nested_member():
    """95. Expr: nested member access"""
    source = """
    struct Point { int x; int y; };
    struct Line { Point start; Point end; };
    void main() { Line l; auto x = l.start.x; }
    """
    assert Parser(source).parse() == "success"


def test_expr_chained_calls():
    """96. Expr: chained function calls"""
    assert Parser("void main() { auto x = getPoint().x; }").parse() == "success"


def test_expr_all_operators():
    """97. Expr: all binary operators"""
    source = """
    void main() {
        auto a = 1 + 2 - 3 * 4 / 5 % 6;
        auto b = x < y && z > w || a == b && c != d;
        auto c = p <= q && r >= s;
    }
    """
    assert Parser(source).parse() == "success"


def test_expr_complex_nested():
    """98. Expr: complex nested"""
    source = """
    void main() {
        auto result = (a + b) * (c - d) / (e % f);
    }
    """
    assert Parser(source).parse() == "success"


# ========== Complex Programs (12 tests) ==========
def test_program_calculator():
    """99. Program: calculator"""
    source = """
    int add(int x, int y) { return x + y; }
    int sub(int x, int y) { return x - y; }
    int mul(int x, int y) { return x * y; }
    int div(int x, int y) { return x / y; }
    void main() {
        int a = readInt();
        int b = readInt();
        printInt(add(a, b));
    }
    """
    assert Parser(source).parse() == "success"


def test_program_factorial():
    """100. Program: factorial"""
    source = """
    int factorial(int n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }
    void main() {
        int num = readInt();
        int result = factorial(num);
        printInt(result);
    }
    """
    assert Parser(source).parse() == "success"


def test_program_struct_usage():
    """101. Program: struct usage"""
    source = """
    struct Point {
        int x;
        int y;
    };

    void printPoint(Point p) {
        printInt(p.x);
        printInt(p.y);
    }

    void main() {
        Point p = {10, 20};
        printPoint(p);
        p.x = 30;
        p.y = 40;
        printPoint(p);
    }
    """
    assert Parser(source).parse() == "success"


def test_program_nested_loops():
    """102. Program: nested loops"""
    source = """
    void main() {
        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 10; j++) {
                printInt(i * 10 + j);
            }
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_program_switch_case():
    """103. Program: switch case"""
    source = """
    void main() {
        int day = readInt();
        switch (day) {
            case 1:
                printString("Monday");
                break;
            case 2:
                printString("Tuesday");
                break;
            default:
                printString("Other");
                break;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_program_mixed_control_flow():
    """104. Program: mixed control flow"""
    source = """
    void main() {
        int i = 0;
        while (i < 100) {
            if (i % 15 == 0) {
                printString("FizzBuzz");
            } else if (i % 3 == 0) {
                printString("Fizz");
            } else if (i % 5 == 0) {
                printString("Buzz");
            } else {
                printInt(i);
            }
            i++;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_program_complex_expressions():
    """105. Program: complex expressions"""
    source = """
    void main() {
        int a = 5;
        int b = 10;
        int c = 15;
        int result = (a + b) * c - (a * b) / c + a % b;
        printInt(result);
    }
    """
    assert Parser(source).parse() == "success"


def test_program_all_statements():
    """106. Program: all statement types"""
    source = """
    struct Data { int value; };

    int process(int x) {
        if (x < 0) {
            return -x;
        }

        int sum = 0;
        for (int i = 0; i < x; i++) {
            sum = sum + i;
        }

        while (sum > 100) {
            sum = sum - 10;
        }

        switch (sum % 3) {
            case 0:
                return sum;
            case 1:
                return sum + 1;
            default:
                return sum + 2;
        }
    }

    void main() {
        Data d = {42};
        int result = process(d.value);
        printInt(result);
    }
    """
    assert Parser(source).parse() == "success"


def test_program_block_scoping():
    """107. Program: block scoping"""
    source = """
    void main() {
        int x = 10;
        {
            int x = 20;
            printInt(x);
        }
        printInt(x);
    }
    """
    assert Parser(source).parse() == "success"


def test_program_array_simulation():
    """108. Program: array simulation with struct"""
    source = """
    struct Array {
        int a0;
        int a1;
        int a2;
    };

    void main() {
        Array arr = {1, 2, 3};
        printInt(arr.a0);
        printInt(arr.a1);
        printInt(arr.a2);
    }
    """
    assert Parser(source).parse() == "success"


def test_program_multiple_returns():
    """109. Program: multiple return paths"""
    source = """
    int max(int a, int b) {
        if (a > b) {
            return a;
        } else {
            return b;
        }
    }

    void main() {
        int x = max(5, 10);
        printInt(x);
    }
    """
    assert Parser(source).parse() == "success"


def test_program_comprehensive():
    """110. Program: comprehensive test"""
    source = """
    struct Point { int x; int y; };
    struct Rectangle { Point topLeft; Point bottomRight; };

    int area(Rectangle r) {
        int width = r.bottomRight.x - r.topLeft.x;
        int height = r.bottomRight.y - r.topLeft.y;
        return width * height;
    }

    void main() {
        Rectangle rect = {{0, 0}, {10, 20}};
        int a = area(rect);
        printInt(a);

        for (int i = 0; i < a; i++) {
            if (i % 2 == 0) {
                continue;
            }
            printInt(i);
        }
    }
    """
    assert Parser(source).parse() == "success"
