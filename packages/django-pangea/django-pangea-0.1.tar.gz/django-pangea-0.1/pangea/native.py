

def evaluate(expr, with_obj):
    from pangea.AST import ASTBase
    if isinstance(expr, ASTBase):
        return expr.evaluate_native_expression(with_obj)

    # if not an AST node, then we pass the value on
    return expr


class _Predicate(object):
    @staticmethod
    def EQ(a,b):
        return a == b

    @staticmethod
    def GTE(a,b):
        return a >= b

    @staticmethod
    def LTE(a,b):
        return a <= b

_special_keys = {
    'eq': _Predicate.EQ,
    'gte': _Predicate.GTE,
    'lte': _Predicate.LTE
}
def get_obj_value(arg_name, obj):
    arg_levels = arg_name.split('__')
    if arg_levels[-1] in _special_keys:
        predicate = _special_keys[arg_levels[-1]]
        arg_levels = arg_levels[:-1]
    else:
        predicate = _Predicate.EQ

    current_obj = obj
    for arg in arg_levels:
        current_obj = getattr(current_obj, arg)

    return current_obj, predicate




def predicate_check(arg_name, arg_value, obj):
    #
    #
    obj_value, check = get_obj_value(arg_name, obj)
    return check(obj_value, arg_value)