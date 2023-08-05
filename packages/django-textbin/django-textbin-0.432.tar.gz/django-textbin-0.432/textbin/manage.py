#!/usr/bin/env python
import os
import sys
import imp


def main():
    try:
        # Check - is app installed?
        imp.find_module('textbin.settings')
    except ImportError:
        # Used if package is not installed
        # to prevent ImportError: No module named textbin.settings
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "textbin.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
