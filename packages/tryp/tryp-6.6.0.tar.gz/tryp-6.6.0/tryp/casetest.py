from macropy.experimental.tco import macros, tco


@tco
def rec(z, n):
    if n == 0:
        return z
    else:
        return rec(z * n, n - 1)

__all__ = ()
