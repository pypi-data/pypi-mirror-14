#!/usr/bin/env python
"""
Modelica parse Tree to AST tree.
"""
from __future__ import print_function, absolute_import, division, print_function, unicode_literals

import antlr4
import antlr4.Parser
import yaml

from . import ast
from .generated.ModelicaLexer import ModelicaLexer
from .generated.ModelicaListener import ModelicaListener
from .generated.ModelicaParser import ModelicaParser


class ASTListener(ModelicaListener):

    def __init__(self):
        self.ast = {}
        self.ast_result = None
        self.file_node = None
        self.class_node = None
        self.comp_clause = None
        self.eq_sect = None
        self.symbol_node = None
        self.eq_comment = None
        self.sym_count = 0

    # FILE ===========================================================

    def enterStored_definition(self, ctx):
        within = ''
        if ctx.WITHIN() is not None:
            within = ctx.WITHIN().getText()
        file_node = ast.File()
        file_node.within = within
        self.ast[ctx] = file_node
        self.file_node = file_node

    def exitStored_definition(self, ctx):
        for class_node in [self.ast[e] for e in ctx.stored_definition_class()]:
            self.ast[ctx].classes[class_node.name] = class_node
        self.ast_result = self.ast[ctx]

    # CLASS ===========================================================

    def enterStored_definition_class(self, ctx):
        class_node = ast.Class()
        class_node.final = ctx.FINAL() is not None
        self.class_node = class_node
        self.ast[ctx] = class_node

    def exitStored_definition_class(self, ctx):
        pass

    def enterClass_definition(self, ctx):
        class_node = self.class_node
        class_node.encapsulated = ctx.ENCAPSULATED() is not None
        class_node.partial = ctx.class_prefixes().PARTIAL() is not None
        class_node.type = ctx.class_prefixes().class_type().getText()

    def enterClass_spec_comp(self, ctx):
        class_node = self.class_node
        class_node.name = ctx.IDENT()[0].getText()

    def exitClass_spec_comp(self, ctx):
        class_node = self.class_node
        class_node.comment = self.ast[ctx.string_comment()]

    def exitComposition(self, ctx):

        for eqlist in [self.ast[e] for e in ctx.equation_section()]:
            if eqlist is not None:
                if eqlist.initial:
                    self.class_node.initial_equations += eqlist.equations
                else:
                    self.class_node.equations += eqlist.equations

    def enterEquation_section(self, ctx):
        eq_sect = ast.EquationSection(
            initial=ctx.INITIAL() is not None
        )
        self.ast[ctx] = eq_sect
        self.eq_sect = eq_sect

    def exitEquation_section(self, ctx):
        eq_sect = self.ast[ctx]
        if eq_sect.initial:
            eq_sect.equations += [self.ast[e] for e in ctx.equation()]
        else:
            eq_sect.equations += [self.ast[e] for e in ctx.equation()]

    # EQUATION ===========================================================

    def enterEquation(self, ctx):
        pass

    def exitEquation(self, ctx):
        self.ast[ctx] = self.ast[ctx.equation_options()]
        try:
            self.ast[ctx].comment = self.ast[ctx.comment()]
        except AttributeError:
            pass

    def exitEquation_simple(self, ctx):
        self.ast[ctx] = ast.Equation(
            left=self.ast[ctx.simple_expression()],
            right=self.ast[ctx.expression()])

    def exitEquation_connect_clause(self, ctx):
        self.ast[ctx] = self.ast[ctx.connect_clause()]

    def exitConnect_clause(self, ctx):
        self.ast[ctx] = ast.ConnectClause(
            left=self.ast[ctx.component_reference()[0]],
            right=self.ast[ctx.component_reference()[1]])

    # EXPRESSIONS ===========================================================

    def exitSimple_expression(self, ctx):
        # TODO only using first expression
        self.ast[ctx] = self.ast[ctx.expr()[0]]

    def exitExpression_simple(self, ctx):
        self.ast[ctx] = self.ast[ctx.simple_expression()]

    def exitExpr_primary(self, ctx):
        self.ast[ctx] = self.ast[ctx.primary()]

    def exitExpr_add(self, ctx):
        self.ast[ctx] = ast.Expression(
            operator=ctx.op.text,
            operands=[self.ast[e] for e in ctx.expr()]
        )

    def exitExpr_mul(self, ctx):
        self.ast[ctx] = ast.Expression(
            operator=ctx.op.text,
            operands=[self.ast[e] for e in ctx.expr()]
        )

    def exitExpr_rel(self, ctx):
        self.ast[ctx] = ast.Expression(
            operator=ctx.op.text,
            operands=[self.ast[e] for e in ctx.expr()]
        )

    def exitExpr_neg(self, ctx):
        self.ast[ctx] = ast.Expression(
            operator=ctx.op.text,
            operands=[self.ast[ctx.expr()]]
        )

    # PRIMARY ===========================================================

    def exitPrimary_unsigned_number(self, ctx):
        self.ast[ctx] = ast.Primary(value=str(yaml.load(ctx.getText())))

    def exitPrimary_string(self, ctx):
        self.ast[ctx] = ast.Primary(value=ctx.getText())

    def exitPrimary_false(self, ctx):
        self.ast[ctx] = ast.Primary(value=False)

    def exitPrimary_true(self, ctx):
        self.ast[ctx] = ast.Primary(value=True)

    def exitPrimary_function(self, ctx):
        self.ast[ctx] = ast.Primary(value=ctx.getText())

    def exitPrimary_derivative(self, ctx):
        self.ast[ctx] = ast.Primary(value=ctx.getText())
        comp_name = ctx.function_call_args().function_arguments().function_argument()[0].getText()
        self.ast[ctx] = ast.Expression(
            operator='der',
            operands=[ast.ComponentRef(name=comp_name)]
        )
        if 'state' not in self.class_node.symbols[comp_name].prefixes:
            self.class_node.symbols[comp_name].prefixes += ['state']

    def exitComponent_reference(self, ctx):
        # TODO handle other idents
        self.ast[ctx] = ast.ComponentRef(
            name=ctx.getText()
        )

    def exitPrimary_component_reference(self, ctx):
        self.ast[ctx] = ast.ComponentRef(
            name=ctx.getText()
        )

    def exitEquation_function(self, ctx):
        # TODO, add function ast
        self.ast[ctx] = ctx.getText()

    def exitEquation_when(self, ctx):
        # TODO, add when ast
        self.ast[ctx] = ctx.getText()

    # COMPONENTS ===========================================================

    def exitElement_list(self, ctx):
        self.ast[ctx] = [self.ast[e] for e in ctx.element()]

    def exitElement(self, ctx):
        self.ast[ctx] = self.ast[ctx.elem]

    def exitImport_clause(self, ctx):
        self.ast[ctx] = 'TODO'

    def exitExtends_clause(self, ctx):
        self.ast[ctx] = 'TODO'

    def exitRegular_element(self, ctx):
        self.ast[ctx] = self.ast[ctx.comp_elem]

    def exitReplaceable_element(self, ctx):
        self.ast[ctx] = 'TODO'

    def enterComponent_clause(self, ctx):
        if ctx.array_subscripts() is not None:
            dimensions = [int(s) for s in ctx.array_subscripts().subscript().getText()]
        else:
            dimensions = [1]
        prefixes = ctx.type_prefix().getText().split(' ')
        if prefixes[0] == '':
            prefixes = []
        self.ast[ctx] = ast.ComponentClause(
            prefixes=prefixes,
            type=ctx.type_specifier().getText(),
            dimensions=dimensions
        )
        self.comp_clause = self.ast[ctx]

    def enterComponent_declaration(self, ctx):
        sym = ast.Symbol(order = self.sym_count, start=ast.Primary(value=0.0))
        self.sym_count += 1
        self.ast[ctx] = sym
        self.symbol_node = sym

    def exitComponent_declaration(self, ctx):
        self.ast[ctx].comment = self.ast[ctx.comment()]

    def enterDeclaration(self, ctx):
        sym = self.symbol_node
        dimensions = None
        if ctx.array_subscripts() is not None:
            dimensions = [int(s) for s in ctx.array_subscripts().subscript().getText()]
        elif self.comp_clause.dimensions is not None:
            dimensions = self.comp_clause.dimensions
        sym.name = ctx.IDENT().getText()
        sym.dimensions = dimensions
        sym.prefixes = self.comp_clause.prefixes
        sym.type = self.comp_clause.type
        if sym.name in self.class_node.symbols:
            raise IOError(sym.name, 'already defined')
        self.class_node.symbols[sym.name] = sym
        self.symbol_node = sym

    def exitElement_modification(self, ctx):
        sym = self.symbol_node
        if ctx.name().getText() == 'start':
            sym.start = self.ast[ctx.modification().expression()]

    def exitModification_assignment(self, ctx):
        sym = self.symbol_node
        sym.start = self.ast[ctx.expression()]

    # COMMENTS ==============================================================

    def exitComment(self, ctx):
        # TODO handle annotation
        self.ast[ctx] = self.ast[ctx.string_comment()]

    def exitString_comment(self, ctx):
        self.ast[ctx] = ctx.getText()[1:-1]


# UTILITY FUNCTIONS ========================================================

def parse(text):
    input_stream = antlr4.InputStream(text)
    lexer = ModelicaLexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = ModelicaParser(stream)
    parse_tree = parser.stored_definition()
    ast_listener = ASTListener()
    parse_walker = antlr4.ParseTreeWalker()
    parse_walker.walk(ast_listener, parse_tree)
    ast_tree = ast_listener.ast_result
    return ast_tree
