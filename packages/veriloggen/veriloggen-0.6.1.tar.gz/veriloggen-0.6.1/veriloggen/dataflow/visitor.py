from __future__ import absolute_import
from __future__ import print_function

from . import dtypes

#-------------------------------------------------------------------------------
class _Visitor(object):
    def __init__(self):
        self.visited_node = {}

    def generic_visit(self, node):
        raise TypeError("Type '%s' is not supported." % str(type(node)))
    
    def visit(self, node):
        if node in self.visited_node:
            return self.visited_node[node]
        
        ret = self._visit(node)
        self.visited_node[node] = ret
        return ret
        
    def _visit(self, node):
        if isinstance(node, dtypes._Accumulator):
            return self.visit__Accumulator(node)
        
        if isinstance(node, dtypes._BinaryOperator):
            return self.visit__BinaryOperator(node)

        if isinstance(node, dtypes._UnaryOperator):
            return self.visit__UnaryOperator(node)

        if isinstance(node, dtypes._SpecialOperator):
            return self.visit__SpecialOperator(node)

        if isinstance(node, dtypes._Variable):
            return self.visit__Variable(node)

        if isinstance(node, dtypes._Constant):
            return self.visit__Constant(node)

        visitor = getattr(self, 'visit_' + node.__class__.__name__, self.generic_visit)
        return visitor(node)

    def visit__BinaryOperator(self, node):
        raise NotImplementedError()

    def visit__UnaryOperator(self, node):
        raise NotImplementedError()
    
    def visit__SpecialOperator(self, node):
        raise NotImplementedError()
    
    def visit__Accumulator(self, node):
        raise NotImplementedError()
    
    def visit__Variable(self, node):
        raise NotImplementedError()
        
    def visit__Constant(self, node):
        raise NotImplementedError()

#-------------------------------------------------------------------------------    
class InputVisitor(_Visitor):
    def visit__BinaryOperator(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return left | right

    def visit__UnaryOperator(self, node):
        right = self.visit(node.right)
        return right

    def visit__SpecialOperator(self, node):
        ret = set()
        for var in node.args:
            var = self.visit(var)
            ret.update(var)
        return ret
    
    def visit__Accumulator(self, node):
        right = self.visit(node.right)
        initval = self.visit(node.initval) if node.initval is not None else set()
        reset = self.visit(node.reset) if node.reset is not None else set()
        return right | initval | reset

    def visit__Variable(self, node):
        return set([node])
        
    def visit__Constant(self, node):
        return set()

#-------------------------------------------------------------------------------    
class OutputVisitor(_Visitor):
    def visit__BinaryOperator(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        mine = set([node]) if node._has_output() else set()
        return left | right | mine

    def visit__UnaryOperator(self, node):
        right = self.visit(node.right)
        mine = set([node]) if node._has_output() else set()
        return right | mine
    
    def visit__SpecialOperator(self, node):
        ret = set()
        for var in node.args:
            var = self.visit(var)
            ret.update(var)
        mine = set([node]) if node._has_output() else set()
        return ret | mine
    
    def visit__Accumulator(self, node):
        right = self.visit(node.right)
        mine = set([node]) if node._has_output() else set()
        return right | mine
        
    def visit__Variable(self, node):
        mine = set([node]) if node._has_output() else set()
        return mine
        
    def visit__Constant(self, node):
        mine = set([node]) if node._has_output() else set()
        return mine

#-------------------------------------------------------------------------------    
class OperatorVisitor(_Visitor):
    def visit__BinaryOperator(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        mine = set([node])
        return left | right | mine

    def visit__UnaryOperator(self, node):
        right = self.visit(node.right)
        mine = set([node])
        return right | mine
    
    def visit__SpecialOperator(self, node):
        ret = set()
        for var in node.args:
            var = self.visit(var)
            ret.update(var)
        mine = set([node])
        return ret | mine

    def visit__Accumulator(self, node):
        right = self.visit(node.right)
        initval = self.visit(node.initval) if node.initval is not None else set()
        reset = self.visit(node.reset) if node.reset is not None else set()
        mine = set([node])
        return right | initval | reset | mine
            
    def visit__Variable(self, node):
        return set()
        
    def visit__Constant(self, node):
        return set()

class AllVisitor(OperatorVisitor):
    def visit__Variable(self, node):
        return set([node])
        
    def visit__Constant(self, node):
        return set([node])
