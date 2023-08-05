#!/usr/bin/python

'''Produce a dependency ordering of a list of directories by reading
dependency information from files named `requires`, `provides`, and
`required_by` located in the `.deps` directory of each target
directory.

For example, given this directory structure:

    task1/
      .deps/
        requires
    task2/
      .deps/
        provides
    task3/
      .deps/
        required_by

If `task1/.deps/requires` contains `task2` and
`task3/.deps/required_by` contains `task1` then `depdirs` would
produce the ordering:

    task2 task3 task1

If `task2/.deps/provides` contains `vpn`, then `task1/.deps/requires` could
contain `vpn` instead of `task1` and the ordering would be the same.

**NOTE**

- The ordering between items with no dependencies is indeterminate.
  The ordering `task3 task2 task1` would also be valid for the above
  example.

- If multiple directories `provide` the same resource, the first
  directory discovered will be used to fulfill that requirement in all
  cases (in other words, *which* directory is used is consistent but
  indeterminate).

'''

__author__ = 'Lars Kellogg-Stedman <lars@oddbit.com>'
__version__ = '0.1'

import sys
import argparse
import logging

# the following allows us to use 'pydoc' even when missing
# the requried modules.  this also allows us to import __version__
# in setup.py.
try:
    import toposort
    has_toposort = True
except ImportError:
    has_toposort = False

try:
    from pathlib2 import Path
    has_path = True
except ImportError:
    Path = None
    has_path = False

LOG = logging.getLogger(__name__)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--verbose', '-v',
                   action='store_const',
                   const='INFO',
                   dest='loglevel')
    p.add_argument('--debug', '-d',
                   action='store_const',
                   const='DEBUG',
                   dest='loglevel')
    p.add_argument('dirs', nargs='*')
    p.set_defaults(loglevel='WARNING')
    return p.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=args.loglevel)

    if has_path is False or has_toposort is False:
        LOG.error('Your python environment is missing required modules')
        sys.exit(1)

    dirs = {}

    for item in (Path(dir) for dir in args.dirs):
        if item.name.startswith('.'):
            continue

        if not item.is_dir():
            LOG.warn('skipping %s (not a directory)', item)
            continue

        dirs[item] = {
            'requires': [],
            'required_by': [],
            'provides': [],
        }

        this = dirs[item]

        for reqtype in this.keys():
            LOG.debug('check %s %s', item.name, reqtype)
            try:
                with (item / '.deps' / reqtype).open() as fd:
                    LOG.debug('reading %s deps for %s', reqtype, item.name)
                    this[reqtype] = fd.read().splitlines()
            except IOError:
                continue

    # generated provided_by dictionary
    provided_by = {}
    for k, v in dirs.items():
        provided_by[k.name] = k
        for provide in v['provides']:
            provided_by[provide] = k

    order = {}
    for k, v in dirs.items():
        order.setdefault(k, set())
        for req in v['requires']:
            LOG.debug('%s requires %s (provided by %s)',
                      k, req, provided_by[req])
            order[k].add(provided_by[req])

        for req in v['required_by']:
            LOG.debug('%s is required by %s (via %s)',
                      k, provided_by[req], req)
            order.setdefault(provided_by[req], set()).add(k)

    order = [item for stage in toposort.toposort(order)
             for item in stage]

    print ' '.join(str(x) for x in order)

if __name__ == '__main__':
    main()
