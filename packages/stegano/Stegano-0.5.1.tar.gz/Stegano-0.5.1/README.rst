Stéganô
=======

.. image:: https://api.travis-ci.org/cedricbonhomme/Stegano.svg?branch=master
    :target: https://travis-ci.org/cedricbonhomme/Stegano

A Python Steganography module.


Installation
------------

.. code:: bash

    $ sudo pip install Stegano


Use Stéganô as a library in your Python program
-----------------------------------------------

If you want to use Stéganô in your Python program you just have to import the
appropriate steganography technique. For example:

.. code:: python

    >>> from stegano import slsb
    >>> secret = slsb.hide("./pictures/Lenna.png", "Hello World")
    >>> secret.save("./Lenna-secret.png")


Use Stéganô as a program
------------------------

In addition you can use Stéganô as a program.

Example:

.. code:: bash

    $ slsb --hide -i ../examples/pictures/Lenna.png -o Lena1.png -m "Secret Message"

Another example (hide the message  with Sieve of Eratosthenes):

.. code:: bash

    $ slsb-set --hide -i ../examples/pictures/Lenna.png -o Lena2.png --generator eratosthenes -m 'Secret Message'


Examples
--------

There are some examples in the folder *examples*.

.. code:: bash

    $ git clone https://github.com/cedricbonhomme/Stegano.git
    $ cd stegano/examples


Running the tests
-----------------

.. code:: bash

    $ python -m unittest discover -v


Turorial
--------

A `tutorial <https://stegano.readthedocs.org>`_ is available.


Contact
-------

`My home page <https://www.cedricbonhomme.org>`_.
