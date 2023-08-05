from __future__ import (
    absolute_import, division, generators, nested_scopes, print_function,
    unicode_literals, with_statement
)

import sys
from toolz import pipe
from pathlt import transforms as t


def main():
    transforms = [
        t.parentdir_expand,
        t.unambiguous_path,
        t.physical_path
    ]
    print(pipe(sys.argv[1], *transforms))

if __name__ == '__main__':
    main()
