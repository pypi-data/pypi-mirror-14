.. _oa_buildgraph:

The :program:`buildgraph` command
=================================

The :ref:`organelle assembler <oa>`'s :program:`buildgraph`
realizes the assembling of the reads by building the De Bruijn Graph which
is the central data structure used by the :ref:`organelle assembler <oa>`.

.. figure:: ../oa-buildgraph.*
  :align: center
  :figwidth: 80 %
  :width: 500

  The :ref:`organelle assembler <oa>`'s :program:`buildgraph` command
  executes all the colored tasks, starting by the green one and ending
  at the red task


command prototype
-----------------

.. program:: oa buildgraph

.. code-block:: none

    usage: oa buildgraph [-h]
                         [--seeds seeds] [--kup ORGASM:KUP]
                         [--adapt5 adapt5] [--adapt3 adapt3]
                         [--coverage BUILDGRAPH:COVERAGE]
                         [--lowcomplexity]
                         [--minread BUILDGRAPH:MINREAD]
                         [--minoverlap BUILDGRAPH:MINOVERLAP]
                         [--minratio BUILDGRAPH:MINRATIO]
                         [--mincov BUILDGRAPH:MINCOV]
                         [--assmax BUILDGRAPH:ASSMAX]
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

Graph initialisation options
++++++++++++++++++++++++++++

.. _buildgraph.seeds:

.. include:: ../options/seeds.txt

.. code-block:: bash

   $ oa buildgraph --seeds protChloroArabidopsis seqindex

A set of seed sequences must be or nucleic or proteic. For initiating
assembling with both nucleic and proteic sequences you must use at least two 
``--seeds`` options one for each class of sequences.

.. code-block:: bash

   $ oa buildgraph --seeds protChloroArabidopsis --seeds rDNAChloro.fasta seqindex

.. _buildgraph.kup:

.. include:: ../options/kup.txt

Graph extension options
+++++++++++++++++++++++

The main aim of the :program:`buildgraph` command is to build the De Bruijn Graph which
is the central data structure used by the :ref:`organelle assembler <oa>`. This building is
done by two algorithms:

   - the *extension* algorithm which is the main one 
   - the *fillgap* algorithm which is run when the first one failed to rescue the assembling procedure.
   
The *extension* algorithm is actually an heuristics and several parametters can be set to adapt the 
efficiency of the algorithm to your data. Without precising them, these parameters are automatically
estimated from the dataset.

.. figure:: ../extension.*
  :align: center
  :figwidth: 80 %
  :width: 500

  The assembling stack


.. option::    --minread BUILDGRAPH:MINREAD

        the minimum count of read to consider [default:
        <estimated>]

         .. code-block:: bash
         
            $ oa buildgraph --seeds protChloroArabidopsis --minread 5 seqindex

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

This set of options allows for excluding some reads from the assembling procedure.


.. option::    --lowcomplexity

        Use also low complexity probes. Probes are the 3' end of
        the sequence currently extended. By default probes with 
        a low complexity are not used during the graph extension 
        procedure. A probe is defined as a low complexity probe if 
        it is fully composed of an homopolymer or an homo-dimer or 
        an homo-trimer. 

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

        Maximum base pair assembled. This limit the size of the 
        De Bruijn Graph, and must be set to a larger value than
        the size of the sequence you want to assemble to take into
        account all the alternative paths present in the De Bruijn Graph.

Graph cleaning options
++++++++++++++++++++++

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
         
            $ oa buildgraph --seeds protChloroArabidopsis \
                            --smallbranches 15 seqindex

        During the cleaning steps, all the branches with a length
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

            $ oa buildgraph --seeds protChloroArabidopsis \
                            --snp seqindex

        Run the assembling, ignoring the SNPs.


Scaffolding option
++++++++++++++++++

.. _buildgraph.back:

.. include:: ../options/back.txt

.. _`bwa`: http://sourceforge.net/projects/bio-bwa/
.. _`yed`: https://www.yworks.com/en/products/yfiles/yed/
