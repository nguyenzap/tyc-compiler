"""
AST Generation module for TyC programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.TyCVisitor import TyCVisitor
from build.TyCParser import TyCParser
from src.utils.nodes import *


class ASTGeneration(TyCVisitor):
    """AST Generation visitor for TyC language."""

    # ── Program & top-level declarations ──────────────────────────────

    def visitProgram(self, ctx: TyCParser.ProgramContext):
        decls = []
        for child in ctx.getChildren():
            if isinstance(child, TyCParser.StructDeclContext):
                decls.append(self.visit(child))
            elif isinstance(child, TyCParser.FuncDeclContext):
                decls.append(self.visit(child))
        return Program(decls)

    def visitStructDecl(self, ctx: TyCParser.StructDeclContext):
        name = ctx.IDENTIFIER().getText()
        members = [self.visit(m) for m in ctx.memberDecl()]
        return StructDecl(name, members)

    def visitMemberDecl(self, ctx: TyCParser.MemberDeclContext):
        member_type = self.visit(ctx.type_())
        name = ctx.IDENTIFIER().getText()
        return MemberDecl(member_type, name)

    def visitFuncDecl(self, ctx: TyCParser.FuncDeclContext):
        return_type = self.visit(ctx.returnType()) if ctx.returnType() else None
        name = ctx.IDENTIFIER().getText()
        params = self.visit(ctx.paramList()) if ctx.paramList() else []
        body = self.visit(ctx.blockStmt())
        return FuncDecl(return_type, name, params, body)

    def visitReturnType(self, ctx: TyCParser.ReturnTypeContext):
        return self.visit(ctx.type_())

    def visitParamList(self, ctx: TyCParser.ParamListContext):
        return [self.visit(p) for p in ctx.param()]

    def visitParam(self, ctx: TyCParser.ParamContext):
        param_type = self.visit(ctx.type_())
        name = ctx.IDENTIFIER().getText()
        return Param(param_type, name)

    # ── Types ─────────────────────────────────────────────────────────

    def visitType(self, ctx: TyCParser.TypeContext):
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.STRING():
            return StringType()
        elif ctx.VOID():
            return VoidType()
        else:
            return StructType(ctx.IDENTIFIER().getText())

    # ── Statements ────────────────────────────────────────────────────

    def visitStmt(self, ctx: TyCParser.StmtContext):
        if ctx.varDecl():
            return self.visit(ctx.varDecl())
        elif ctx.blockStmt():
            return self.visit(ctx.blockStmt())
        elif ctx.ifStmt():
            return self.visit(ctx.ifStmt())
        elif ctx.whileStmt():
            return self.visit(ctx.whileStmt())
        elif ctx.forStmt():
            return self.visit(ctx.forStmt())
        elif ctx.switchStmt():
            return self.visit(ctx.switchStmt())
        elif ctx.breakStmt():
            return self.visit(ctx.breakStmt())
        elif ctx.continueStmt():
            return self.visit(ctx.continueStmt())
        elif ctx.returnStmt():
            return self.visit(ctx.returnStmt())
        elif ctx.exprStmt():
            return self.visit(ctx.exprStmt())
        else:
            return None  # empty statement (bare SEMI)

    def visitBlockStmt(self, ctx: TyCParser.BlockStmtContext):
        stmts = []
        for s in ctx.stmt():
            result = self.visit(s)
            if result is not None:
                stmts.append(result)
        return BlockStmt(stmts)

    def visitVarDecl(self, ctx: TyCParser.VarDeclContext):
        if ctx.AUTO():
            var_type = None
        else:
            var_type = self.visit(ctx.type_())
        name = ctx.IDENTIFIER().getText()
        init_value = self.visit(ctx.expr()) if ctx.expr() else None
        return VarDecl(var_type, name, init_value)

    def visitIfStmt(self, ctx: TyCParser.IfStmtContext):
        condition = self.visit(ctx.expr())
        then_stmt = self.visit(ctx.stmt(0))
        else_stmt = self.visit(ctx.stmt(1)) if ctx.ELSE() else None
        return IfStmt(condition, then_stmt, else_stmt)

    def visitWhileStmt(self, ctx: TyCParser.WhileStmtContext):
        condition = self.visit(ctx.expr())
        body = self.visit(ctx.stmt())
        return WhileStmt(condition, body)

    def visitForStmt(self, ctx: TyCParser.ForStmtContext):
        init = self.visit(ctx.forInit()) if ctx.forInit() else None
        condition = self.visit(ctx.expr()) if ctx.expr() else None
        update = self.visit(ctx.forUpdate()) if ctx.forUpdate() else None
        body = self.visit(ctx.stmt())
        return ForStmt(init, condition, update, body)

    def visitForInit(self, ctx: TyCParser.ForInitContext):
        if ctx.AUTO():
            name = ctx.IDENTIFIER().getText()
            init_value = self.visit(ctx.expr()) if ctx.expr() else None
            return VarDecl(None, name, init_value)
        elif ctx.type_():
            var_type = self.visit(ctx.type_())
            name = ctx.IDENTIFIER().getText()
            init_value = self.visit(ctx.expr()) if ctx.expr() else None
            return VarDecl(var_type, name, init_value)
        else:
            return ExprStmt(self.visit(ctx.expr()))

    def visitForUpdate(self, ctx: TyCParser.ForUpdateContext):
        return self.visit(ctx.expr())

    def visitSwitchStmt(self, ctx: TyCParser.SwitchStmtContext):
        expr = self.visit(ctx.expr())
        cases = []
        default_case = None
        for sc in ctx.switchCase():
            result = self.visit(sc)
            if isinstance(result, CaseStmt):
                cases.append(result)
            elif isinstance(result, DefaultStmt):
                default_case = result
        return SwitchStmt(expr, cases, default_case)

    def visitSwitchCase(self, ctx: TyCParser.SwitchCaseContext):
        stmts = [self.visit(s) for s in ctx.stmt()]
        stmts = [s for s in stmts if s is not None]
        if ctx.CASE():
            expr = self.visit(ctx.expr())
            return CaseStmt(expr, stmts)
        else:
            return DefaultStmt(stmts)

    def visitBreakStmt(self, ctx: TyCParser.BreakStmtContext):
        return BreakStmt()

    def visitContinueStmt(self, ctx: TyCParser.ContinueStmtContext):
        return ContinueStmt()

    def visitReturnStmt(self, ctx: TyCParser.ReturnStmtContext):
        expr = self.visit(ctx.expr()) if ctx.expr() else None
        return ReturnStmt(expr)

    def visitExprStmt(self, ctx: TyCParser.ExprStmtContext):
        return ExprStmt(self.visit(ctx.expr()))

    # ── Expressions ───────────────────────────────────────────────────

    def visitExpr(self, ctx: TyCParser.ExprContext):
        return self.visit(ctx.assignExpr())

    def visitAssignExpr(self, ctx: TyCParser.AssignExprContext):
        if ctx.ASSIGN():
            lhs = self.visit(ctx.logicalOrExpr())
            rhs = self.visit(ctx.assignExpr())
            return AssignExpr(lhs, rhs)
        return self.visit(ctx.logicalOrExpr())

    # Helper for left-associative binary operators
    def _visit_binary(self, operands, ctx):
        exprs = [self.visit(e) for e in operands]
        if len(exprs) == 1:
            return exprs[0]
        result = exprs[0]
        for i in range(1, len(exprs)):
            op = ctx.getChild(2 * i - 1).getText()
            result = BinaryOp(result, op, exprs[i])
        return result

    def visitLogicalOrExpr(self, ctx: TyCParser.LogicalOrExprContext):
        return self._visit_binary(ctx.logicalAndExpr(), ctx)

    def visitLogicalAndExpr(self, ctx: TyCParser.LogicalAndExprContext):
        return self._visit_binary(ctx.equalityExpr(), ctx)

    def visitEqualityExpr(self, ctx: TyCParser.EqualityExprContext):
        return self._visit_binary(ctx.relationalExpr(), ctx)

    def visitRelationalExpr(self, ctx: TyCParser.RelationalExprContext):
        return self._visit_binary(ctx.additiveExpr(), ctx)

    def visitAdditiveExpr(self, ctx: TyCParser.AdditiveExprContext):
        return self._visit_binary(ctx.multiplicativeExpr(), ctx)

    def visitMultiplicativeExpr(self, ctx: TyCParser.MultiplicativeExprContext):
        return self._visit_binary(ctx.unaryExpr(), ctx)

    def visitUnaryExpr(self, ctx: TyCParser.UnaryExprContext):
        if ctx.postfixExpr():
            return self.visit(ctx.postfixExpr())
        op = ctx.getChild(0).getText()
        operand = self.visit(ctx.unaryExpr())
        return PrefixOp(op, operand)

    def visitPostfixExpr(self, ctx: TyCParser.PostfixExprContext):
        base = self.visit(ctx.primaryExpr())
        for suffix in ctx.postfixSuffix():
            if suffix.INC():
                base = PostfixOp("++", base)
            elif suffix.DEC():
                base = PostfixOp("--", base)
            elif suffix.DOT():
                member = suffix.IDENTIFIER().getText()
                base = MemberAccess(base, member)
            elif suffix.LPAREN() is not None:
                args = self.visit(suffix.argList()) if suffix.argList() else []
                name = base.name
                base = FuncCall(name, args)
        return base

    def visitPrimaryExpr(self, ctx: TyCParser.PrimaryExprContext):
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        elif ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        elif ctx.STRING_LIT():
            return StringLiteral(ctx.STRING_LIT().getText())
        elif ctx.IDENTIFIER():
            return Identifier(ctx.IDENTIFIER().getText())
        elif ctx.expr():
            return self.visit(ctx.expr())
        else:
            values = self.visit(ctx.argList()) if ctx.argList() else []
            return StructLiteral(values)

    def visitArgList(self, ctx: TyCParser.ArgListContext):
        return [self.visit(e) for e in ctx.expr()]
