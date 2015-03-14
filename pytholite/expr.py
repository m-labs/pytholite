import ast

from migen.fhdl.structure import *
from migen.fhdl.structure import _Slice

from pytholite import transel
from pytholite.reg import *
from pytholite.util import eval_ast


class ExprCompiler:
    def __init__(self, symdict):
        self.symdict = symdict

    def visit_expr(self, node):
        # Attempt compile-time evaluation first
        try:
            result = eval_ast(node, self.symdict)
        except:
            result = None
        if isinstance(result, int):
            return result

        if isinstance(node, ast.Call):
            return self.visit_expr_call(node)
        elif isinstance(node, ast.BinOp):
            return self.visit_expr_binop(node)
        elif isinstance(node, ast.Compare):
            return self.visit_expr_compare(node)
        elif isinstance(node, ast.Name):
            return self.visit_expr_name(node)
        elif isinstance(node, ast.Num):
            return self.visit_expr_num(node)
        elif isinstance(node, ast.Attribute):
            return self.visit_expr_attribute(node)
        elif isinstance(node, ast.Subscript):
            return self.visit_expr_subscript(node)
        else:
            raise NotImplementedError

    def visit_expr_call(self, node):
        if isinstance(node.func, ast.Name):
            callee = self.symdict[node.func.id]
        else:
            raise NotImplementedError
        if callee == transel.bitslice:
            if len(node.args) != 2 and len(node.args) != 3:
                raise TypeError("bitslice() takes 2 or 3 arguments")
            val = self.visit_expr(node.args[0])
            low = eval_ast(node.args[1], self.symdict)
            if len(node.args) == 3:
                up = eval_ast(node.args[2], self.symdict)
            else:
                up = low + 1
            return _Slice(val, low, up)
        else:
            raise NotImplementedError

    def visit_expr_binop(self, node):
        left = self.visit_expr(node.left)
        right = self.visit_expr(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.LShift):
            return left << right
        elif isinstance(node.op, ast.RShift):
            return left >> right
        elif isinstance(node.op, ast.BitOr):
            return left | right
        elif isinstance(node.op, ast.BitXor):
            return left ^ right
        elif isinstance(node.op, ast.BitAnd):
            return left & right
        else:
            raise NotImplementedError

    def visit_expr_compare(self, node):
        test = self.visit_expr(node.left)
        r = None
        for op, rcomparator in zip(node.ops, node.comparators):
            comparator = self.visit_expr(rcomparator)
            if isinstance(op, ast.Eq):
                comparison = test == comparator
            elif isinstance(op, ast.NotEq):
                comparison = test != comparator
            elif isinstance(op, ast.Lt):
                comparison = test < comparator
            elif isinstance(op, ast.LtE):
                comparison = test <= comparator
            elif isinstance(op, ast.Gt):
                comparison = test > comparator
            elif isinstance(op, ast.GtE):
                comparison = test >= comparator
            else:
                raise NotImplementedError
            if r is None:
                r = comparison
            else:
                r = r & comparison
            test = comparator
        return r

    def visit_expr_name(self, node):
        if node.id == "True":
            return 1
        if node.id == "False":
            return 0
        r = self.symdict[node.id]
        if isinstance(r, ImplRegister):
            r = r.storage
        return r

    def visit_expr_num(self, node):
        return node.n

    def visit_expr_attribute(self, node):
        raise NotImplementedError

    def visit_expr_subscript(self, node):
        raise NotImplementedError
