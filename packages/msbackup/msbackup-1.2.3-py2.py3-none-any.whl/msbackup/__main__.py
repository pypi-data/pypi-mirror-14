# -*- coding: utf-8 -*-
"""Main module of 'msbackup' package."""

import sys

try:
    from msbackup.msbackup import main
except ImportError:
    from .msbackup import main


sys.exit(main())
