.. _oa:

The ORGanelle ASseMbler principles
==================================

.. include:: ./strategy.txt

.. include:: ./assembly-graph.txt


The ORGanelle ASseMbler commands
--------------------------------

Once installed, |Orgasm| enrich the command shell with the :ref:`oa <oa>` command. It is providing
a set of sub-commands allowing for the complete assembling of small genomes
(organelle genomes) from a genome skimming sequence dataset. You can have a
basic idea on how to proced by following the :doc:`tutorial <./mitochondrion>`.


.. figure:: command-flowgram.*
  :align: center
  :figwidth: 80 %
  :width: 500

  The :ref:`organelle assembler <oa>`'s provides a set of commands.

Several of these commands (at least three) have to executed to complete
an assembling process.

 - The bold green path indicates the minimal succession of
   commands you need to run to assemble a sequence from a set of illumina reads.
 - The green dotted path indicates an alternative succession of commands
   commonly run to achieve the assembling process.
 - The fine blue dotted arrows indicate the data used by each of the commands.
 - The fine red dotted arrows indicate the final results provided by commands.
 - The orange boxed commands correspond to utility commands not required for the
   assembling but sometime useful to get or restore some information.

The set of sub-commands can be splitted in several categories corresponding to
the main steps of the assembling procedure.

.. toctree::
   :maxdepth: 2

   preparing
   assembling
   finishing
   unfolding
   utilities


The file formats
================

.. include:: ./formats.txt


