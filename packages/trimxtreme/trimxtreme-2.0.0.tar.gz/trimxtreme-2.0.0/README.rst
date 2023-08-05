.. image:: https://travis-ci.org/foom/trimxtreme.svg?branch=master
    :target: https://travis-ci.org/foom/trimxtreme

.. image:: https://img.shields.io/pypi/v/trimxtreme.svg?branch=master
    :target: https://pypi.python.org/pypi/trimxtreme

========
trimxtreme
========

Cutadapt finds and removes adapter sequences, primers, poly-A tails and other
types of unwanted sequence from your high-throughput sequencing reads.

Cleaning your data in this way is often required: Reads from small-RNA
sequencing contain the 3’ sequencing adapter because the read is longer than
the molecule that is sequenced. Amplicon reads start with a primer sequence.
Poly-A tails are useful for pulling out RNA from your sample, but often you
don’t want them to be in your reads.

Cutadapt helps with these trimming tasks by finding the adapter or primer
sequences in an error-tolerant way. It can also modify and filter reads in
various ways. Adapter sequences can contain IUPAC wildcard characters. Also,
paired-end reads and even colorspace data is supported. If you want, you can
also just demultiplex your input data, without removing adapter sequences at all.

Cutadapt comes with an extensive suite of automated tests and is available under
the terms of the MIT license.

If you use trimxtreme, please cite
`DOI:10.14806/ej.17.1.200 <http://dx.doi.org/10.14806/ej.17.1.200>`_ .


Links
-----

* `Documentation <https://trimxtreme.readthedocs.org/>`_
* `Source code <https://github.com/foom/trimxtreme/>`_
* `Report an issue <https://github.com/foom/trimxtreme/issues>`_
* `Project page on PyPI (Python package index) <https://pypi.python.org/pypi/trimxtreme/>`_
* `Follow @foom_ on Twitter <https://twitter.com/foom_>`_
* `Wrapper for the Galaxy platform <https://bitbucket.org/lance_parsons/trimxtreme_galaxy_wrapper>`_
