Writing PB in file
==================

.. contents:: Table of Contents
   :local:
   :backlinks: none

.. note::

   This page is initialy a jupyter notebook. You can see a `notebook HTML
   render <WritePB_.html>`__ of it or download the `notebook
   itself <WritePB.ipynb>`__.


The API allows to write all the files the command line tools can. This
includes the outputs of PBassign. The functions to handle several file
formats are available in the :mod:`pbxplore.io` module.

.. code:: python

    from __future__ import print_function, division
    from pprint import pprint
    import os

.. code:: python

    import pbxplore as pbx

::

    ---------------------------------------------------------------------------

    ImportError                               Traceback (most recent call last)

    <ipython-input-2-853cbdb98b68> in <module>()
    ----> 1 import pbxplore as pbx


    ImportError: No module named pbxplore

Fasta files
-----------

The most common way to save PB sequences is to write them in a fasta
file.

PBxplore allows two ways to write fasta files. The sequences can be
written either all at once or one at a time. To write a batch of
sequences at once, we need a list of sequences and a list of the
corresponding sequence names. The writing function here is
:func:`pbxplore.io.write_fasta`.

.. code:: python

    names = []
    pb_sequences = []
    pdb_path = os.path.join(pbx.DEMO_DATA_PATH, '2LFU.pdb')
    for chain_name, chain in pbx.chains_from_files([pdb_path]):
        dihedrals = chain.get_phi_psi_angles()
        pb_seq = pbx.assign(dihedrals)
        names.append(chain_name)
        pb_sequences.append(pb_seq)

    pprint(names)

    pprint(pb_sequences)

    with open('output.fasta', 'w') as outfile:
        pbx.io.write_fasta(outfile, pb_sequences, names)

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-3-feec9831b75c> in <module>()
          1 names = []
          2 pb_sequences = []
    ----> 3 pdb_path = os.path.join(pbx.DEMO_DATA_PATH, '2LFU.pdb')
          4 for chain_name, chain in pbx.chains_from_files([pdb_path]):
          5     dihedrals = chain.get_phi_psi_angles()


    NameError: name 'pbx' is not defined

.. code:: python

    !cat output.fasta
    !rm output.fasta

::

    cat: output.fasta: Aucun fichier ou dossier de ce type
    rm: impossible de supprimer «output.fasta»: Aucun fichier ou dossier de ce type

Sequences can be written once at a time using the
:func:`pbxplore.io.write_fasta_entry` function.

.. code:: python

    pdb_path = os.path.join(pbx.DEMO_DATA_PATH, '2LFU.pdb')
    with open('output.fasta', 'w') as outfile:
        for chain_name, chain in pbx.chains_from_files([pdb_path]):
            dihedrals = chain.get_phi_psi_angles()
            pb_seq = pbx.assign(dihedrals)
            pbx.io.write_fasta_entry(outfile, pb_seq, chain_name)

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-5-ca18ad829ea9> in <module>()
    ----> 1 pdb_path = os.path.join(pbx.DEMO_DATA_PATH, '2LFU.pdb')
          2 with open('output.fasta', 'w') as outfile:
          3     for chain_name, chain in pbx.chains_from_files([pdb_path]):
          4         dihedrals = chain.get_phi_psi_angles()
          5         pb_seq = pbx.assign(dihedrals)


    NameError: name 'pbx' is not defined

.. code:: python

    !cat output.fasta
    !rm output.fasta

::

    cat: output.fasta: Aucun fichier ou dossier de ce type
    rm: impossible de supprimer «output.fasta»: Aucun fichier ou dossier de ce type

By default, the lines in fasta files are wrapped at 60 caracters as
defined in :const:`pbxplore.io.fasta.FASTA_WIDTH`. Both
:func:`pbxplore.io.write_fasta` and
:func:`pbxplore.io.write_fasta_entry` have a ``width`` optionnal
argument that allows to control the wrapping.

.. code:: python

    print(pb_sequences[0])

::

    ---------------------------------------------------------------------------

    IndexError                                Traceback (most recent call last)

    <ipython-input-7-37179c94b1b9> in <module>()
    ----> 1 print(pb_sequences[0])


    IndexError: list index out of range

.. code:: python

    with open('output.fasta', 'w') as outfile:
        for width in (60, 70, 80):
            pbx.io.write_fasta_entry(outfile, pb_sequences[0],
                                            'width={} blocks'.format(width),
                                            width=width)

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-8-975b3b2c17a0> in <module>()
          1 with open('output.fasta', 'w') as outfile:
          2     for width in (60, 70, 80):
    ----> 3         pbx.io.write_fasta_entry(outfile, pb_sequences[0],
          4                                         'width={} blocks'.format(width),
          5                                         width=width)


    NameError: name 'pbx' is not defined

.. code:: python

    !cat output.fasta
    !rm output.fasta

Dihedral angles
---------------

One needs the phi and psi dihedral angles to assign protein block
sequences. Having these angles, it is sometime convenient to store them
in a file. This can be done using the :func:`pbxplore.io.write_phipsi`
function. This function works like the :func:`pbxplore.io.write_fasta`
one as it takes 3 arguments: the output file, a list of dihedral angle
records, and a list of names corresponding to each record.

.. code:: python

    # Store the dihedral angles for all chains in a PDB file.
    # Store also the chain name for all chains.
    all_dihedrals = []
    names = []
    pdb_path = os.path.join(pbx.DEMO_DATA_PATH, '2LFU.pdb')
    for chain_name, chain in pbx.chains_from_files([pdb_path]):
        all_dihedrals.append(chain.get_phi_psi_angles())
        names.append(chain_name)

    # Write the dihedral angles in a file
    with open('output.phipsi', 'w') as outfile:
        pbx.io.write_phipsi(outfile, all_dihedrals, names)

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-10-d20016330794> in <module>()
          3 all_dihedrals = []
          4 names = []
    ----> 5 pdb_path = os.path.join(pbx.DEMO_DATA_PATH, '2LFU.pdb')
          6 for chain_name, chain in pbx.chains_from_files([pdb_path]):
          7     all_dihedrals.append(chain.get_phi_psi_angles())


    NameError: name 'pbx' is not defined

The output is formated with one line per residue. The first columns
repeat the name given for the chain, then is the residue id followed by
the phi and the psi angle. If an angle is not defined, 'None' is written
instead.

.. code:: python

    !head output.phipsi
    !tail output.phipsi
    !rm output.phipsi

::

    head: impossible d'ouvrir «output.phipsi» en lecture: Aucun fichier ou dossier de ce type
    tail: impossible d'ouvrir «output.phipsi» en lecture: Aucun fichier ou dossier de ce type
    rm: impossible de supprimer «output.phipsi»: Aucun fichier ou dossier de ce type

Read fasta files
----------------

We want to read sequences that we wrote in files. PBxplore provides a
function to read fasta files: the :func:`pbxplore.io.read_fasta`
function.

.. code:: python

    def pdb_to_fasta_pb(pdb_path, fasta_path):
        """
        Write a fasta file with all the PB sequences from a PDB
        """
        with open(fasta_path, 'w') as outfile:
            for chain_name, chain in pbx.chains_from_files([pdb_path]):
                dihedrals = chain.get_phi_psi_angles()
                pb_seq = pbx.assign(dihedrals)
                pbx.io.write_fasta_entry(outfile, pb_seq, chain_name)

    # Write a fasta file
    pdb_path = os.path.join(pbx.DEMO_DATA_PATH, '2LFU.pdb')
    pdb_to_fasta_pb(pdb_path, 'output.fasta')

    # Read a list of headers and a list of sequences from a fasta file
    names, sequences = pbx.io.read_fasta('output.fasta')

    print('names:')
    pprint(names)
    print('sequences:')
    pprint(sequences)

    !rm output.fasta

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-12-83ffe81d42a5> in <module>()
         10 
         11 # Write a fasta file
    ---> 12 pdb_path = os.path.join(pbx.DEMO_DATA_PATH, '2LFU.pdb')
         13 pdb_to_fasta_pb(pdb_path, 'output.fasta')
         14 


    NameError: name 'pbx' is not defined

If the sequences we want to read are spread amongst several fasta files,
then we can use the :func:`pbxplore.io.read_several_fasta` function
that takes a list of fasta file path as argument instead of a single
path.

.. code:: python

    # Write several fasta files
    pdb_to_fasta_pb(os.path.join(pbx.DEMO_DATA_PATH, '1BTA.pdb'), '1BTA.fasta')
    pdb_to_fasta_pb(os.path.join(pbx.DEMO_DATA_PATH, '2LFU.pdb'), '2FLU.fasta')

    # Read the fasta files
    names, sequences = pbx.io.read_several_fasta(['1BTA.fasta', '2FLU.fasta'])

    # Print the first entries
    print('names:')
    pprint(names[:5])
    print('sequences:')
    pprint(sequences[:5])

    !rm 1BTA.fasta 2FLU.fasta

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-13-fe5b22c077f3> in <module>()
          1 # Write several fasta files
    ----> 2 pdb_to_fasta_pb(os.path.join(pbx.DEMO_DATA_PATH, '1BTA.pdb'), '1BTA.fasta')
          3 pdb_to_fasta_pb(os.path.join(pbx.DEMO_DATA_PATH, '2LFU.pdb'), '2FLU.fasta')
          4 
          5 # Read the fasta files


    NameError: name 'pbx' is not defined

