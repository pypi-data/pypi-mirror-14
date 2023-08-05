"""
Helper script for starting up bolts and spouts.
"""

import argparse
import importlib
import os
import sys


def main():
    """main entry point for Python bolts and spouts"""
    parser = argparse.ArgumentParser(description='Run a bolt/spout class',
                                     epilog='This is internal to streamparse '
                                            'and is used to run spout and bolt '
                                            'classes via ``python -m '
                                            'streamparse.run <class name>``.')
    parser.add_argument('target_class', help='The bolt/spout class to start.')
    args = parser.parse_args()
    # Add current directory to sys.path so imports will work
    sys.path.append(os.getcwd())
    # Import module
    mod_name, cls_name = args.target_class.rsplit('.', 1)
    mod = importlib.import_module(mod_name)
    # Get class from module and run it
    cls = getattr(mod, cls_name)
    cls().run()


if __name__ == '__main__':
    main()
