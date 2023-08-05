from __future__ import absolute_import
from pangea import native
import django.db.models as dj
import django.db.models.functions as dj_func

from pangea.django import build_dj_expression


class ASTBase(object):
    def to_django_expression(self, prefix):
        return NotImplementedError()

    def evaluate_native_expression(self, obj):
        raise NotImplementedError()

    def django(self):
        return self.to_django_expression(u'')

    def __call__(self, obj):
        return native.evaluate(self, obj)


class Case(ASTBase):
    def __init__(self, *branches, **kwargs):
        self.default_branch = None
        self.django_output_field = kwargs.pop('django_output_field', None)
        for b in branches:
            if b[0] == Else:
                print self.default_branch
                self.default_branch = b
                break

        self.branches = branches

    def to_django_expression(self, prefix):
        # build branches
        branches = []
        for b in self.branches:
            if b != self.default_branch:
                branches.append(build_case_branch(b, prefix))
        if self.default_branch:
            return dj.Case(*branches, default=build_dj_expression(self.default_branch[1], prefix),
                           output_field=self.django_output_field)
        else:
            return dj.Case(*branches, output_field=self.django_output_field)

    def evaluate_native_expression(self, obj):
        for predicate, result in self.branches:
            if native.evaluate(predicate, obj):
                return native.evaluate(result, obj)
        raise ValueError("All branches failed in case statement!")

def build_case_branch(branch, prefix):
    predicate = branch[0]
    if not isinstance(predicate, When):
        raise ValueError("Syntax Error")

    return dj.When(condition=dj.Q(**branch[0].params),
                   then=build_dj_expression(branch[1], prefix))

class Property(ASTBase):
    def __init__(self, prop_name):
        self.prop_name = prop_name

    def to_django_expression(self, prefix):
        return dj.F(prefix + self.prop_name)

    def evaluate_native_expression(self, obj):
        return getattr(obj, self.prop_name)


class Concat(ASTBase):
    def __init__(self, concat_list):
        self.concat_list = concat_list

    def to_django_expression(self, prefix):

       return dj.functions.Concat(*map(lambda e: build_dj_expression(e, prefix), self.concat_list))

    def evaluate_native_expression(self, obj):
        args = [native.evaluate(expr, obj) for expr in self.concat_list]
        return u''.join(args)


class When(ASTBase):
    def __init__(self, **kwargs):
        self.params = kwargs

    def to_django_expression(self, prefix):
        raise ValueError()

    def evaluate_native_expression(self, obj):
        for arg_name, arg_value in self.params.items():
            if not native.predicate_check(arg_name, arg_value, obj):
                return False
        return True

class Else(object):
    pass