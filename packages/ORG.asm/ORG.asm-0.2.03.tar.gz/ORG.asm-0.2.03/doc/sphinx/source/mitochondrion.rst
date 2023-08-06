Assembling a mitochondrion genome with |orgasm|
===============================================

We are presenting here a simple case desmonstrating how to assemble a
mitochondrial genome from a genome skimming dataset. The dataset used
for this tutorial corresponds to a simulated datased presenting no difficulty
for its assembling. The aims of this tutorial is only to guide you during your
first steps with |orgasm|.

The dataset is composed of two files

    - a forward fastq file : :download:`papi_R1.fastq.gz <../../../samples/papi_R1.fastq.gz>`
    - a reverse fastq file : :download:`papi_R2.fastq.gz <../../../samples/papi_R2.fastq.gz>`

.. _mitoindex:

Step 1 : indexing the reads
---------------------------

To assemble a genome from sequence reads, you need first to index them. This step allows an efficient access
to the reads during the assembling process. The organelle assembler is optimized for running with paired end
Illumina reads. It can also works, but less efficiently, with single reads, and 454 or Ion Torrent reads.

Considering two fastq files ``papi_R1.fastq.gz`` and ``papi_R2.fastq.gz`` containing respectively the forward and the
reverse reads of the paired reads, to build the index named ``butterfly`` from a UNIX terminal you have to run the
:ref:`oa index <oa_index>` command:

.. code-block:: bash

    > oa index --estimate-length=0.9 butterfly papi_R1.fastq.gz papi_R2.fastq.gz

This command produce the following screen output

.. code-block:: bash

    2015-08-17 11:16:37,975 [INFO ]  Forward file compressed by gzip
    2015-08-17 11:16:37,978 [INFO ]  Reverse file compressed by gzip
    2015-08-17 11:16:37,981 [INFO ]  Computing read length statistics for the forward file
    Counter({100: 47371})
    2015-08-17 11:16:38,824 [INFO ]  Computing read length statistics for the reverse file
    Counter({100: 47371})
    2015-08-17 11:16:39,645 [INFO ]  Read size considered for a quantile of 0.90 : 100
    2015-08-17 11:16:39,646 [INFO ]  orgasmi -o butterfly -l 100 /var/folders/84/_g1lrhc11x170szbh74py3580000gn/T/tmp15_y043_/forward-c4ao4xw1 /var/folders/84/_g1lrhc11x170szbh74py3580000gn/T/tmp15_y043_/reverse-zjsu9xv0
    2015-08-17 11:16:39,646 [INFO ]  Starting indexing...
    2015-08-17 11:16:39,650 [INFO ]  Forward tmp file : /var/folders/84/_g1lrhc11x170szbh74py3580000gn/T/tmp15_y043_/forward-c4ao4xw1
    2015-08-17 11:16:39,650 [INFO ]  Reverse tmp file : /var/folders/84/_g1lrhc11x170szbh74py3580000gn/T/tmp15_y043_/reverse-zjsu9xv0

    Reading sequence reads...

    Read length adjusted to 99
    maximum reads : 55555555
        94742 sequences read

    Sorting reads...

        94742 sequences sorted

    Writing sorted sequence reads...

        94742 sequences read

    Writing sequence pairing data...

    Done.

    Reading indexed sequence reads...

        94742 sequences read

    Sorting reads...

        94742 sequences sorted

    Writing sequence suffix index...

    Done.

    Writing global data...

    Done.
    2015-08-17 11:16:41,612 [INFO ]  Done.

    Loading global data...

    Done.

    Reading indexed sequence reads...

        94742 sequences read

    Reading indexed pair data...

    Done.

    Loading reverse index...

    Done.

    Indexing reverse complement sequences ...


    Fast indexing forward reads...


    Fast indexing reverse reads...

    Done.
    2015-08-17 11:16:41,616 [INFO ]  Count of indexed reads: 94742
    Deleting tmp file : /var/folders/84/_g1lrhc11x170szbh74py3580000gn/T/tmp15_y043_/reverse-zjsu9xv0
    Deleting tmp file : /var/folders/84/_g1lrhc11x170szbh74py3580000gn/T/tmp15_y043_/forward-c4ao4xw1
    Deleting tmp file : /var/folders/84/_g1lrhc11x170szbh74py3580000gn/T/tmp15_y043_/unziped-zwymn7j9
    Deleting tmp file : /var/folders/84/_g1lrhc11x170szbh74py3580000gn/T/tmp15_y043_/unziped-c43bqgpw
    Deleting tmp directory : /var/folders/84/_g1lrhc11x170szbh74py3580000gn/T/tmp15_y043_


the :ref:`oa index <oa_index>` command is able to manage with compressed read files :

  - by `gzip`_ (file name ending by `.gz`)
  - by `bzip2`_ (file name ending by `.bz2`)

and to estimed the better indexing length to use :ref:`--estimate-length <index.estimate-length>`
option.

By using the following ``Unix`` command you can observe that the :ref:`oa index <oa_index>`
produced five files. All of them are named ``butterfly.???`` where ``???`` is a variable
three-letters extension.

.. code-block:: bash

    > ls -l
    total 11800
    -rw-r--r--  1 coissac  staff     1020 17 aoû 11:16 butterfly.log
    -rw-r--r--  1 coissac  staff  2652776 17 aoû 11:16 butterfly.ofx
    -rw-r--r--  1 coissac  staff      112 17 aoû 11:16 butterfly.ogx
    -rw-r--r--  1 coissac  staff   378968 17 aoû 11:16 butterfly.opx
    -rw-r--r--  1 coissac  staff   378968 17 aoû 11:16 butterfly.orx
    -rw-r--r--  1 coissac  staff  1303814 14 aoû 18:27 papi_R1.fastq.gz
    -rw-r--r--  1 coissac  staff  1302685 14 aoû 18:27 papi_R2.fastq.gz

``butterfly.log``
.................

    Contains traces from the indexing operation. Actually most of the screen
    outputs is also stored in this log file.

``butterfly.ofx``, ``butterfly.ogx``, ``butterfly.opx`` and ``butterfly.orx``
.............................................................................

    These four files are the sequence index. They contain all the information
    |orgasm| needs to perform the assembly. Once this indexing step is realised
    |orgasm| does not need anymore both the **fastq** files
    :download:`papi_R1.fastq.gz <../../../samples/papi_R1.fastq.gz>` and
    :download:`papi_R2.fastq.gz <../../../samples/papi_R2.fastq.gz>`.

Step 2 : Building the assembling graph
--------------------------------------

Now than the reads are indexed, we have to build the assembling graph.
This job is done by the :ref:`oa buildgraph <oa_buildgraph>` command.
This command can be launched with the following ``Unix`` command:

.. code-block:: bash

    $ oa buildgraph --seeds protMitoMachaon butterfly butterfly.mito

This ask for assembling the reads indexed in the ``butterfly`` index, using
the internal seed sequences named ``protMitoMachaon`` and constituted by the
set of protein sequences of the machaon mitochondrial genome. The result of the
assembling will be stored in a set of files named ``butterfly.mito.???`` where
is a variable three-letters extension.


.. code-block:: bash

    2015-08-17 12:05:24,808 [INFO ]  Building De Bruijn Graph
    2015-08-17 12:05:24,808 [INFO ]  Minimum overlap between read: 50

The first lines printed recall the current operation and the minimum length of
the overlap between two reads required during the assembling process.

Then the index is loaded in memory. For this tutorial we are assembling a
simulated dataset containing only 94742 sequences. A true dataset contains
usualy several millons of reads.

.. code-block:: bash

    Loading global data...

    Done.

    Reading indexed sequence reads...

        94742 sequences read

    Reading indexed pair data...

    Done.

    Loading reverse index...

    Done.

    Indexing reverse complement sequences ...


    Fast indexing forward reads...


    Fast indexing reverse reads...

    Done.

The assembler then load a set of external data and the ``protMitoMachaon``
seed set requested by the :ref:`--seeds <buildgraph.seeds>` option.

.. code-block:: bash

    2015-08-17 12:05:24,812 [INFO ]  Load 3' adapter internal dataset : adapt3ILLUMINA
    2015-08-17 12:05:24,812 [INFO ]  Load 5' adapter internal dataset : adapt5ILLUMINA
    2015-08-17 12:05:24,812 [INFO ]  Load probe internal dataset : protMitoMachaon

According to the global assembling algorithm the first step of the assembling constists in
looking for the reads presenting sequence similaritiy with seed sequences.

.. code-block:: bash

    2015-08-17 12:05:24,812 [INFO ]  Running probes matching against reads...
    2015-08-17 12:05:24,813 [INFO ]      -> probe set: protMitoMachaon
    2015-08-17 12:05:24,813 [INFO ]  Matching against protein probes
      99.7 % |#################################################| ] remain : 00:00:00
    2015-08-17 12:05:34,734 [INFO ]  ==> 10724 matches
    2015-08-17 12:05:34,740 [INFO ]  Match list :
    2015-08-17 12:05:34,741 [INFO ]       nd3        :  1267 (357.4x)
    2015-08-17 12:05:34,741 [INFO ]       nd4L       :   814 (279.8x)
    2015-08-17 12:05:34,741 [INFO ]       atp6       :  1493 (218.0x)
    2015-08-17 12:05:34,741 [INFO ]       cox3       :  1382 (174.1x)
    2015-08-17 12:05:34,741 [INFO ]       nd1        :  1446 (152.9x)
    2015-08-17 12:05:34,741 [INFO ]       cytB       :  1489 (128.6x)
    2015-08-17 12:05:34,741 [INFO ]       nd6        :   602 (112.2x)
    2015-08-17 12:05:34,741 [INFO ]       cox1       :  1356 ( 87.7x)
    2015-08-17 12:05:34,741 [INFO ]       nd4        :   637 ( 47.1x)
    2015-08-17 12:05:34,741 [INFO ]       cox2       :   193 ( 28.1x)
    2015-08-17 12:05:34,741 [INFO ]       atp8       :     5 (  3.0x)
    2015-08-17 12:05:34,741 [INFO ]       nd5        :    38 (  2.2x)
    2015-08-17 12:05:34,741 [INFO ]       nd2        :     2 (  0.2x)
    2015-08-17 12:05:34,741 [INFO ]  Coverage estimated from probe matches at : 357


In that case, 10724 matches where identified and they belong several genes as
shown by the printed table. This table allows also to make a first estimation
of the sequencing coverage.

.. code-block:: bash

    2015-08-17 12:05:34,741 [INFO ]  Minimum read estimated from coverage (357x)  ar: 58

Here estimated à *397x*. This coverage estimation is important because it allows to
set the assembling parametters. The estimation realized from matches is higly approximative.
To make a better estimate, 15kb of sequences are assembled following this first estimation.

.. code-block:: bash

    2015-08-17 12:05:34,775 [INFO ]  Assembling of 15000 pb for estimating actual coverage
    2015-08-17 12:05:34,775 [INFO ]  0 bp [ 0.0% fake reads; Stack size:    10723 /  -1.00 0  Gene: nd5
    2015-08-17 12:05:49,522 [INFO ]  10000 bp [ 0.0% fake reads; Stack size:    10723 /   0.00 0  Gene: nd5
    | : 14998 bp [ 0.0% fake reads; Stack size:    10723 /   0.00 0  Gene: nd5
    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393

    Deleting terminal branches

    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393
    2015-08-17 12:05:57,794 [INFO ]  Dead branch length setup to : 10 bp

    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393
    2015-08-17 12:05:58,247 [INFO ]  coverage estimated : 393x based on 14999 bp (minread: 64)

This allows to get a second coverage estimate (here *393x*) which is far most precise.
The true assembling stage can now be run.

.. code-block:: bash

    2015-08-17 12:05:58,315 [INFO ]  Starting the assembling
    2015-08-17 12:05:58,315 [INFO ]  0 bp [ 0.0% fake reads; Stack size:    10723 /  -1.00 0  Gene: nd5
    2015-08-17 12:06:13,684 [INFO ]  10000 bp [ 0.0% fake reads; Stack size:    10723 /   0.00 0  Gene: nd5
    - : 15185 bp [ 0.0% fake reads; Stack size:        9 /  -1.00 0  Gene: nd3

In our case it leads to the assembling of *15185 bp* in less of a minute.


Following the assembling a cleaning step is run to simplifly the assembling graph by
removing allow the aborted paths mainly created by sequencing errors and nuclear copies
of some part of the mitochondrial genome.

.. code-block:: bash

    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393
    Deleting terminal branches
    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393
    2015-08-17 12:06:25,465 [INFO ]       Dead branch length setup to : 10 bp
    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393

Following this cleaning a last estimate of the coverage is done.
Moreover the assembler estimates the insert size and the variance of this size.
This estimate is computed from the relative positions of the pair-end reads in
the assembling graph.

.. code-block:: bash

    2015-08-17 12:06:25,936 [INFO ]  coverage estimated : 393 based on 15184 bp (minread: 16)
    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393
    2015-08-17 12:06:26,434 [INFO ]  Fragment length estimated : 100.000000 pb (sd: 0.000000)

Because of our artificial dataset, the insert size is precisely 100bp and the standard
deviation is null.

When the sequence coverage is too low and/or when some low complexity sequences
(micro-satellite) are present into the genome the assembler is not able to produce
the complete sequence as a single contig.

To save these assembling a gap-filling step is systematically run for trying to
reduce as much as possible the number of contigs. Usually |orgasm| finished after
this step with a single contig.

.. code-block:: bash

    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393
    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393

    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393

    Deleting terminal branches

    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393
         Dead branch length setup to : 10 bp

    Remaining edges : 30370 node : 30370
    #######################################################
    #
    # Added : 0 bp (total=15185 bp)
    #
    #######################################################

In our case the assembling was complete so no base-pair was added and the gap-filling
procedure stop quicly.

The assembling procedure ends with a last cleaning step:

.. code-block:: bash

    ==================================================================

    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393

    ==================================================================

    2015-08-17 12:06:28,513 [INFO ]  Clean dead branches
    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393
    2015-08-17 12:06:28,869 [INFO ]       Dead branch length setup to : 10 bp

    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393
    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393
    2015-08-17 12:06:29,689 [INFO ]  Clean low coverage terminal branches
    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393

    Deleting terminal branches

    2015-08-17 12:06:30,049 [INFO ]  Clean low coverage internal branches
    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393

    Deleting terminal branches

    Deleting internal branches


And the scaffolding of the contigs if several of them persist after the gap-filling
procedure.

.. code-block:: bash

    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393
    2015-08-17 12:06:31,305 [INFO ]  Scaffold the assembly

At this step asking for the listing of the current directory

.. code-block:: bash

    > ls -l

shows that five new files were created. Their names start with the ``butterfly.mito``
prefix indicated as second parametter.

.. code-block:: bash

    total 14248
    -rw-r--r--  1 coissac  staff   252030 17 aoû 12:06 butterfly.mito.gml
    -rw-r--r--  1 coissac  staff   252030 17 aoû 12:06 butterfly.mito.intermediate.gml
    -rw-r--r--  1 coissac  staff    20688 17 aoû 12:06 butterfly.mito.log
    -rw-r--r--  1 coissac  staff   417567 17 aoû 12:06 butterfly.mito.oax
    -rw-r--r--  1 coissac  staff   302132 17 aoû 12:05 butterfly.mito.omx


``butterfly.mito.log``
......................

    Contains traces from the assembling operation. Actually most of the screen
    outputs is also stored in this log file.

``butterfly.mito.oax``
......................

    This file contains a description of the whole assembling graph. It
    is used to transfer the status of the assembling from a command to
    another. Most of the command read this file, alter the assembling
    graph extracted from it and overwrite this file with the new version
    of the graph.

``butterfly.mito.omx``
......................

    The ``butterfly.mito.omx`` file contains the set of seed reads.


``butterfly.mito.intermediate.gml`` and ``butterfly.mito.gml``
..............................................................

    The ``.gml`` file contains a simpliflied graph representation of
    the assembling. They can be visualized using any graph visualisation
    tools accepting the Graph Modeling Language (`GML`_) format. For this
    purpose we are usualy using the `Yed <yed>`_ program.

    The :download:`butterfly.mito.intermediate.gml <../../../samples/butterfly.mito.intermediate.gml>`
    file is produced regularly during the assembling process by the
    :ref:`oa index <oa_index>` command. It gives opportunity for following
    the assembling process during its computation.

    The :download:`butterfly.mito.gml <../../../samples/butterfly.mito.gml>`
    contains the final assembling graph.

    These files are produced for the user convinience and they are not
    reuse latter by the assembler.

Step 3 : unfolding the graph to get the sequence
------------------------------------------------

The last step required to get the sequence of the mitochondrial genome
is to extract the sequence from the graph. This operation corresponds to find
an optimal path in the graph. This linear path is a description of the sequence.

The :ref:`oa unfold <oa_unfold>` command realizes this operation and produces
as final result a fasta file containing the sequence of the assembled genome.

.. code-block:: bash

    > oa unfold butterfly butterfly.mito

The first outputs of the :ref:`oa unfold <oa_unfold>` command are similar to
those produced by the :ref:`oa buildgraph <oa_buildgraph>` command presenting
the loading of the sequence index and of the seed reads identified by the
:ref:`oa buildgraph <oa_buildgraph>` command.

.. code-block:: bash

    Loading global data...

    Done.

    Reading indexed sequence reads...

        94742 sequences read

    Reading indexed pair data...

    Done.

    Loading reverse index...

    Done.

    Indexing reverse complement sequences ...


    Fast indexing forward reads...


    Fast indexing reverse reads...

    Done.

    2015-08-17 12:25:18,563 [INFO ]  Load matches from previous run : 1 probe sets restored
    2015-08-17 12:25:18,563 [INFO ]     ==> A total of : 10724
    2015-08-17 12:25:18,564 [INFO ]  Match list :
    2015-08-17 12:25:18,564 [INFO ]       nd3        :  1267 (357.4x)
    2015-08-17 12:25:18,564 [INFO ]       nd4L       :   814 (279.8x)
    2015-08-17 12:25:18,564 [INFO ]       atp6       :  1493 (218.0x)
    2015-08-17 12:25:18,564 [INFO ]       cox3       :  1382 (174.1x)
    2015-08-17 12:25:18,564 [INFO ]       nd1        :  1446 (152.9x)
    2015-08-17 12:25:18,565 [INFO ]       cytB       :  1489 (128.6x)
    2015-08-17 12:25:18,565 [INFO ]       nd6        :   602 (112.2x)
    2015-08-17 12:25:18,565 [INFO ]       cox1       :  1356 ( 87.7x)
    2015-08-17 12:25:18,565 [INFO ]       nd4        :   637 ( 47.1x)
    2015-08-17 12:25:18,565 [INFO ]       cox2       :   193 ( 28.1x)
    2015-08-17 12:25:18,565 [INFO ]       atp8       :     5 (  3.0x)
    2015-08-17 12:25:18,565 [INFO ]       nd5        :    38 (  2.2x)
    2015-08-17 12:25:18,566 [INFO ]       nd2        :     2 (  0.2x)
    2015-08-17 12:25:18,901 [INFO ]  Evaluate fragment length
    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393
    2015-08-17 12:25:19,411 [INFO ]  Fragment length estimated : 100.000000 pb (sd: 0.000000)

A this stage a scaffolding of the assembling is realized for trying to identify
in the graph the missing edges by using the information provided by the pair-end
relationship.

.. code-block:: bash

    2015-08-17 12:25:19,411 [INFO ]  Evaluate pair-end constraints
    Compacting graph 100.0 % |#################################################\ ] remain : 00:00:00
    Minimum stem coverage = 393

On such assembling graph each contig can be assimilated to a path linking a
subset of vertices of a connected componante. Exploring connecting componante
can by expensive in computation time. To increase our change to find a solution
a heuristic is applyed on the graph to identify the connected componantes that
have a good chance to correspond to the targeted genome.

.. code-block:: bash

    2015-08-17 12:25:19,786 [INFO ]  Select the good connected componantes
    2015-08-17 12:25:19,787 [INFO ]  Print the result as a fasta file

    Coverage 1x = 396
    Path is circular

The selected componante(s) is/are analyzed to find an optimal path in them
and the corresponding sequence is printed out in a fasta file. If you look at
the file now contained by the current folder

.. code-block:: bash

    ls -l

You can observe two new files.

.. code-block:: bash

    -rw-r--r--  1 coissac  staff    31087 17 aoû 12:25 butterfly.mito.fasta
    -rw-r--r--  1 coissac  staff   252144 17 aoû 12:25 butterfly.mito.path.gml


The  :download:`butterfly.mito.path.gml <../../../samples/butterfly.mito.path.gml>`
file contains a simplified graph representation of the assembling similar to the
one produced by the :ref:`oa buildgraph <oa_buildgraph>` command but including
moreover information about the selected path.

.. figure:: butterfly.mito.path.*
  :align: center
  :figwidth: 80 %
  :width: 500

  The ``.gml`` file contains a graph representation of the assembling

  It can be visualized using the `Yed <yed>`_ program


The :download:`butterfly.mito.fasta <../../../samples/butterfly.mito.fasta>`
file contains the produced sequence in fasta format. Most of the time you have
a single contig corresponding to the complete sequence of the targeted genome.
You can read this file using your favorite sequence/text editor or using the
**Unix** ``cat`` command.

.. code-block:: bash

    > cat butterfly.mito.fasta

.. code-block:: bash

    >Seq_1 seq_length=15184; coverage=393.0; circular=True; -1 : ACCCG->(15184)->AAAAC  [393].{connection: 1}
    ACCCGAAAATTTCCCAGAATAAATAAAATTTTACTAAACCTATCAACACCAAAAAACATT
    TATATTTTTTTCCACTATTTATATAATTTTTAAAAAAAAAATATTTTTTAAAATTTAAAA
    AAACACCCTCAGAGAAAATTCTCAAAAAAAAAAATCTTTTAAAGATAAAAAAGTTAATAA
    ATTTCATTTAAATAAATTTTATTAGTAAATAATAAATATTAATAGATTAAATTAAATATT
    AAATTATTAGGTGAAATTTTAATTTAATTAAAATTTTAATAAATAATATGATTTATTAAA
    TTTTATAAAAAACTAGAATTAGATACTCTATTATTAAAAATTAAATAAAAAATACTAAAA
    TAGTATATAATTATTTATAGAAACTTAAATAATTTGGCGGTATTTTAGTTCATTTAGAGG
    AATCTGTTTAATAATTGATAATCCACGAATAAATTTACTTAATTTATATATTTTGTATAT
    CGTTGTTAAAAAAATATTTTTTAATAAAAATAATATTTAAAAATTTTAAAATTAAATTAA
    TTCAGATCAAGATGCAGATTATAATTAAGAATATAATGGATTACAATAAGAAATGATTAA
    ...
    AGGGATTTCCTTTATATTTGGGGTATGAACCCAAAAGCTTATTTTAGCTTATTTTTAATT
    TTATTTTTTTTTATTTATATAAATATTTATATGGAATGGTTTAGTAAAAAAATAAAAATA
    TTATATAAATTATTAATAGTAAAAAAAAAATTAAGGTTTTTAAATTTTTTTAGTAATATA
    TATATATATATATTAAAAATTTAATATATTAATATATTTAATAATATAATAAAAATATTT
    AATTTATTAATATATAAATTAATATATTATAATTTTTTAGTTTTTAAAATTTTATATAGC
    AATTTAGGTATTTAATATTTATTATGAAAAAAAAAAAAAAAAAAATTATTTAAGGGTTTA
    ATAAGGGCCTAATAAAAAATTTTATAAAAGGGGATTTTTTTAAAAATTAAAAAATTTAAA
    AAAC

.. _`gzip`: http://www.gzip.org
.. _`bzip2`: http://www.bzip.org
.. _`GML`: https://en.wikipedia.org/wiki/Graph_Modelling_Language
.. _`yed`: https://www.yworks.com/en/products/yfiles/yed/
