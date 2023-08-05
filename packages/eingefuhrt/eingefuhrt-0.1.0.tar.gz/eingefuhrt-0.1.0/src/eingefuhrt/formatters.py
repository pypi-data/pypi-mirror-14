from __future__ import absolute_import

import re

from eingefuhrt.constants import ALWAYS_FIRST
from eingefuhrt.constants import STANDARD_MODULES


def _generate_module_matching(module_list):
    regex = re.compile('^({})'.format('|'.join(re.escape(mod) for mod in module_list)))
    return lambda name: regex.match(name) is not None

is_always_first = _generate_module_matching(ALWAYS_FIRST)
is_standard_module = _generate_module_matching(STANDARD_MODULES)

del _generate_module_matching  # People have a tendency to import thing they shouldn't


def hacking_import_to_string(imp):
    if imp.name == imp.path:  # Example: import foo.bar
        return 'import {}'.format(imp.path)

    assert '.' not in imp.name, "'from foo import bar.baz' is impossible"

    if not imp.path.endswith(imp.name):  # Examples: import foo as bar; or: import foo.bar as baz
        return 'import {imp.path} as {imp.name}'.format(imp=imp)

    module, sep, value = imp.path.rpartition('.')
    if module == '':  # Example: from . import foo
        assert sep == '.'
        module = sep

    assert value == imp.name
    return 'from {module} import {value}'.format(module=module, value=value)


def hacking_format_import_block(block):
    block = sorted(block, key=lambda i: i.path.lower())
    return '\n'.join(hacking_import_to_string(i) for i in block)


def hacking(import_list):
    """Format imports as in the OpenStack Style Guidelines

    <http://docs.openstack.org/developer/hacking/>
    """
    import_list = set(import_list)

    always_first = set(imp for imp in import_list if is_always_first(imp.path))
    standard_modules = set(imp for imp in import_list if is_standard_module(imp.path))
    third_party = import_list - standard_modules - always_first

    code_blocks = [always_first, standard_modules, third_party]

    formatted_blocks = (hacking_format_import_block(b) for b in code_blocks)
    formatted_blocks = [b for b in formatted_blocks if b]

    return '\n\n'.join(formatted_blocks) + '\n'
