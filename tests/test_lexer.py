"""
Lexer test cases for TyC compiler
TODO: Implement 100 test cases for lexer
"""

import pytest
from tests.utils import Tokenizer


# ========== Simple Test Cases (10 types) ==========
def test_keyword_auto():
    """1. Keyword"""
    tokenizer = Tokenizer("auto")
    assert tokenizer.get_tokens_as_string() == "auto,<EOF>"


def test_operator_assign():
    """2. Operator"""
    tokenizer = Tokenizer("=")
    assert tokenizer.get_tokens_as_string() == "=,<EOF>"


def test_separator_semi():
    """3. Separator"""
    tokenizer = Tokenizer(";")
    assert tokenizer.get_tokens_as_string() == ";,<EOF>"


def test_integer_single_digit():
    """4. Integer literal"""
    tokenizer = Tokenizer("5")
    assert tokenizer.get_tokens_as_string() == "5,<EOF>"


def test_float_decimal():
    """5. Float literal"""
    tokenizer = Tokenizer("3.14")
    assert tokenizer.get_tokens_as_string() == "3.14,<EOF>"


def test_string_simple():
    """6. String literal"""
    tokenizer = Tokenizer('"hello"')
    assert tokenizer.get_tokens_as_string() == "hello,<EOF>"


def test_identifier_simple():
    """7. Identifier"""
    tokenizer = Tokenizer("x")
    assert tokenizer.get_tokens_as_string() == "x,<EOF>"


def test_line_comment():
    """8. Line comment"""
    tokenizer = Tokenizer("// This is a comment")
    assert tokenizer.get_tokens_as_string() == "<EOF>"


def test_integer_in_expression():
    """9. Mixed: integers and operator"""
    tokenizer = Tokenizer("5+10")
    assert tokenizer.get_tokens_as_string() == "5,+,10,<EOF>"


def test_complex_expression():
    """10. Complex: variable declaration"""
    tokenizer = Tokenizer("auto x = 5 + 3 * 2;")
    assert tokenizer.get_tokens_as_string() == "auto,x,=,5,+,3,*,2,;,<EOF>"


# ========== Additional Test Cases (100 new tests) ==========

# ========== Keywords (15 more tests) ==========
def test_keyword_break():
    """11. Keyword: break"""
    assert Tokenizer("break").get_tokens_as_string() == "break,<EOF>"


def test_keyword_case():
    """12. Keyword: case"""
    assert Tokenizer("case").get_tokens_as_string() == "case,<EOF>"


def test_keyword_continue():
    """13. Keyword: continue"""
    assert Tokenizer("continue").get_tokens_as_string() == "continue,<EOF>"


def test_keyword_default():
    """14. Keyword: default"""
    assert Tokenizer("default").get_tokens_as_string() == "default,<EOF>"


def test_keyword_else():
    """15. Keyword: else"""
    assert Tokenizer("else").get_tokens_as_string() == "else,<EOF>"


def test_keyword_float():
    """16. Keyword: float"""
    assert Tokenizer("float").get_tokens_as_string() == "float,<EOF>"


def test_keyword_for():
    """17. Keyword: for"""
    assert Tokenizer("for").get_tokens_as_string() == "for,<EOF>"


def test_keyword_if():
    """18. Keyword: if"""
    assert Tokenizer("if").get_tokens_as_string() == "if,<EOF>"


def test_keyword_int():
    """19. Keyword: int"""
    assert Tokenizer("int").get_tokens_as_string() == "int,<EOF>"


def test_keyword_return():
    """20. Keyword: return"""
    assert Tokenizer("return").get_tokens_as_string() == "return,<EOF>"


def test_keyword_string():
    """21. Keyword: string"""
    assert Tokenizer("string").get_tokens_as_string() == "string,<EOF>"


def test_keyword_struct():
    """22. Keyword: struct"""
    assert Tokenizer("struct").get_tokens_as_string() == "struct,<EOF>"


def test_keyword_switch():
    """23. Keyword: switch"""
    assert Tokenizer("switch").get_tokens_as_string() == "switch,<EOF>"


def test_keyword_void():
    """24. Keyword: void"""
    assert Tokenizer("void").get_tokens_as_string() == "void,<EOF>"


def test_keyword_while():
    """25. Keyword: while"""
    assert Tokenizer("while").get_tokens_as_string() == "while,<EOF>"


# ========== Operators (16 more tests) ==========
def test_operator_plus():
    """26. Operator: +"""
    assert Tokenizer("+").get_tokens_as_string() == "+,<EOF>"


def test_operator_minus():
    """27. Operator: -"""
    assert Tokenizer("-").get_tokens_as_string() == "-,<EOF>"


def test_operator_star():
    """28. Operator: *"""
    assert Tokenizer("*").get_tokens_as_string() == "*,<EOF>"


def test_operator_div():
    """29. Operator: /"""
    assert Tokenizer("/").get_tokens_as_string() == "/,<EOF>"


def test_operator_mod():
    """30. Operator: %"""
    assert Tokenizer("%").get_tokens_as_string() == "%,<EOF>"


def test_operator_le():
    """31. Operator: <="""
    assert Tokenizer("<=").get_tokens_as_string() == "<=,<EOF>"


def test_operator_ge():
    """32. Operator: >="""
    assert Tokenizer(">=").get_tokens_as_string() == ">=,<EOF>"


def test_operator_eq():
    """33. Operator: =="""
    assert Tokenizer("==").get_tokens_as_string() == "==,<EOF>"


def test_operator_ne():
    """34. Operator: !="""
    assert Tokenizer("!=").get_tokens_as_string() == "!=,<EOF>"


def test_operator_and():
    """35. Operator: &&"""
    assert Tokenizer("&&").get_tokens_as_string() == "&&,<EOF>"


def test_operator_or():
    """36. Operator: ||"""
    assert Tokenizer("||").get_tokens_as_string() == "||,<EOF>"


def test_operator_inc():
    """37. Operator: ++"""
    assert Tokenizer("++").get_tokens_as_string() == "++,<EOF>"


def test_operator_dec():
    """38. Operator: --"""
    assert Tokenizer("--").get_tokens_as_string() == "--,<EOF>"


def test_operator_lt():
    """39. Operator: <"""
    assert Tokenizer("<").get_tokens_as_string() == "<,<EOF>"


def test_operator_gt():
    """40. Operator: >"""
    assert Tokenizer(">").get_tokens_as_string() == ">,<EOF>"


def test_operator_not():
    """41. Operator: !"""
    assert Tokenizer("!").get_tokens_as_string() == "!,<EOF>"


def test_operator_dot():
    """42. Operator: ."""
    assert Tokenizer(".").get_tokens_as_string() == ".,<EOF>"


# ========== Separators (6 more tests) ==========
def test_separator_lbrace():
    """43. Separator: {"""
    assert Tokenizer("{").get_tokens_as_string() == "{,<EOF>"


def test_separator_rbrace():
    """44. Separator: }"""
    assert Tokenizer("}").get_tokens_as_string() == "},<EOF>"


def test_separator_lparen():
    """45. Separator: ("""
    assert Tokenizer("(").get_tokens_as_string() == "(,<EOF>"


def test_separator_rparen():
    """46. Separator: )"""
    assert Tokenizer(")").get_tokens_as_string() == "),<EOF>"


def test_separator_comma():
    """47. Separator: ,"""
    assert Tokenizer(",").get_tokens_as_string() == ",,<EOF>"


def test_separator_colon():
    """48. Separator: :"""
    assert Tokenizer(":").get_tokens_as_string() == ":,<EOF>"


# ========== Integer Literals (9 more tests) ==========
def test_integer_zero():
    """49. Integer: 0"""
    assert Tokenizer("0").get_tokens_as_string() == "0,<EOF>"


def test_integer_multi_digit():
    """50. Integer: 42"""
    assert Tokenizer("42").get_tokens_as_string() == "42,<EOF>"


def test_integer_large():
    """51. Integer: 2500"""
    assert Tokenizer("2500").get_tokens_as_string() == "2500,<EOF>"


def test_integer_negative():
    """52. Integer: -45"""
    assert Tokenizer("-45").get_tokens_as_string() == "-45,<EOF>"


def test_integer_negative_small():
    """53. Integer: -1"""
    assert Tokenizer("-1").get_tokens_as_string() == "-1,<EOF>"


def test_integer_with_leading_zeros():
    """54. Integer: 007"""
    assert Tokenizer("007").get_tokens_as_string() == "007,<EOF>"


def test_integer_255():
    """55. Integer: 255"""
    assert Tokenizer("255").get_tokens_as_string() == "255,<EOF>"


def test_integer_9():
    """56. Integer: 9"""
    assert Tokenizer("9").get_tokens_as_string() == "9,<EOF>"


def test_integer_100():
    """57. Integer: 100"""
    assert Tokenizer("100").get_tokens_as_string() == "100,<EOF>"


# ========== Float Literals (14 more tests) ==========
def test_float_zero():
    """58. Float: 0.0"""
    assert Tokenizer("0.0").get_tokens_as_string() == "0.0,<EOF>"


def test_float_trailing_dot():
    """59. Float: 1."""
    assert Tokenizer("1.").get_tokens_as_string() == "1.,<EOF>"


def test_float_leading_dot():
    """60. Float: .5"""
    assert Tokenizer(".5").get_tokens_as_string() == ".5,<EOF>"


def test_float_exponent():
    """61. Float: 1e4"""
    assert Tokenizer("1e4").get_tokens_as_string() == "1e4,<EOF>"


def test_float_exponent_negative():
    """62. Float: 2E-3"""
    assert Tokenizer("2E-3").get_tokens_as_string() == "2E-3,<EOF>"


def test_float_decimal_exponent():
    """63. Float: 1.23e4"""
    assert Tokenizer("1.23e4").get_tokens_as_string() == "1.23e4,<EOF>"


def test_float_decimal_exponent_negative():
    """64. Float: 5.67E-2"""
    assert Tokenizer("5.67E-2").get_tokens_as_string() == "5.67E-2,<EOF>"


def test_float_negative():
    """65. Float: -3.14"""
    assert Tokenizer("-3.14").get_tokens_as_string() == "-3.14,<EOF>"


def test_float_negative_exponent():
    """66. Float: -1.5e2"""
    assert Tokenizer("-1.5e2").get_tokens_as_string() == "-1.5e2,<EOF>"


def test_float_dot_zero():
    """67. Float: .0"""
    assert Tokenizer(".0").get_tokens_as_string() == ".0,<EOF>"


def test_float_zero_dot():
    """68. Float: 0."""
    assert Tokenizer("0.").get_tokens_as_string() == "0.,<EOF>"


def test_float_exponent_with_dot():
    """69. Float: 1.e5"""
    assert Tokenizer("1.e5").get_tokens_as_string() == "1.e5,<EOF>"


def test_float_exponent_positive():
    """70. Float: 1e+3"""
    assert Tokenizer("1e+3").get_tokens_as_string() == "1e+3,<EOF>"


def test_float_dot_exponent():
    """71. Float: .5e-2"""
    assert Tokenizer(".5e-2").get_tokens_as_string() == ".5e-2,<EOF>"


# ========== String Literals (14 tests) ==========
def test_string_empty():
    """72. String: empty"""
    assert Tokenizer('""').get_tokens_as_string() == ",<EOF>"


def test_string_world():
    """73. String: world"""
    assert Tokenizer('"world"').get_tokens_as_string() == "world,<EOF>"


def test_string_escape_newline():
    """74. String: with \\n"""
    assert Tokenizer('"line1\\nline2"').get_tokens_as_string() == "line1\\nline2,<EOF>"


def test_string_escape_tab():
    """75. String: with \\t"""
    assert Tokenizer('"Hello\\tWorld"').get_tokens_as_string() == "Hello\\tWorld,<EOF>"


def test_string_escape_return():
    """76. String: with \\r"""
    assert Tokenizer('"text\\r"').get_tokens_as_string() == "text\\r,<EOF>"


def test_string_escape_backspace():
    """77. String: with \\b"""
    assert Tokenizer('"back\\bspace"').get_tokens_as_string() == "back\\bspace,<EOF>"


def test_string_escape_formfeed():
    """78. String: with \\f"""
    assert Tokenizer('"form\\ffeed"').get_tokens_as_string() == "form\\ffeed,<EOF>"


def test_string_escape_quote():
    """79. String: with \\\""""
    assert Tokenizer('"He said: \\"Hi\\""').get_tokens_as_string() == 'He said: \\"Hi\\",<EOF>'


def test_string_escape_backslash():
    """80. String: with \\\\"""
    assert Tokenizer('"C:\\\\Users\\\\file"').get_tokens_as_string() == "C:\\\\Users\\\\file,<EOF>"


def test_string_multi_escape():
    """81. String: multiple escapes"""
    assert Tokenizer('"Line1\\nLine2\\nLine3"').get_tokens_as_string() == "Line1\\nLine2\\nLine3,<EOF>"


def test_string_tab_newline():
    """82. String: tab and newline"""
    assert Tokenizer('"Hello\\tWorld\\n"').get_tokens_as_string() == "Hello\\tWorld\\n,<EOF>"


def test_string_all_escapes():
    """83. String: all escape types"""
    assert Tokenizer('"\\b\\f\\r\\n\\t\\\\\\"\\""').get_tokens_as_string() == '\\b\\f\\r\\n\\t\\\\\\"\\",<EOF>'


def test_string_with_spaces():
    """84. String: with spaces"""
    assert Tokenizer('"  hello  world  "').get_tokens_as_string() == "  hello  world  ,<EOF>"


def test_string_long():
    """85. String: long string"""
    assert Tokenizer('"This is a longer string with many words"').get_tokens_as_string() == "This is a longer string with many words,<EOF>"


# ========== String Errors (6 tests) ==========
def test_string_illegal_escape_x():
    """86. String error: illegal \\x"""
    assert Tokenizer('"hello\\x"').get_tokens_as_string() == "Illegal Escape In String: hello\\x"


def test_string_illegal_escape_a():
    """87. String error: illegal \\a"""
    assert Tokenizer('"test\\a"').get_tokens_as_string() == "Illegal Escape In String: test\\a"


def test_string_illegal_escape_digit():
    """88. String error: illegal \\1"""
    assert Tokenizer('"\\123"').get_tokens_as_string() == "Illegal Escape In String: \\1"


def test_string_illegal_escape_q():
    """89. String error: illegal \\q"""
    assert Tokenizer('"abc\\q"').get_tokens_as_string() == "Illegal Escape In String: abc\\q"


def test_string_unclose_newline():
    """90. String error: unclosed with newline"""
    assert Tokenizer('"hello\n').get_tokens_as_string() == "Unclosed String: hello\n"


def test_string_unclose_eof():
    """91. String error: unclosed EOF"""
    assert Tokenizer('"world').get_tokens_as_string() == "Unclosed String: world"


# ========== Identifiers (9 tests) ==========
def test_identifier_y():
    """92. Identifier: y"""
    assert Tokenizer("y").get_tokens_as_string() == "y,<EOF>"


def test_identifier_abc():
    """93. Identifier: abc"""
    assert Tokenizer("abc").get_tokens_as_string() == "abc,<EOF>"


def test_identifier_underscore():
    """94. Identifier: _temp"""
    assert Tokenizer("_temp").get_tokens_as_string() == "_temp,<EOF>"


def test_identifier_with_underscore():
    """95. Identifier: my_var"""
    assert Tokenizer("my_var").get_tokens_as_string() == "my_var,<EOF>"


def test_identifier_double_underscore():
    """96. Identifier: __private"""
    assert Tokenizer("__private").get_tokens_as_string() == "__private,<EOF>"


def test_identifier_with_digit():
    """97. Identifier: var1"""
    assert Tokenizer("var1").get_tokens_as_string() == "var1,<EOF>"


def test_identifier_with_digits():
    """98. Identifier: counter2"""
    assert Tokenizer("counter2").get_tokens_as_string() == "counter2,<EOF>"


def test_identifier_single_underscore():
    """99. Identifier: _"""
    assert Tokenizer("_").get_tokens_as_string() == "_,<EOF>"


def test_identifier_complex():
    """100. Identifier: a_b_c_123"""
    assert Tokenizer("a_b_c_123").get_tokens_as_string() == "a_b_c_123,<EOF>"


# ========== Comments (4 tests) ==========
def test_block_comment():
    """101. Comment: block comment"""
    assert Tokenizer("/* This is a block comment */").get_tokens_as_string() == "<EOF>"


def test_block_comment_multiline():
    """102. Comment: multiline block"""
    assert Tokenizer("/* line1\nline2\nline3 */").get_tokens_as_string() == "<EOF>"


def test_comment_with_code():
    """103. Comment: with code"""
    assert Tokenizer("auto x = 5; // comment").get_tokens_as_string() == "auto,x,=,5,;,<EOF>"


def test_comment_no_nesting():
    """104. Comment: no nesting"""
    assert Tokenizer("/* /* nested */ still in comment").get_tokens_as_string() == "still,in,comment,<EOF>"


# ========== ERROR_CHAR (4 tests) ==========
def test_error_char_at():
    """105. Error: @"""
    assert Tokenizer("@").get_tokens_as_string() == "Error Token @"


def test_error_char_hash():
    """106. Error: #"""
    assert Tokenizer("#").get_tokens_as_string() == "Error Token #"


def test_error_char_dollar():
    """107. Error: $"""
    assert Tokenizer("$").get_tokens_as_string() == "Error Token $"


def test_error_char_backtick():
    """108. Error: `"""
    assert Tokenizer("`").get_tokens_as_string() == "Error Token `"


# ========== Complex/Mixed (2 tests) ==========
def test_function_declaration():
    """109. Complex: function"""
    assert Tokenizer("int add(int x, int y) { return x + y; }").get_tokens_as_string() == "int,add,(,int,x,,,int,y,),{,return,x,+,y,;,},<EOF>"


def test_struct_declaration():
    """110. Complex: struct"""
    assert Tokenizer("struct Point { int x; int y; };").get_tokens_as_string() == "struct,Point,{,int,x,;,int,y,;,},;,<EOF>"
