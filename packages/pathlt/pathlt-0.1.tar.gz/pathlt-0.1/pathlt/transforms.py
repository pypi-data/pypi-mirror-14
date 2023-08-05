from __future__ import (
    absolute_import, division, generators, nested_scopes, print_function,
    unicode_literals, with_statement
)

import re
import os


def parentdir_expand(path):
    """ Expand parent directory traversal

  Allow the user to specify ..<n> and expand to a recognized directory path.
  for example ..5 would expand to ../../../../..

  :param path: str
  :return: str
  """
    if path[0:2] != '..':
        return path
    else:
        parentdir_match = r'\.\.(\d*){0}(.*)'.format(os.path.sep)
        matches = re.match(parentdir_match, path)
        expand_depth = matches.group(1) or 1
        extra_path = matches.group(2)

        parent_path = os.path.join(*['..'] * int(expand_depth))
        return os.path.join(parent_path, extra_path)


def physical_path(path, transform_callback=None):
    """ Return the physical path if path ends with //

    :param path: str
    :return: str
    """
    transform_callback = transform_callback or os.path.realpath

    if re.match(r'.*(?<!\\)//', path):
        return transform_callback(path)
    else:
        return path
