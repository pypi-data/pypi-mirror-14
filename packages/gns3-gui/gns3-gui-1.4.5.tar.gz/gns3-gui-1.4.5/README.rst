GNS3-gui
========

.. image:: https://travis-ci.org/GNS3/gns3-gui.svg?branch=master
    :target: https://travis-ci.org/GNS3/gns3-gui

.. image:: https://img.shields.io/pypi/v/gns3-gui.svg
    :target: https://pypi.python.org/pypi/gns3-gui


GNS3 GUI repository.

Linux (Debian based)
--------------------

The following instructions have been tested with Ubuntu and Mint.
You must be connected to the Internet in order to install the dependencies.

Dependencies:

- Python 3.4 or above
- Setuptools
- PyQt 5 libraries
- Apache Libcloud library
- Requests library
- Paramiko library

The following commands will install some of these dependencies:

.. code:: bash

   sudo apt-get install python3-setuptools
   sudo apt-get install python3-pyqt5
   sudo apt-get install python3-pyqt5.qtsvg
   sudo apt-get install python3-pyqt5.qtwebkit

If you want to test using PyQt4

.. code:: bash
   sudo apt-get install python3-pyqt4

Finally these commands will install the GUI as well as the rest of the dependencies:

.. code:: bash

   cd gns3-gui-master
   sudo python3 setup.py install
   gns3

Windows
-------

Please use our `all-in-one installer <https://gns3.com/software/download>`_ to install the stable build.

If you install via source you need to first install:

- Python (3.3 or above) - https://www.python.org/downloads/windows/
- Pywin32 - https://sourceforge.net/projects/pywin32/
- Qt5 - http://www.qt.io/download-open-source/
- PyQt5 - http://www.riverbankcomputing.com/software/pyqt/download5
- PyCrypto (which if you compile from source, requires Visual Studio 2010 with GMP or MPIR libraries)

And finally, call

.. code:: bash

   python setup.py install

to install the remaining dependencies.

Mac OS X
--------

Please use our DMG package or you can manually install using the following steps (experimental):

`First install homebrew <http://brew.sh/>`_.

Then install the GNS3 dependencies.

.. code:: bash

   brew install python3
   brew install qt
   brew install sip --without-python --with-python3
   brew install pyqt5 --without-python --with-python3

If you want to test using PyQt4

.. code:: bash
   brew install pyqt --without-python --with-python3

Finally, install both the GUI & server from the source.

.. code:: bash

   cd gns3-gui-master
   python3 setup.py install

.. code:: bash

   cd gns3-server-master
   python3 setup.py install

Or follow this `HOWTO that uses MacPorts <http://binarynature.blogspot.ca/2014/05/install-gns3-early-release-on-mac-os-x.html>`_.

Development
-------------

If you want to update the interface, modify the .ui files using QT tools. And:

.. code:: bash

    cd scripts
    python build_pyqt.py

Debug
"""""

If you want to see the full logs in the internal shell you can type:

.. code:: bash
    
    debug 2


Or start the app with --debug flag.

Due to the fact PyQT intercept you can use a web debugger for inspecting stuff:
https://github.com/Kozea/wdb


Test with PyQT4
~~~~~~~~~~~~~~~~

If you want to simulate a user with PyQT4:

.. code:: bash
   
    export GNS3_QT4=1
    python gns3/main.py


