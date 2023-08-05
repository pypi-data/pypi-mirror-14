from pangea.AST import Case, Property, Concat, When


class Pangea(object):
    """
    singleton to help with building Pangea ADTS
    """

    @classmethod
    def Case(cls, *args, **kwargs):
        return Case(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return Property(*args, **kwargs)

    def Concat(self, *args):
        return Concat(args)

    def When(self, **kwargs):
        return When(**kwargs)

    Else = AST.Else

P = Pangea()
