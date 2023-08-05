"""Pipeline module.

This module provides a fluent api around mongo's aggregation pipeline.

"""

from bson.son import SON

from rcquerybuilder.builder import Expr
from rcquerybuilder.builder import _get_query


def expr():
    """Creates a new ``PipelineExpr``. Useful for chaining.

    Returns:
        PipelineExpr: The created ``PipelineExpr``.
    """
    return PipelineExpr()


class PipelineExpr(Expr):
    def __init__(self):
        super(PipelineExpr, self).__init__()
        self.query = SON()

    def operator(self, operator, value_or_expression):
        if isinstance(value_or_expression, (list, tuple)):
            expression = [_get_query(voe)
                          for voe in value_or_expression]
        else:
            expression = _get_query(value_or_expression)

        super(PipelineExpr, self).operator(operator, expression)

        return self

    def multiply(self, *expression):
        return self.operator('$multiply', expression)

    def abs(self, expression):
        return self.operator('$abs', expression)

    def add(self, expression):
        return self.operator('$add', expression)

    def ceil(self, expression):
        return self.operator('$ceil', expression)

    def divide(self, *expression):
        return self.operator('$divide', expression)

    def floor(self, expression):
        return self.operator('$floor', expression)

    def ln(self, expression):
        return self.operator('$ln', expression)

    def log(self, expression):
        return self.operator('$log', expression)

    def mod(self, expression):
        return self.operator('$mod', expression)

    def sqrt(self, expression):
        return self.operator('$sqrt', expression)

    def subtract(self, expression):
        return self.operator('$subtract', expression)

    def concat(self, *expressions):
        return self.operator('$concat', expressions)

    def substr(self, string, start, length):
        return self.operator('$substr', [string, start, length])

    def to_lower(self, expression):
        return self.operator('$toLower', expression)

    def to_upper(self, expression):
        return self.operator('$toUpper', expression)

    def strcasecmp(self, field1, field2):
        return self.operator('$strcasecmp', [field1, field2])

    def array_elem_at(self, array_or_field, index):
        return self.operator('$arrayElemAt', [array_or_field, int(index)])

    def concat_arrays(self, *arrays):
        return self.operator('$concatArrays', arrays)

    def filter(self, input, name, cond):
        return self.operator('$filter', {
            'input': input,
            'as': name,
            'cond': _get_query(cond)
        })

    def is_array(self, expression):
        return self.operator('$isArray', expression)

    def day_of_year(self, expression):
        return self.operator('$dayOfYear', expression)

    def day_of_month(self, expression):
        return self.operator('$dayOfMonth', expression)

    def year(self, expression):
        return self.operator('$year', expression)

    def month(self, expression):
        return self.operator('$month', expression)

    def week(self, expression):
        return self.operator('$week', expression)

    def hour(self, expression):
        return self.operator('$hour', expression)

    def minute(self, expression):
        return self.operator('$minute', expression)

    def second(self, expression):
        return self.operator('$second', expression)

    def millisecond(self, expression):
        return self.operator('$millisecond', expression)

    def date_to_string(self, date, date_format='%Y-%m-%d %H:%M:%S'):
        return self.operator('$dateToString', {
            'format': date_format,
            'date': date
        })

    def cond(self, if_cond, then_cond, else_cond):
        return self.operator('$cond', {
            'if': _get_query(if_cond),
            'then': _get_query(then_cond),
            'else': _get_query(else_cond)
        })

    def if_null(self, expression, replacement):
        return self.operator('$ifNull', [expression, replacement])

    def set(self, value, atomic=None):
        self._requires_current_field()
        self.query[self.current_field] = _get_query(value)

        return self

    @classmethod
    def expr(cls):
        return cls()


class PipelineStage(PipelineExpr):
    key = None

    def build(self):
        return {self.key: self.query}


class MatchStage(PipelineStage):
    key = '$match'


class ProjectStage(PipelineStage):
    key = '$project'

    def id(self, show=True):
        return self.field('_id').equals(int(show))


class GroupStage(PipelineStage):
    key = '$group'

    def id(self, *args, **kwargs):
        return self.field('_id').equals(
                _get_query(
                        args[0] if args else kwargs
                )
        )

    def group_all(self):
        self.current_field = '_id'
        self.query['_id'] = None

        return self

    def first(self, expression):
        return self.operator('$first', expression)

    def last(self, expression):
        return self.operator('$last', expression)

    def push(self, expression):
        return self.operator('$push', expression)

    def add_to_set(self, expression):
        return self.operator('$addToSet', expression)

    def avg(self, expression):
        return self.operator('$avg', expression)

    def sum(self, expression):
        return self.operator('$sum', expression)

    def max(self, expression):
        return self.operator('$max', expression)

    def min(self, expression):
        return self.operator('$min', expression)

    def build(self):
        if '_id' not in self.query:
            self.group_all()
        return super(GroupStage, self).build()


class SortStage(object):
    key = '$sort'

    def __init__(self):
        self._sorts = SON()

    def by(self, *args):
        if not args:
            raise RuntimeError('This method needs at least one argument')

        if isinstance(args[0], list):
            return self.by(*args[0])

        if isinstance(args[0], tuple):
            sort_by = SON(args)
        else:
            raise ValueError('The arguments to this method must be tuples')

        self._sorts.update(sort_by)

        return self

    def sort(self, field, direction=1):
        if isinstance(direction, basestring):
            if direction.lower() == 'asc':
                direction = 1
            else:
                direction = -1
        self._sorts[field] = direction

        return self

    def build(self):
        return {self.key: self._sorts}
