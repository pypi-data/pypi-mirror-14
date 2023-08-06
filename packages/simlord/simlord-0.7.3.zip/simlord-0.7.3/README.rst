README
======

SimLoRD - Simulate long Read Data
---------------------------------

SimLoRD is a read simulator for third generation sequencing reads and is
currently focused on the Pacific Biosciences SMRT error model.

Reads are simulated from both strands of a provided or randomly
generated reference sequence.

Features
~~~~~~~~

-  The reference can be read from a FASTA file or randomly generated
   with a given GC content. It can consist of several chromosomes, whose
   structure is respected when drawing reads. (Simulation of genome
   rearrangements may be incorporated at a later stage.)
-  The read lengths can be determined in four ways: drawing from a
   log-normal distribution (typical for genomic DNA), sampling from an
   existing FASTQ file (typical for RNA), sampling from a a text file
   with integers (RNA), or using a fixed length
-  Quality values and number of passes depend on fragment length.
-  Provided subread error probabilities are modified according to number
   of passes
-  Outputs reads in FASTQ format and alignments in SAM format

System requirements
~~~~~~~~~~~~~~~~~~~

-  `python3 <https://www.python.org/>`__
-  `scipy <http://www.scipy.org/>`__
-  `numpy <http://www.numpy.org/>`__
-  `pysam <http://pysam.readthedocs.org/en/latest/>`__
-  `dinopy <https://bitbucket.org/HenningTimm/dinopy>`__

We recommend using
`miniconda <http://conda.pydata.org/miniconda.html#miniconda>`__ and
creating an environment for SimLoRD

::

    # Create and activate a new environment called simlord
    conda create -n simlord python=3 pip numpy scipy cython
    source activate simlord

    # Install packages that are not available with conda from pip
    pip install pysam
    pip install dinopy
    pip install simlord

    # You now have a 'simlord' script; try it:
    simlord --help

    # To switch back to your normal environment, use
    source deactivate

Platform support
~~~~~~~~~~~~~~~~

SimLoRD is a pure Python program. This means that it runs on any
operating system (OS) for which Python 3 and the other packages are
available.

Example usage
~~~~~~~~~~~~~

**Example 1:** Simulate 10000 reads for the reference ref.fasta, use the
default options for simulation and store the reads in ``myreads.fastq``
and the alignment in ``myreads.sam``.


::

    simlord  --read-reference ref.fasta -n 10000  myreads


**Example 2:** Generate a reference with 10 mio bases GC content 0.6
(i.e., probability 0.3 for both C and G; thus 0.2 probability for both A
and T), store the reference as random.fasta, and simulate 10000 reads
with default options, store reads as ``myreads.fastq``, do not store
alignments.

::

    simlord --generate-reference 0.6 10000000 --save-reference random.fasta\
            -n 10000 --nosam  myreads


**Example 3:** Simulate reads from the given ``reference.fasta``, using
a fixed read length of 5000 and custom subread error probabilities (12%
insertion, 12% deletion, 2% substitution). As before, save reads as
``myreads.fastq`` and ``myreads.sam``.

::

    simlord --read-reference reference.fasta  -n 10000 -fl 5000\
            -pi 0.12 -pd 0.12 -ps 0.02  myreads


A full list of parameters, as well as their documentation, can be found `here <https://bitbucket.org/genomeinformatics/simlord/wiki/Home>`__.

License
~~~~~~~

SimLoRD is Open Source and licensed under the `MIT
License <http://opensource.org/licenses/MIT>`__.