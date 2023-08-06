Installing |orgasm|
===================

Availability of |orgasm|
........................

|Orgasm| is open source and protected by the CeCILL 2.1 license
(`http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html <http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html>`_).

|Orgasm| is deposited on the Python Package Index (PyPI : `https://pypi.python.org/pypi/ORG.asm`_)
and all the sources can be downloaded from the `metabarcoding.org <http://metabarcoding.org>`_ gitlab server
(`https://git.metabarcoding.org/org-asm/org-asm`_).

Prerequisites
.............

To install the |orgasm|, you need that these softwares are installed on your
system:

* Python 3.4 (installed by default on most ``Unix`` systems, available from
  `the Python website <http://www.python.org/>`_)
* ``gcc`` (installed by default on most ``Unix`` systems, available from the
  GNU sites dedicated to `GCC <https://www.gnu.org/software/gcc/>`_ and
  `GMake <https://www.gnu.org/software/make/>`_)

On a linux system
^^^^^^^^^^^^^^^^^

You have to take care that the Python development packages are installed.

On MacOSX
^^^^^^^^^

The C compiler and all the other compilation tools are included in the `XCode <https://itunes.apple.com/fr/app/xcode/id497799835?mt=12>`_
application not installed by default. Python3 is not prived by default. You have to install a complete distribution
of Python that you can download as a `MacOSX package from the Python website <https://www.python.org/downloads/>`_.

Downloading and installing |orgasm|
...................................

The |orgasm| is downloaded and installed using the :download:`get-orgasm.py <../../../get_orgasm/get-orgasm.py>` script.
This is a user level installation that does not need administrator privilege.

Once downloaded, move the file :download:`get-orgasm.py <../../../get_orgasm/get-orgasm.py>` in the directory where you want to install
the |orgasm|. From a Unix terminal you must now run the command :

  .. code-block:: bash

      > python3 get-orgasm.py

The script will create a new directory at the place you are running it in which all the
|orgasm| will be installed. No system privilege are required, and you system will not
be altered in any way by the obitools installation.

The newly created directory is named ORG.asm-VERSION where version is substituted by the
latest version number available.

Inside the newly created directory all the |orgasm| is installed. Close to this directory
there is a shell script named ``orgasm``. Running this script activate the |orgasm|
by reconfiguring your Unix environment.

  .. code-block:: bash

	> ./orgasm

Once activated you can desactivate |orgasm| by typing the command ``exit``.

  .. code-block:: bash

	> exit

	ORG.asm are no more activated, Bye...
	=====================================


System level installation
.........................

To install the |orgasm| at the system level you can follow two options :

	- copy the |orgasm| script in a usual directory for installing program like ``/usr/local/bin``
	  but never move the ``ORG.asm`` directory itself after the installation by the
	  :download:`get-orgasm.py <../../../get_orgasm/get-orgasm.py>`.

	- The other solution is to add the ``export/bin`` directory located in the ``ORG.asm`` directory
	  to the ``PATH`` environment variable.

Retrieving the sources of |orgasm|
..................................

If you want to compile by yourself the |orgasm|, you will need to install the same
prerequisite:

  .. code-block:: bash

    > pip3 install -U pip
    > pip3 install -U sphinx
    > pip3 install -U cython

moreover you need to install any git client (a list of clients is available from `GIT website <https://git-scm.com/downloads>`_)

Then you can download the

  .. code-block:: bash

      > git clone https://git.metabarcoding.org/org-asm/org-asm.git

This command will create a new directory called ``org-asm``.

Compiling and installing |orgasm|
.................................

From the directory where you retrieved the sources, execute the following commands:

  .. code-block:: bash

      > cd org-asm

      > python3 setup.py --serenity install

Once installed, you can test your installation by running the commands of the
:doc:`tutorials <./mitochondrion>`.
