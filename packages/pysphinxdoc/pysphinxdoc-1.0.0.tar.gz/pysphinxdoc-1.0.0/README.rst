
|Travis|_ |Coveralls|_ |Python27|_ |Python34|_ |PyPi|_ 

.. |Travis| image:: https://travis-ci.org/AGrigis/pysphinxdoc.svg?branch=master
.. _Travis: https://travis-ci.org/AGrigis/pysphinxdoc

.. |Coveralls| image:: https://coveralls.io/repos/AGrigis/pysphinxdoc/badge.svg?branch=master&service=github
.. _Coveralls: https://coveralls.io/github/AGrigis/pysphinxdoc

.. |Python27| image:: https://img.shields.io/badge/python-2.7-blue.svg
.. _Python27: https://badge.fury.io/py/pysphinxdoc

.. |Python34| image:: https://img.shields.io/badge/python-3.4-blue.svg
.. _Python34: https://badge.fury.io/py/pysphinxdoc

.. |PyPi| image:: https://badge.fury.io/py/pysphinxdoc.svg
.. _PyPi: https://badge.fury.io/py/pysphinxdoc


===========
pysphinxdoc
===========

[pysphinxdoc] API Documentation Generation Tool.

Pysphinxdoc is a tool for generating automatically API documentation
for Python modules, based on their reStructuredText docstrings, using the
`sikit-learn <http://scikit-learn.org/>`_ theme,
`Bootstrap <http://getbootstrap.com/>`_ and
`Sphinx <http://www.sphinx-doc.org/>`_.
Visit this `module documentation <https://AGrigis.github.io/pysphinxdoc/>`_
for a live example.

How to
------

Here is an exemple to generate the 'pysphinxdoc' module documentation:
first execute 'sphinxdoc -v 2 -p $HOME/git/pysphinxdoc/ -n pysphinxdoc
-o $HOME/git/pysphinxdoc/doc/' and then in the $HOME/git/pysphinxdoc/doc/
folder 'make raw-html'.

Expect a '$name_module/doc/source/_static' folder containing a logo named
'$name_module.png' and an 'carousel' subfolder containing a list of images
to be displayed in the index banner of the site.

The documentation is generated from the reStructuredText docstrings of each
module, function or class.

In order to find module information, an 'info.py' module is expected at the
root of the module with mandatory keys:

    * NAME: the name of the module.
    * DESCRIPTION: the module short description that will be displayed in the
      banner.
    * LONG_DESCRIPTION: the index page content.
    * URL: the module URL.
    * AUTHOR: the author of the module.
    * AUTHOR_EMAIL: the author e-mail.
    * __version__: the module version.

And optional keys:

    * EXTRANAME: a name that will be displayed in the last element of the
      navbar (default 'PYSPHINXDOC').
    * EXTRAURL: the associated URL (default the pySphinxDoc URL).

