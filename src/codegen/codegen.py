"""
Code generator for TyC.
"""

from typing import Any

from ..utils.nodes import *
from ..utils.visitor import BaseVisitor
from .emitter import *
from .frame import *
from .io import IO_SYMBOL_LIST
from .utils import *


class StringArrayType:
    """Marker type for JVM main(String[] args)."""
    pass


class CodeGenerator(BaseVisitor):
    """Minimal AST -> Jasmin code generator."""

    def __init__(self):
        self.emit = None
        self.functions = {}
        self.current_return_type = VoidType()
        self.class_name = "TyC"
        self.structs: dict[str, dict[str, Any]] = {}
        self._pending_struct_type = None

    def _lookup_symbol(self, name: str, sym_list: list[Symbol]) -> Symbol:
        for sym in reversed(sym_list):
            if sym.name == name:
                return sym
        raise RuntimeError(f"Undeclared symbol: {name}")

    def _infer_type(self, node: Expr, o: Access):
        if isinstance(node, IntLiteral):
            return IntType()
        if isinstance(node, FloatLiteral):
            return FloatType()
        if isinstance(node, StringLiteral):
            return StringType()
        if isinstance(node, Identifier):
            return self._lookup_symbol(node.name, o.sym).type
        if isinstance(node, AssignExpr):
            return self._infer_type(node.rhs, o)
        if isinstance(node, FuncCall):
            return self.functions[node.name].type.return_type
        if isinstance(node, BinaryOp):
            if node.operator in ["+", "-", "*", "/", "%"]:
                left_type = self._infer_type(node.left, o)
                right_type = self._infer_type(node.right, o)
                if is_float_type(left_type) or is_float_type(right_type):
                    return FloatType()
                return IntType()
            if node.operator in ["<", "<=", ">", ">=", "==", "!="]:
                return IntType()
        return IntType()

    def visit_program(self, node: Program, o: Any = None):
        self.emit = Emitter(f"{self.class_name}.j")
        self.emit.print_out(self.emit.emit_prolog(self.class_name))

        for io_sym in IO_SYMBOL_LIST:
            self.functions[io_sym.name] = io_sym

        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                return_type = decl.return_type if decl.return_type else VoidType()
                param_types = [p.param_type for p in decl.params]
                self.functions[decl.name] = Symbol(
                    decl.name, FunctionType(param_types, return_type), CName(self.class_name)
                )

        for decl in node.decls:
            if isinstance(decl, StructDecl):
                self.visit(decl, None)

        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                self.visit(decl, None)

        self.emit.emit_epilog()

    def visit_func_decl(self, node: FuncDecl, o: Any = None):
        self.current_return_type = node.return_type if node.return_type else VoidType()
        frame = Frame(node.name, self.current_return_type)
        frame.enter_scope(True)

        if node.name == "main":
            mtype = FunctionType([StringArrayType()], VoidType())
        else:
            mtype = FunctionType([p.param_type for p in node.params], self.current_return_type)

        self.emit.print_out(self.emit.emit_method(node.name, mtype, True))

        start_label = frame.get_start_label()
        end_label = frame.get_end_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))

        local_syms: list[Symbol] = []
        if node.name == "main":
            args_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    args_idx, "args", StringArrayType(), start_label, end_label
                )
            )

        for param in node.params:
            idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(idx, param.name, param.param_type, start_label, end_label)
            )
            local_syms.append(Symbol(param.name, param.param_type, Index(idx)))

        sub_body = SubBody(frame, local_syms)
        self.visit(node.body, sub_body)

        if is_void_type(self.current_return_type):
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))
        else:
            # Emit an unreachable fallback return so the JVM verifier sees a
            # type-valid end for every code path (needed when all explicit
            # paths return early, e.g. if-else with returns in both branches).
            if is_int_type(self.current_return_type):
                self.emit.print_out(self.emit.emit_push_iconst(0, frame))
            elif is_float_type(self.current_return_type):
                self.emit.print_out(self.emit.emit_push_fconst("0.0", frame))
            else:
                self.emit.print_out(self.emit.jvm.emitPUSHNULL())
                frame.push()
            self.emit.print_out(self.emit.emit_return(self.current_return_type, frame))

        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_scope()
        self.emit.print_out(self.emit.emit_end_method(frame))

    def visit_block_stmt(self, node: BlockStmt, o: SubBody = None):
        for stmt in node.statements:
            o = self.visit(stmt, o)
        return o

    def visit_var_decl(self, node: VarDecl, o: SubBody = None):
        frame = o.frame
        idx = frame.get_new_index()
        var_type = node.var_type if node.var_type else self._infer_type(node.init_value, Access(frame, o.sym))
        self.emit.print_out(
            self.emit.emit_var(
                idx, node.name, var_type, frame.get_start_label(), frame.get_end_label()
            )
        )
        if node.init_value is not None:
            prev_pending = self._pending_struct_type
            vt_name = getattr(var_type, "struct_name", None)
            if isinstance(node.init_value, StructLiteral) and vt_name is not None:
                self._pending_struct_type = vt_name
            rhs_code, _ = self.visit(node.init_value, Access(frame, o.sym))
            self._pending_struct_type = prev_pending
            self.emit.print_out(rhs_code)
            self.emit.print_out(self.emit.emit_write_var(node.name, var_type, idx, frame))
        o.sym.append(Symbol(node.name, var_type, Index(idx)))
        return o

    def visit_expr_stmt(self, node: ExprStmt, o: SubBody = None):
        code, expr_type = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        if not is_void_type(expr_type):
            self.emit.print_out(self.emit.emit_pop(o.frame))
        return o

    def visit_if_stmt(self, node: IfStmt, o: SubBody = None):
        frame = o.frame
        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        else_label = frame.get_new_label()
        end_label = frame.get_new_label()
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(else_label, frame))
        self.visit(node.then_stmt, o)
        self.emit.print_out(self.emit.emit_goto(end_label, frame))
        self.emit.print_out(self.emit.emit_label(else_label, frame))
        if node.else_stmt:
            self.visit(node.else_stmt, o)
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        return o

    def visit_while_stmt(self, node: WhileStmt, o: SubBody = None):
        frame = o.frame
        frame.enter_loop()
        cont_label = frame.get_continue_label()
        brk_label = frame.get_break_label()
        self.emit.print_out(self.emit.emit_label(cont_label, frame))
        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(brk_label, frame))
        self.visit(node.body, o)
        self.emit.print_out(self.emit.emit_goto(cont_label, frame))
        self.emit.print_out(self.emit.emit_label(brk_label, frame))
        frame.exit_loop()
        return o

    def visit_return_stmt(self, node: ReturnStmt, o: SubBody = None):
        if node.expr is None:
            self.emit.print_out(self.emit.emit_return(VoidType(), o.frame))
            return o
        prev_pending = self._pending_struct_type
        if isinstance(node.expr, StructLiteral):
            rt_name = getattr(self.current_return_type, "struct_name", None)
            if rt_name is not None:
                self._pending_struct_type = rt_name
        code, ret_type = self.visit(node.expr, Access(o.frame, o.sym))
        self._pending_struct_type = prev_pending
        self.emit.print_out(code)
        self.emit.print_out(self.emit.emit_return(ret_type, o.frame))
        return o

    def _coerce_to_float(self, code: str, t, frame) -> str:
        """Append i2f if t is IntType, otherwise return code unchanged."""
        if is_int_type(t):
            return code + self.emit.emit_i2f(frame)
        return code

    def visit_binary_op(self, node: BinaryOp, o: Access = None):
        left_code, left_type = self.visit(node.left, o)
        right_code, right_type = self.visit(node.right, o)
        frame = o.frame

        if node.operator in ["+", "-"]:
            result_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            if is_float_type(result_type):
                left_code = self._coerce_to_float(left_code, left_type, frame)
                right_code = self._coerce_to_float(right_code, right_type, frame)
            return (
                left_code
                + right_code
                + self.emit.emit_add_op(node.operator, result_type, frame),
                result_type,
            )
        if node.operator in ["*", "/"]:
            result_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            if is_float_type(result_type):
                left_code = self._coerce_to_float(left_code, left_type, frame)
                right_code = self._coerce_to_float(right_code, right_type, frame)
            return (
                left_code
                + right_code
                + self.emit.emit_mul_op(node.operator, result_type, frame),
                result_type,
            )
        if node.operator == "%":
            return left_code + right_code + self.emit.emit_mod(frame), IntType()
        if node.operator in ["<", "<=", ">", ">=", "==", "!="]:
            op_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            if is_float_type(op_type):
                left_code = self._coerce_to_float(left_code, left_type, frame)
                right_code = self._coerce_to_float(right_code, right_type, frame)
            return left_code + right_code + self.emit.emit_re_op(node.operator, op_type, frame), IntType()
        if node.operator == "&&":
            return left_code + right_code + self.emit.emit_and_op(frame), IntType()
        if node.operator == "||":
            return left_code + right_code + self.emit.emit_or_op(frame), IntType()
        raise RuntimeError(f"Unsupported operator: {node.operator}")

    def visit_assign_expr(self, node: AssignExpr, o: Access = None):
        frame = o.frame
        if isinstance(node.lhs, MemberAccess):
            obj_code, obj_type = self.visit(node.lhs.obj, o)
            struct_name = getattr(obj_type, "struct_name", None)
            member_type = self.structs[struct_name][node.lhs.member]
            rhs_code, _ = self.visit(node.rhs, o)
            # Stack after obj_code+rhs_code: [obj_ref, rhs_val]
            # dup_x1 → [rhs_val, obj_ref, rhs_val]; putfield pops [obj, val] → [rhs_val]
            code = (obj_code + rhs_code
                    + self.emit.emit_dup_x1(frame)
                    + self.emit.emit_put_field(f"{struct_name}/{node.lhs.member}", member_type, frame))
            return code, member_type
        if not isinstance(node.lhs, Identifier):
            raise RuntimeError("Minimal codegen only supports identifier assignment")
        rhs_code, rhs_type = self.visit(node.rhs, o)
        lhs_sym = self._lookup_symbol(node.lhs.name, o.sym)
        idx = lhs_sym.value.value
        code = rhs_code + self.emit.emit_dup(frame) + self.emit.emit_write_var(
            node.lhs.name, lhs_sym.type, idx, frame
        )
        return code, rhs_type

    def visit_func_call(self, node: FuncCall, o: Access = None):
        frame = o.frame
        fn_sym = self.functions[node.name]
        fn_type = fn_sym.type
        code = ""
        for i, arg in enumerate(node.args):
            prev_pending = self._pending_struct_type
            if isinstance(arg, StructLiteral) and i < len(fn_type.param_types):
                pt_name = getattr(fn_type.param_types[i], "struct_name", None)
                if pt_name is not None:
                    self._pending_struct_type = pt_name
            arg_code, _ = self.visit(arg, o)
            self._pending_struct_type = prev_pending
            code += arg_code
        code += self.emit.emit_invoke_static(f"{fn_sym.value.value}/{node.name}", fn_type, frame)
        return code, fn_type.return_type

    def visit_identifier(self, node: Identifier, o: Access = None):
        sym = self._lookup_symbol(node.name, o.sym)
        return self.emit.emit_read_var(node.name, sym.type, sym.value.value, o.frame), sym.type

    def visit_int_literal(self, node: IntLiteral, o: Access = None):
        return self.emit.emit_push_iconst(node.value, o.frame), IntType()

    def visit_float_literal(self, node: FloatLiteral, o: Access = None):
        return self.emit.emit_push_fconst(str(node.value), o.frame), FloatType()

    def visit_string_literal(self, node: StringLiteral, o: Access = None):
        return self.emit.emit_push_const(node.value, StringType(), o.frame), StringType()

    def visit_struct_decl(self, node: StructDecl, o: Any = None):
        # Each struct compiles to its own .class. Snapshot the active emitter so the
        # main TyC class stream is not disturbed.
        prev_emit = self.emit
        struct_emit = Emitter(f"{node.name}.j")
        struct_emit.print_out(struct_emit.emit_prolog(node.name))

        # Remember member layout for later GETFIELD/PUTFIELD lookups.
        if not hasattr(self, "structs"):
            self.structs = {}
        member_table = {}
        for m in node.members:
            struct_emit.print_out(struct_emit.emit_field_decl(m.name, m.member_type))
            member_table[m.name] = m.member_type
        self.structs[node.name] = member_table

        struct_emit.print_out(struct_emit.emit_default_ctor())
        struct_emit.emit_epilog()

        self.emit = prev_emit
        return None

    def visit_member_decl(self, node: MemberDecl, o: Any = None):
        return None

    def visit_param(self, node: Param, o: Any = None):
        return None

    def visit_int_type(self, node: IntType, o: Any = None):
        return node

    def visit_float_type(self, node: FloatType, o: Any = None):
        return node

    def visit_string_type(self, node: StringType, o: Any = None):
        return node

    def visit_void_type(self, node: VoidType, o: Any = None):
        return node

    def visit_struct_type(self, node: StructType, o: Any = None):
        return node

    def visit_for_stmt(self, node: ForStmt, o: SubBody = None):
        frame = o.frame
        # init runs in same scope as the loop
        if node.init is not None:
            o = self.visit(node.init, o)

        frame.enter_loop()
        cont_label = frame.get_continue_label()
        brk_label = frame.get_break_label()
        start_label = frame.get_new_label()

        self.emit.print_out(self.emit.emit_label(start_label, frame))
        if node.condition is not None:
            cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
            self.emit.print_out(cond_code)
            self.emit.print_out(self.emit.emit_if_false(brk_label, frame))

        self.visit(node.body, o)

        self.emit.print_out(self.emit.emit_label(cont_label, frame))
        if node.update is not None:
            upd_code, upd_type = self.visit(node.update, Access(frame, o.sym))
            self.emit.print_out(upd_code)
            if not is_void_type(upd_type):
                self.emit.print_out(self.emit.emit_pop(frame))

        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        self.emit.print_out(self.emit.emit_label(brk_label, frame))
        frame.exit_loop()
        return o

    def visit_switch_stmt(self, node: SwitchStmt, o: SubBody = None):
        frame = o.frame

        sel_code, _ = self.visit(node.expr, Access(frame, o.sym))
        sel_idx = frame.get_new_index()
        self.emit.print_out(sel_code)
        self.emit.print_out(self.emit.emit_write_var(
            "_sw", IntType(), sel_idx, frame
        ))

        frame.enter_loop()
        brk_label = frame.get_break_label()

        case_labels = [frame.get_new_label() for _ in node.cases]
        default_label = frame.get_new_label()

        for i, case in enumerate(node.cases):
            self.emit.print_out(self.emit.emit_read_var(
                "_sw", IntType(), sel_idx, frame
            ))
            case_code, _ = self.visit(case.expr, Access(frame, o.sym))
            self.emit.print_out(case_code)
            frame.pop()
            frame.pop()
            self.emit.print_out(self.emit.jvm.emitIFICMPEQ(case_labels[i]))

        self.emit.print_out(self.emit.emit_goto(default_label, frame))

        for i, case in enumerate(node.cases):
            self.emit.print_out(self.emit.emit_label(case_labels[i], frame))
            for stmt in case.statements:
                self.visit(stmt, o)

        self.emit.print_out(self.emit.emit_label(default_label, frame))
        if node.default_case is not None:
            for stmt in node.default_case.statements:
                self.visit(stmt, o)

        self.emit.print_out(self.emit.emit_label(brk_label, frame))
        frame.exit_loop()
        return o

    def visit_case_stmt(self, node: CaseStmt, o: Any = None):
        return None

    def visit_default_stmt(self, node: DefaultStmt, o: Any = None):
        return None

    def visit_break_stmt(self, node: BreakStmt, o: SubBody = None):
        self.emit.print_out(self.emit.emit_goto(o.frame.get_break_label(), o.frame))
        return o

    def visit_continue_stmt(self, node: ContinueStmt, o: SubBody = None):
        self.emit.print_out(self.emit.emit_goto(o.frame.get_continue_label(), o.frame))
        return o

    def visit_prefix_op(self, node: PrefixOp, o: Access = None):
        frame = o.frame
        op = node.operator
        if op == "+":
            return self.visit(node.operand, o)
        if op == "-":
            code, t = self.visit(node.operand, o)
            return code + self.emit.emit_neg_op(t, frame), t
        if op == "!":
            code, _ = self.visit(node.operand, o)
            return code + self.emit.emit_not(frame), IntType()
        if op in ("++", "--"):
            if isinstance(node.operand, MemberAccess):
                return self._member_prefix_op(op, node.operand, frame, o)
            if not isinstance(node.operand, Identifier):
                raise RuntimeError("++/-- only supports identifier operand")
            sym = self._lookup_symbol(node.operand.name, o.sym)
            idx = sym.value.value
            load = self.emit.emit_read_var(node.operand.name, IntType(), idx, frame)
            push1 = self.emit.emit_push_iconst(1, frame)
            apply = (self.emit.jvm.emitIADD() if op == "++" else self.emit.jvm.emitISUB())
            frame.pop()
            dup = self.emit.emit_dup(frame)
            store = self.emit.emit_write_var(node.operand.name, IntType(), idx, frame)
            return load + push1 + apply + dup + store, IntType()
        raise RuntimeError(f"Unsupported prefix operator: {op}")

    def _member_prefix_op(self, op: str, ma: MemberAccess, frame, o: Access):
        """Prefix ++/-- on a struct member: returns the new value."""
        obj_code, obj_type = self.visit(ma.obj, o)
        struct_name = getattr(obj_type, "struct_name", None)
        member_type = self.structs[struct_name][ma.member]
        field = f"{struct_name}/{ma.member}"
        # Stack build: obj obj → getfield → obj val → push1 → iadd/isub → obj new_val
        # dup_x1 → new_val obj new_val → putfield → new_val
        code = obj_code
        code += self.emit.emit_dup(frame)
        code += self.emit.emit_get_field(field, member_type, frame)
        code += self.emit.emit_push_iconst(1, frame)
        code += (self.emit.jvm.emitIADD() if op == "++" else self.emit.jvm.emitISUB())
        frame.pop()
        code += self.emit.emit_dup_x1(frame)
        code += self.emit.emit_put_field(field, member_type, frame)
        return code, IntType()

    def visit_postfix_op(self, node: PostfixOp, o: Access = None):
        frame = o.frame
        op = node.operator
        if op not in ("++", "--"):
            raise RuntimeError(f"Unsupported postfix operator: {op}")
        if isinstance(node.operand, MemberAccess):
            return self._member_postfix_op(op, node.operand, frame, o)
        if not isinstance(node.operand, Identifier):
            raise RuntimeError("++/-- only supports identifier operand")
        sym = self._lookup_symbol(node.operand.name, o.sym)
        idx = sym.value.value
        load = self.emit.emit_read_var(node.operand.name, IntType(), idx, frame)
        dup = self.emit.emit_dup(frame)
        push1 = self.emit.emit_push_iconst(1, frame)
        apply = (self.emit.jvm.emitIADD() if op == "++" else self.emit.jvm.emitISUB())
        frame.pop()
        store = self.emit.emit_write_var(node.operand.name, IntType(), idx, frame)
        return load + dup + push1 + apply + store, IntType()

    def _member_postfix_op(self, op: str, ma: MemberAccess, frame, o: Access):
        """Postfix ++/-- on a struct member: returns the old value."""
        obj_code, obj_type = self.visit(ma.obj, o)
        struct_name = getattr(obj_type, "struct_name", None)
        member_type = self.structs[struct_name][ma.member]
        field = f"{struct_name}/{ma.member}"
        # obj obj → getfield → obj old_val → dup_x1 → old_val obj old_val
        # push1 → old_val obj old_val 1 → iadd/isub → old_val obj new_val → putfield → old_val
        code = obj_code
        code += self.emit.emit_dup(frame)
        code += self.emit.emit_get_field(field, member_type, frame)
        code += self.emit.emit_dup_x1(frame)
        code += self.emit.emit_push_iconst(1, frame)
        code += (self.emit.jvm.emitIADD() if op == "++" else self.emit.jvm.emitISUB())
        frame.pop()
        code += self.emit.emit_put_field(field, member_type, frame)
        return code, IntType()

    def visit_member_access(self, node: MemberAccess, o: Access = None):
        frame = o.frame
        obj_code, obj_type = self.visit(node.obj, o)
        struct_name = obj_type.struct_name
        member_type = self.structs[struct_name][node.member]
        return (
            obj_code + self.emit.emit_get_field(
                f"{struct_name}/{node.member}", member_type, frame
            ),
            member_type,
        )

    def visit_struct_literal(self, node: StructLiteral, o: Access = None):
        frame = o.frame
        struct_name = getattr(self, "_pending_struct_type", None)
        if struct_name is None:
            raise RuntimeError("StructLiteral requires enclosing struct type context")
        members = self.structs[struct_name]
        member_items = list(members.items())
        if len(member_items) != len(node.values):
            raise RuntimeError(
                f"StructLiteral arity mismatch for {struct_name}: "
                f"expected {len(member_items)}, got {len(node.values)}"
            )
        code = self.emit.emit_new_instance(struct_name, frame)
        prev_pending = self._pending_struct_type
        for (mname, mtype), value_expr in zip(member_items, node.values):
            code += self.emit.emit_dup(frame)
            mt_name = getattr(mtype, "struct_name", None)
            self._pending_struct_type = mt_name
            v_code, _ = self.visit(value_expr, o)
            code += v_code
            code += self.emit.emit_put_field(
                f"{struct_name}/{mname}", mtype, frame
            )
        self._pending_struct_type = prev_pending
        return code, StructType(struct_name)

