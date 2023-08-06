.. _oa_seeds:

The :program:`seeds` command
============================

.. note::

  For most of the users this command is useless, because this task is automaticaly
  realized by the :ref:`oa buildgraph <oa_buildgraph>` command.


The :ref:`organelle assembler <oa>`'s :program:`seeds` computes the set
of seed reads. The main reason of this command if to write a new version
of the file containing the set of seed reads, because its format changed.

.. figure:: ../oa-seeds.*
  :align: center
  :figwidth: 80 %
  :width: 500

  The :ref:`organelle assembler <oa>`'s :program:`seeds` command
  executes only the red task


command prototype
-----------------

.. program:: oa seeds

.. code-block:: none

    usage: oa seeds [-h] [--seeds seeds] [--kup ORGASM:KUP]
                    index [output]

.. include:: ../options/positional.txt

optional arguments
------------------

General option
++++++++++++++

.. option::    -h, --help

        Shows the help message and exit

Graph initialisation options
++++++++++++++++++++++++++++

.. _seeds.seeds:

.. include:: ../options/seeds.txt

.. code-block:: bash

   $ oa seeds --seeds protChloroArabidopsis seqindex

A set of seed sequences must be or nucleic or proteic. For initiating
assembling with both nucleic and proteic sequences you must use at least two 
``--seeds`` options one for each class of sequences.

.. code-block:: bash

   $ oa seeds --seeds protChloroArabidopsis --seeds rDNAChloro.fasta seqindex


.. _seeds.kup:

.. include:: ../options/kup.txt
