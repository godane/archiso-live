#!/usr/bin/env python

# byte-compile python modules in the given directory tree

import compileall
import sys

compileall.compile_dir(sys.argv[1], force=1)
