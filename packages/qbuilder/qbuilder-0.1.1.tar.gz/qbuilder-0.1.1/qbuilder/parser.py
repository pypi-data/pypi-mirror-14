import operator
import ast
from ast import Call, Str


def in_(lhs, rhs):
    return lhs << (rhs)


def between_(lhs, rhs):
    return lhs.between(rhs[0], rhs[1])


def contains_(lhs, rhs):
    return lhs.contains(rhs)


def contains_any_(lhs, rhs):
    return lhs.contains_any(rhs)


def contains_all_(lhs, rhs):
    return lhs.contains_all(rhs)


def startswith_(lhs, rhs):
    return lhs.startswith(rhs)


OPERATORS = {
    'EQ': operator.eq,
    'NE': operator.ne,
    'GT': operator.gt,
    'GE': operator.ge,
    'LT': operator.lt,
    'LE': operator.le,
    'CONTAINS': contains_,
    'CONTAINS_ANY': contains_any_,
    'CONTAINS_ALL': contains_all_,
    'STARTSWITH': startswith_,
    'IN': in_,
    'BETWEEN': between_
}

MULTI_VALUE = ('IN', 'BETWEEN', 'CONTAINS_ANY')

GROUP = {
    'AND': operator.and_,
    'OR': operator.or_
}

# stack = []


def travel_node(node, Model):
    if isinstance(node, Call):
        if node.func.id in OPERATORS:
            if len(node.args) < 2 or not isinstance(node.args[0], Str):
                raise Exception(
                    'First Argument of '
                    '{} should be a string'.format(node.func.id))
            op = OPERATORS[node.func.id]
            field = Model._meta.fields[node.args[0].s]
            if node.func.id in MULTI_VALUE:
                value = [ast.literal_eval(arg) for arg in node.args[1:]]
            else:
                value = ast.literal_eval(node.args[1])
            return op(field, value)
        elif node.func.id in GROUP:
            exp = []
            for arg in node.args:
                exp.append(travel_node(arg))
            return reduce(GROUP[node.func.id], exp)
        else:
            raise Exception(
                'Invalid Query. {} '
                'not supported.'.format(node.func.id))
