from __future__ import absolute_import
import django.db.models as dj



def build_dj_expression(expr, prefix):
    from pangea.AST import ASTBase
    if isinstance(expr, str) or isinstance(expr, unicode):
        return dj.Value(expr)

    if isinstance(expr, ASTBase):
        return expr.to_django_expression(prefix)

    raise ValueError("Unkown value inside Pangea expression: %r" % expr)
