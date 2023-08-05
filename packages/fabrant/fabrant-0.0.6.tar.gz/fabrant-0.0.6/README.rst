fabrant
=======

Easy handling of vagrant hosts within fabric


Installation
------------

Easy as py(pi):

.. code:: bash

    $ pip install --upgrade fabrant


From git source:

.. code:: bash

    $ git clone https://github.com/constantinius/fabrant.git
    $ cd fabrant
    $ python setup.py install


Usage
-----

Using fabrant within a fabric script is easy:

.. code:: python

    from fabrant import vagrant

    # specify path for vagrant dir. Start the box if it is not already running.
    # Halt the box when context is closed.
    with vagrant("path/to/dir", up=True, halt=True):
        run("ls /vagrant")  # prints contents of usually enabled share


Contribute
----------

Report any issues you find `here
<https://github.com/constantinius/fabrant/issues>`_ or create `pull requests
<https://github.com/constantinius/fabrant/pulls>`_.
