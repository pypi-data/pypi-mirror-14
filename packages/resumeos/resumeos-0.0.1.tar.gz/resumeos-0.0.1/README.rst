ResumeOS
========

Easily bootstrap an OS project to fool HR departments and pad your
resume.

Installation
------------

The old way

.. code:: sh

    git clone https://github.com/melonmanchan/ResumeOS
    cd ResumeOS
    python setup.py install

Or with PIP

.. code:: sh

    pip install resumeos

Tested with Python 2.7.10 on Ubuntu 15.10.

Usage
-----

Just install the required dependancies as specified above, and run

.. code:: sh

    resumeos --name 'My cool OS project' --output 'Best project ever!'

to bootstrap your very own totally unique OS, that prints the output
message and halts.

.. figure:: http://i.imgur.com/KClYFeI.png
   :alt: Example output

   Example output

Credits
-------

This project is based completely on the works of the very handsome and
talented Philipp Oppermann and his ‘Writing an OS in Rust’-book

http://os.phil-opp.com/
