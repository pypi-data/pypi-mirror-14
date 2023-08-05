from __future__ import unicode_literals, print_function
import re, itertools, operator, ast
from pypeg2 import *

# This is needed because using a plain 'not' will remove it from the ast when
# parsed.
RE_NOT = re.compile('not')

# And this is needed because otherwise "not" will be usable as an Indentifier.
K('not')


class LangInstance:
	pass

def create_lang_instance(var_map = None):
	"""
	>>> lang_instance = create_lang_instance()
	>>> lang_instance.aml_evaluate(lang_instance.aml_compile('1 = 1'))
	True
	>>> li = create_lang_instance()
	>>> c = li.aml_compile
	>>> e = li.aml_evaluate
	>>> p = li.aml_translate_python
	>>> s = li.aml_translate_sql
	>>> u = li.aml_suggest
	>>> e(c('1 = 0'))
	False
	>>> e(c('"1" = "1"'))
	True
	>>> e(c('(1=1)'))
	True
	>>> e(c('1 > 1'))
	False
	>>> e(c('not 1 > 1'))
	True
	>>> e(c('1 != 1'))
	False
	>>> e(c('-2 = -2'))
	True
	>>> eval(p(c('-2 = -2')))
	True
	>>> eval(p(c('null = null')))
	True
	>>> eval(p(c('1 = null')))
	False
	>>> e(c('"foo" = "foo"'))
	True
	>>> e(c('"foo" = \\'foo\\''))
	True
	>>> e(c('"fo\\'o" = "fo\\'o"'))
	True
	>>> e(c("'foo'" + '=' + '"foo"'))
	True
	>>> li = create_lang_instance({'foo' : 1});
	>>> c = li.aml_compile
	>>> e = li.aml_evaluate
	>>> e(c('foo = 1'))
	True
	>>> li = create_lang_instance({'foo' : 1.00})
	>>> c = li.aml_compile
	>>> e = li.aml_evaluate
	>>> e(c('foo = 1'))
	True
	>>> li = create_lang_instance({'foo' : 2.24})
	>>> c = li.aml_compile
	>>> e = li.aml_evaluate
	>>> e(c('foo = 2.24'))
	True
	>>> li = create_lang_instance({'foo' : 'foo'})
	>>> c = li.aml_compile
	>>> e = li.aml_evaluate
	>>> e(c('foo = "foo"'))
	True
	>>> li = create_lang_instance()
	>>> c = li.aml_compile
	>>> p = li.aml_translate_python
	>>> s = li.aml_translate_sql
	>>> s(c('null = null'))
	u'null is null'
	>>> p(c('null = null'))
	u'None == None'
	>>> s(c('null != null'))
	u'null is not null'
	>>> p(c('null != null'))
	u'None != None'
	>>> s(c('5 != 3'))
	u'5 <> 3'
	>>> p(c('5 != 3'))
	u'5 != 3'
	>>> li = create_lang_instance({'foo' : 'bar', 'fo2' : 'ba2'})
	>>> c = li.aml_compile
	>>> p = li.aml_translate_python
	>>> e = li.aml_evaluate
	>>> u = li.aml_suggest
	>>> u('1 = fo')
	[u'fo2', u'foo']
	>>> u('1 = FO')
	[u'fo2', u'foo']
	>>> p(c('null = null'))
	u'None == None'
	>>> e(c('foo = "bar"'))
	True
	>>> e(c('fo2 = "ba2"'))
	True
	>>> c('abc = 1')
	Traceback (most recent call last):
	SyntaxError: expecting one of [<class '__init__.BooleanOperationSimple'>, (u'(', <class '__init__.Expression'>, u')')] (line 1)
	"""

	def py_bool_to_lit(py_bool):
		return parse( 'true' if py_bool else 'false', BooleanLiteral)

	if not var_map:
		class Identifier(str):
			grammar = re.compile(r'$a') # This will match nothing.
	else:
		class Identifier(Keyword):
			grammar = Enum(*[K(v) for v in var_map.iterkeys()])
		
	class StringLiteral(str):

		def __new__(cls, s):
			return super(StringLiteral, cls).__new__(cls, ast.literal_eval(s))

		grammar = [re.compile(r'"[^\\\n\r]+?"'), re.compile(r"'[^\\\n\r]+?'")]

	class IntegerLiteral(int):
		grammar = re.compile(r'-?\d+')

	class FloatLiteral(float):
		grammar = re.compile(r'-?\d+.\d+')

	class BooleanLiteral(Keyword):
		grammar = Enum(K('true'), K('false'))

	class NullLiteral(Keyword):
		grammar = Enum(K('null'))

	Comparable = [NullLiteral, FloatLiteral, IntegerLiteral, 
									StringLiteral, Identifier]


	class ComparisonOperator(str):
		grammar = re.compile(r'=|>|<|!=|>=|<=')

	class BooleanFunctionName(Keyword):
		grammar = Enum(K('and'), K('or'))

	class ComparisonOperation(List):
		pass

	ComparisonOperation.grammar = (
			Comparable,
			blank,
			attr('comp_op', ComparisonOperator),
			blank,
			Comparable,
	)

	class BooleanOperationSimple(List):
# The flag() pypeg2 function works great when parsing but does not work when
# composing (the flag gets output whether it was in the source text or not. So
# a workaround is this:
		grammar = (
				attr('negated', optional(RE_NOT)),
				ComparisonOperation,
		)

	class BooleanOperation(List):
		pass

	BooleanOperation.grammar = (
			BooleanOperationSimple,
			maybe_some(
				blank,
				BooleanFunctionName,
				blank,
				BooleanOperationSimple,
			),
	)

	class Expression(List):
		pass

	Expression.grammar = (
			[BooleanOperationSimple, ('(', Expression, ')')],
			maybe_some(
				blank,
				BooleanFunctionName,
				blank,
				[BooleanOperationSimple, ('(', Expression, ')')],
			),
	)

	def eval_node(node):
		en = lambda n: eval_node(n)
		if isinstance(node, Identifier):
			return var_map[node]
		elif isinstance(node, StringLiteral):
			return node
		elif isinstance(node, IntegerLiteral):
			return node
		elif isinstance(node, FloatLiteral):
			return node
		elif isinstance(node, BooleanLiteral):
			if node == 'true':
				return True
			elif node == 'false':
				return False
		elif isinstance(node, NullLiteral):
			return None
		elif isinstance(node, ComparisonOperation):
			opa, opb = node[0:2]
			if node.comp_op == '=':
				return en(opa) == en(opb)
			elif node.comp_op == '>':
				return en(opa) >  en(opb)
			elif node.comp_op == '<':
				return en(opa) <  en(opb)
			elif node.comp_op == '!=':
				return en(opa) != en(opb)
			elif node.comp_op == '>=':
				return en(opa) >= en(opb)
			elif node.comp_op == '<=':
				return en(opa) <= en(opb)
		elif isinstance(node, BooleanOperationSimple):
			a = en(node[0])
			if node.negated:
				a = not a
			return a
		elif isinstance(node, BooleanOperation):
			if len(node) == 1:
				return en(node[0])

			fn_map = {
					'and': lambda a,b: a and b,
					'or':  lambda a,b: a or  b,
			}

			def simple_eval(tr):
				return py_bool_to_lit(fn_map[tr[1]]( en(tr[0]), en(tr[2]))) 
						

			for fname in ['and', 'or']:
				for i in xrange(1, len(node), 2):
					if node[i] == fname:
						new_self = (
							node[:i-1]
							+ [simple_eval(node[i-1:i+2])]
							+ node[i+2:]
						)
						return en(BooleanOperation(new_self))
		elif isinstance(node, Expression):
			def iter_over_relevant():
				for eli, el in enumerate(node):
					if eli % 2 == 0:
						yield eli, el

			if all(
					isinstance(el, BooleanOperationSimple) 
						or
					isinstance(el, BooleanLiteral) 
					for eli, el in iter_over_relevant()
			):
				res = en(BooleanOperation(node))
				return res
			else:
				for eli, el in iter_over_relevant():
					if isinstance(el, Expression):
						new_self = (
								node[:eli]
								+ [py_bool_to_lit(en(el))]
								+ node[eli+1:]
						)
						return en(Expression(new_self))

	def compose_node_to_python(node):
		return compose(node)

	def compose_node_to_sql(node):
		return compose(node)

	def aml_compile(source):
		return parse(source, Expression)

	def aml_evaluate(aml_c):
		result = eval_node(aml_c)
		return result

	def aml_translate_python(aml_c):

		def comp_op_compose(self, *args, **kwargs):
			if self == '=':
				return '=='
			else:
				return self

		def null_compose(self, *args, **kwargs):
			return 'None'

		def string_compose(self, *args, **kwargs):
			return '"' + self.replace('"', r'\"') + '"'

		ComparisonOperator.compose = comp_op_compose
		NullLiteral.compose = null_compose
		StringLiteral.compose = string_compose

		result = compose_node_to_python(aml_c)

		delattr(ComparisonOperator, 'compose')
		delattr(NullLiteral, 'compose')
		delattr(StringLiteral, 'compose')

		return result

	def aml_translate_sql(aml_c):

		def comp_op_compose(self, *args, **kwargs):
			if self == '!=':
				return '<>'
			else:
				return self

		def comp_op_compose(self, *args, **kwargs):
			if self == '!=':
				return '<>'
			else:
				return self

		def null_compose(self, *args, **kwargs):
			return 'null'

		def string_compose(self, *args, **kwargs):
			return "'" + self.replace("'", "''") + "'"

		def comp_operation_compose(self, *args, **kwargs):
			if (
					(
						isinstance(self[0], NullLiteral) 
							or
						isinstance(self[1], NullLiteral)
					)
						and
					(
						self.comp_op in ('=', '!=')
					)
			):

				if self.comp_op == '=':
					middle = 'is'
				else:
					middle = 'is not'

			else:
				middle = compose(self.comp_op)

			return ' '.join([
				compose(self[0]),
				middle,
				compose(self[1]),
			])


		ComparisonOperator.compose = comp_op_compose
		NullLiteral.compose = null_compose
		ComparisonOperation.compose = comp_operation_compose
		StringLiteral.compose = string_compose

		result = compose_node_to_sql(aml_c)

		delattr(ComparisonOperator, 'compose')
		delattr(NullLiteral, 'compose')
		delattr(ComparisonOperation, 'compose')
		delattr(StringLiteral, 'compose')

		return result

	def aml_suggest(source):
		suggestions = [ ]
		if var_map:
			if not source:
				suggestions = list(var_map.iterkeys())
			else:
				split = [el for el in re.split(r'(?m)\s+', source) if el]
				if split:
					for candidate in var_map.iterkeys():
						if candidate.lower().startswith(split[-1].lower()):
							suggestions.append(candidate)
		suggestions.sort()
		return suggestions

	lang_instance = LangInstance()

	lang_instance.aml_compile = aml_compile
	lang_instance.aml_evaluate = aml_evaluate
	lang_instance.aml_translate_python = aml_translate_python
	lang_instance.aml_translate_sql = aml_translate_sql
	lang_instance.aml_suggest = aml_suggest

	return lang_instance

