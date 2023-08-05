=======
notizen
=======

I take notes in some plain text files (Markdown/rST format, usually). After a while, I've already a few files and I need to find easily those files I need.

That's why I developed this tool: to index those notes and to traverse the index and locate the needed notes.

At the moment it is pretty limited: only search by tag, not by title, nor date, nor content.

.. image:: https://img.shields.io/pypi/dw/notizen.svg
   :target: https://pypi.python.org/pypi/notizen/
   :alt: PyPI Downloads

.. image:: https://img.shields.io/pypi/v/notizen.svg
   :target: https://pypi.python.org/pypi/notizen/
   :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/l/notizen.svg
   :target: https://pypi.python.org/pypi/notizen/
   :alt: License

Installation
============

.. code-block:: bash

	$ sudo pip3 install --upgrade notizen

Usage
=====

First index some notes:

.. code-block:: bash

	$ notizen updatedb my-notes/

Then you can search for all files with tag python:

.. code-block:: bash

	$ notizen locate python
	2 matching files under tag "python":
        /foo/bar/my-notes/python_annotations.md
        /foo/bar/my-notes/async-python.md

