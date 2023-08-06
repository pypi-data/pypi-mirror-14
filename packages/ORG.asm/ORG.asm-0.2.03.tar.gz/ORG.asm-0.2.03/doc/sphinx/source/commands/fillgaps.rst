.. _oa_fillgaps:

The :program:`fillgaps` command
===============================

At the end of the :ref:`oa buildgraph <oa_buildgraph>` command the assembling graph
is not always complete. Because of the non homogeneous coverage, some parts of the
genome too low covered were not able to be assembled using the heuristics parameters
used to assemble the main parts of the genome. The :program:`fillgaps` command aims
to rerun the *fillgap* algorithm used by the :ref:`oa buildgraph <oa_buildgraph>`
but with other parameters allowing to fill the gaps not assembled during the initial
assembling.

.. figure:: ../oa-fillgaps.*
  :align: center
  :figwidth: 80 %
  :width: 500

  The :ref:`organelle assembler <oa>`'s :program:`fillgaps` command
  executes all the colored tasks, starting by the green one and ending
  at the red task

command prototype
-----------------

.. program:: oa fillgaps

    usage: oa fillgaps [-h] [--minread BUILDGRAPH:MINREAD]
                       [--coverage BUILDGRAPH:COVERAGE]
                       [--minratio BUILDGRAPH:MINRATIO]
                       [--mincov BUILDGRAPH:MINCOV]
                       [--minoverlap BUILDGRAPH:MINOVERLAP]
                       [--smallbranches BUILDGRAPH:SMALLBRANCHES]
                       [--lowcomplexity] [--back ORGASM:BACK] [--snp]
                       [--adapt5 adapt5] [--adapt3 adapt3]
                       [--seeds seeds] [--kup ORGASM:KUP]
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

.. _fillgaps.seeds:

.. _seeds.kup:

.. code-block:: bash

   $ oa fillgaps --seeds protChloroArabidopsis seqindex

A set of seed sequences must be or nucleic or proteic. For initiating
assembling with both nucleic and proteic sequences you must use at least two 
``--seeds`` options one for each class of sequences.

.. code-block:: bash

   $ oa fillgaps --seeds protChloroArabidopsis --seeds rDNAChloro.fasta seqindex


.. include:: ../options/kup.txt

Graph extension options
+++++++++++++++++++++++

.. figure:: ../extension.*
  :align: center
  :figwidth: 80 %
  :width: 500

  The assembling stack


.. option::    --minread BUILDGRAPH:MINREAD

        the minimum count of read to consider [default: <estimated>]

        .. code-block:: bash

          $ oa fillgaps --minread 5 seqindex

        Consider an extension if at least five reads are present in the extension
        stack.

.. option::    --coverage BUILDGRAPH:COVERAGE

        the expected sequencing coverage [default:
        <estimated>]

.. option::    --minoverlap BUILDGRAPH:MINOVERLAP

        minimum length of the overlap between the sequence and
        reads to participate in the extension. [default:
        <estimated>]

.. option::    --minratio BUILDGRAPH:MINRATIO

        minimum ratio between occurrences of an extension and
        the occurrences of the most frequent extension to keep
        it. [default: <estimated>]

.. option::    --mincov BUILDGRAPH:MINCOV

        minimum occurrences of an extension to keep it.
        [default: 1]

Graph filtering options
+++++++++++++++++++++++

.. option::    --lowcomplexity

        Use also low complexity probes

.. option::    --adapt5 adapt5

        adapter sequences used to filter reads beginning by
        such sequences; either a fasta file containing adapter
        sequences or internal set of adapter sequences among
        ['adapt5ILLUMINA'] [default: adapt5ILLUMINA]

.. option::    --adapt3 adapt3

        adapter sequences used to filter reads ending by such
        sequences; either a fasta file containing adapter
        sequences or internal set of adapter sequences among
        ['adapt3ILLUMINA'] [default: adapt3ILLUMINA]

Graph limit option
++++++++++++++++++

.. option::    --assmax BUILDGRAPH:ASSMAX

        maximum base pair assembled

Graph cleaning options
++++++++++++++++++++++

.. option::    --smallbranches BUILDGRAPH:SMALLBRANCHES

        After a cycle a extension, if you observe the assembling graph
        you can observe a main path and many small aborted branches surrounding
        this main path. They correspond to path initiated by a sequencing
        error or a nuclear copy of a chloroplast region not enough covered by
        the skimming sequencing to be successfuly extended.
        One of the cleaning step consist in deleting these small branches.
        This option indicates up to which lenght branches have to be deleted.
        By default this legth is automaticaly estimated from the graph.

          .. code-block:: bash

            $ oa buildgraph --seeds protChloroArabidopsis \
                            --smallbranches 15 seqindex

          During the cleaning steps, all the branches with a legth
          shorter or equal to 15 base pairs will be deleted

.. option::    --snp

        When the data set correspond to a pool of individuals, it is possible
        that natural polymorphisms artificially complexy the assembling graph.
        For helping the assembling process of such data set, this option will
        clear the graph for such SNP by keeping only the most abundant allele
        prsent in the dataset. The generated sequence can be considered as a
        king of consensus. Read can be remapped in a second time on this
        consensus using classical sofware like `BWA <bwa>`_ to get the lost SNP
        information.

        By default this option is deactivated

          .. code-block:: bash

            $ oa fillgaps --seeds protChloroArabidopsis \
                            --snp seqindex

          Run the assembling, ignoring the SNPs.


Gap filling option
++++++++++++++++++

.. option::    --back ORGASM:BACK

        The number of bases taken at the end of contigs to
        jump with pared-ends [default: <estimated>]

.. _`bwa`: http://sourceforge.net/projects/bio-bwa/
.. _`yed`: https://www.yworks.com/en/products/yfiles/yed/
