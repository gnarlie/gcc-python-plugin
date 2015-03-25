# -*- coding: utf-8 -*-
#   Copyright 2012 David Malcolm <dmalcolm@redhat.com>
#   Copyright 2012 Red Hat, Inc.
#
#   This is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see
#   <http://www.gnu.org/licenses/>.

# Demonstration of how to look up an enum's declaration from Python

import gcc
import sys

class TestPass(gcc.GimplePass):
    def execute(self, fn):
        print('fn: %s' % fn)
        print('return: %r' % fn.decl.type.type)
        enum_type = fn.decl.type.type
        for val in fn.decl.type.type.values:
            print('    str(val): %s' % str(val))
            print('    val.type: %s' % val.type)

test_pass = TestPass(name='test-pass')
test_pass.register_after('cfg')

