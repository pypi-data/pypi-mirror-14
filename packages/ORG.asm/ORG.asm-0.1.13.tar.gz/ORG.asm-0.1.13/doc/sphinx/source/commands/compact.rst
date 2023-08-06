.. _oa_compact:

The :program:`compact` command
==============================

The :ref:`organelle assembler <oa>`'s :program:`compact`
rebuild the `gml` file containing the compacted version of the assembling graph
from a previously asssembled dataset.

command prototype
-----------------

.. program:: oa buildgraph

.. code-block:: none

    usage: oa buildgraph [-h]
                         [--back ORGASM:BACK]
                         index [output]

.. include:: ../options/positional.txt


optional arguments
------------------

General option
++++++++++++++

.. option::    -h, --help

                              show the help message and exit

Scaffolding option
++++++++++++++++++

.. _buildgraph.back:

.. include:: ../options/back.txt

