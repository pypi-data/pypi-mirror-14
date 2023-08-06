.. _oa_cutlow:

The :program:`cutlow` command
=============================

The :ref:`organelle assembler <oa>`'s :program:`cutlow`
redoes the cleaning step allowing to clean-out all the branches of the assembling graph
not reaching the coverage specified by the `--coverage` option.
realizes the assembling of the reads by building the De Bruijn Graph which
is the central data structure used by the :ref:`organelle assembler <oa>`.

.. figure:: ../oa-cutlow.*
  :align: center
  :figwidth: 80 %
  :width: 500

  The :ref:`organelle assembler <oa>`'s :program:`cutlow` command
  re-executes all the cleaning task in red.


command prototype
-----------------

.. program:: oa buildgraph

.. code-block:: none

    usage: oa cutlow [-h]
                     [--coverage BUILDGRAPH:COVERAGE]
                     [--smallbranches BUILDGRAPH:SMALLBRANCHES]
                     [--back ORGASM:BACK] [--snp]
                     index [output]

.. include:: ../options/positional.txt

optional arguments
------------------

General option
++++++++++++++

.. option::    -h, --help

                              show the help message and exit

Graph cleaning options
++++++++++++++++++++++

.. option::    --coverage BUILDGRAPH:COVERAGE

        during the cutlow execution all stems with a coverage below the specified coverage
        will be deleted [default:<estimated>]


.. _buildgraph.smallbranches:

.. option::    --smallbranches BUILDGRAPH:SMALLBRANCHES

        After a cycle a extension, if you observe the assembling graph
        you can observe a main path and many small aborted branches surrounding
        this main path. They correspond to path initiated by a sequencing
        error or a nuclear copy of a chloroplast region not enough covered by
        the skimming sequencing to be successfully extended.
        One of the cleaning step consist in deleting these small branches.
        This option indicates up to which length branches have to be deleted.
        By default this length is automatically estimated from the graph.

            .. code-block:: bash
            
               $ oa cutlow --smallbranches 15 seqindex
            
        During the cleaning steps, all the branches with a length
        shorter or equal to 15 base pairs will be deleted
                              
Scaffolding option
++++++++++++++++++

.. _buildgraph.back:

.. include:: ../options/back.txt

                              