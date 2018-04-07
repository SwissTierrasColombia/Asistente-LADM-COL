Documentation for the Code
**************************

.. automodule:: testpypkg


Modulo test1 -- auto members
=============================

This is something I want to say that is not in the docstring.

.. automodule:: testpypkg.test1
   :members:

module2 -- explicit members
=============================

This is something I want to say that is not in the docstring.

.. automodule:: testpypkg.module2
   :members: public_fn_with_sphinxy_docstring, _private_fn_with_docstring,public_fn_without_docstring

.. autoclass:: testpypkg.module2.MyPublicClass
   :members: get_foobar, _get_baz
