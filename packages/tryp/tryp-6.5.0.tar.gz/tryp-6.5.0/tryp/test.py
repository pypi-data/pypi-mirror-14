from macropy.case_classes import macros, case


@case
class Foo(a | 5, b | 6):
    self.c = a + b

__all__ = ()
