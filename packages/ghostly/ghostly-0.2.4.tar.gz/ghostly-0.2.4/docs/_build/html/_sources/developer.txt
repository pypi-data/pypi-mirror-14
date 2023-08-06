Developer Documentation
=======================

Contributions
-------------

Contributions are more than welcome!

To get setup do the following;

.. code-block:: bash

    mkvirtualenv --python=/usr/bin/python3.5 ghostly
    git clone https://github.com/alexhayes/ghostly.git
    cd ghostly
    pip install -r requirements/dev.txt
    pip install Django>=1.8,<1.9


Running Tests
-------------

Once you've checked out you should be able to run the tests.

.. code-block:: bash

    tox


Creating Documentation
----------------------

.. code-block:: bash

    cd docs
    make clean html

