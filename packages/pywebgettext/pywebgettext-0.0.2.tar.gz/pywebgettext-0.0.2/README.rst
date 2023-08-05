pywebgettext - Extract gettext strings from python template
===========================================================

You can use pywebgettext instead of xgettext in order to 
generate POT translation file from HTML template.
pywebgettext can extract the gettext message inside HTML tag attributes or script tag.


Installation
============

.. code-block:: bash

    pip install pywebgettext


Documentation
=============

1. Generate POT translation file:

.. code-block:: bash

    $ pywebgettext --output=locale/messages.pot --sort-by-file template1.html file2.py 


2. Merge against existing PO file or initialize a PO file:

.. code-block:: bash

    $ msgmerge --sort-by-file --output-file=locale/fr_FR/LC_MESSAGES/messages.po locale/fr_FR/LC_MESSAGES/messages.po locale/messages.pot


Initialize PO file, if it doesn't exist yet:

.. code-block:: bash

    $ msginit --input=messages --output-file=locale/fr_FR/LC_MESSAGES/messages.po --no-wrap --locale=fr_FR


3. Fill empty strings like msgstr "" in messages.po.

4. Compile:
    
.. code-block:: bash

    $ msgfmt locale/fr_FR/LC_MESSAGES/messages.po -o locale/fr_FR/LC_MESSAGES/messages.mo

