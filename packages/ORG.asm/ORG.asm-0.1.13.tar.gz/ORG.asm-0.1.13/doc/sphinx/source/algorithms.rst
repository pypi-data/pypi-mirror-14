The ORGanelle ASeMbler algorithmns
==================================

In a eukaryote cell, the genome is mainly stored in the nucleus but organelles,
*i.e.* mitochondrion and chloroplast for plants contain also genetic material.
|Orgasm| is an assembler dedicated to assemble these organelle genome sequences
from a low coverage shotgun sequencing.

|Orgasm| relies on the property that the copy number of organelle genomes is
higher per cell than the count of nuclear genome copies. The typical size for an
animal mitochondrial genome is about 16,000 base pairs (bp), and 150,000 bp
or 150 kb for a plant chloroplastic genome.

.. figure:: genome_size.*
  :align: center
  :figwidth: 80 %
  :width: 600


.. figure:: algorithms.*
  :align: center
  :figwidth: 80 %
  :width: 500

.. toctree::
  :maxdepth: 2

  algorithms/seedselection
  algorithms/graphextension
  algorithms/graphcleanning
  algorithms/gapfilling
  algorithms/graphunfolding
