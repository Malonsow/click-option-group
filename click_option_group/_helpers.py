# -*- coding: utf-8 -*-

from typing import List, Tuple

import collections.abc as abc
import random
import string

import click


FAKE_OPT_NAME_LEN = 30


def get_callback_and_params(func) -> Tuple[abc.Callable, List[click.Option]]:
    """Returns callback function and its parameters list

    :param func: decorated function or click Command
    :return: (callback, params)
    """
    if isinstance(func, click.Command):
        params = func.params
        func = func.callback
    else:
        params = getattr(func, '__click_params__', [])

    func = resolve_wrappers(func)
    return func, params


def get_fake_option_name(name_len: int = FAKE_OPT_NAME_LEN, prefix: str = 'fake'):
    return f'--{prefix}-' + ''.join(random.choices(string.ascii_lowercase, k=name_len))


def raise_mixing_decorators_error(wrong_option: click.Option, callback: abc.Callable):
    error_hint = wrong_option.opts or [wrong_option.name]

    raise TypeError((
        "Grouped options must not be mixed with regular parameters while adding by decorator. "
        f"Check decorator position for {error_hint} option in '{callback.__name__}'."
    ))


def resolve_wrappers(f):
    """Get the underlying function behind any level of function wrappers."""
    return resolve_wrappers(f.__wrapped__) if hasattr(f, "__wrapped__") else f
