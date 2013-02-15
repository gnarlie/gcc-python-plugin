#   Copyright 2011, 2012 David Malcolm <dmalcolm@redhat.com>
#   Copyright 2011, 2012 Red Hat, Inc.
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

from cpybuilder import *
from wrapperbuilder import PyGccWrapperTypeObject

cu = CompilationUnit()
cu.add_include('gcc-python.h')
cu.add_include('gcc-python-wrappers.h')
cu.add_include('gcc-plugin.h')
cu.add_include("gcc-c-api/gcc-variable.h")

modinit_preinit = ''
modinit_postinit = ''

def generate_variable():
    global modinit_preinit
    global modinit_postinit

    getsettable = PyGetSetDefTable('gcc_Variable_getset_table', [])
    def add_simple_getter(name, c_expression, doc):
        getsettable.add_gsdef(name,
                              cu.add_simple_getter('gcc_Variable_get_%s' % name,
                                                   'PyGccVariable',
                                                   c_expression),
                              None,
                              doc)

    add_simple_getter('decl',
                      'gcc_python_make_wrapper_tree(gcc_variable_get_decl(self->var))',
                      'The declaration of this variable, as a gcc.Tree')

    cu.add_defn(getsettable.c_defn())
    
    pytype = PyGccWrapperTypeObject(identifier = 'gcc_Variable_TypeObj',
                          localname = 'Variable',
                          tp_name = 'gcc.Variable',
                          tp_dealloc = 'gcc_python_wrapper_dealloc',
                          struct_name = 'PyGccVariable',
                          tp_new = 'PyType_GenericNew',
                          tp_getset = getsettable.identifier,
                          #tp_repr = '(reprfunc)gcc_Variable_repr',
                          #tp_str = '(reprfunc)gcc_Variable_repr',
                          )
    cu.add_defn(pytype.c_defn())
    modinit_preinit += pytype.c_invoke_type_ready()
    modinit_postinit += pytype.c_invoke_add_to_module()
    
generate_variable()



cu.add_defn("""
int autogenerated_variable_init_types(void)
{
""" + modinit_preinit + """
    return 1;

error:
    return 0;
}
""")

cu.add_defn("""
void autogenerated_variable_add_types(PyObject *m)
{
""" + modinit_postinit + """
}
""")

print(cu.as_str())
