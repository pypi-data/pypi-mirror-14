PB assignation
==============

.. contents:: Table of Contents
   :local:
   :backlinks: none

.. note::

   This page is initialy a jupyter notebook. You can see a `notebook HTML
   render <Assignement_.html>`__ of it or download the `notebook
   itself <Assignement.ipynb>`__.


We hereby demonstrate how to use the API to assign PB sequences.

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

Use the built-in structure parser
---------------------------------

Assign PB for a single structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :func:`pbxplore.chains_from_files` function is the prefered way to
read PDB and PDBx/mmCIF files using PBxplore. This function takes a list
of file path as argument, and yield each chain it can read from these
files. It provides a single interface to read PDB and PDBx/mmCIF files,
to read single model and multimodel files, and to read a single file of
a collection of files.

Here we want to read a single file with a single model and a single
chain. Therefore, we need the first and only record that is yield by
:func:`pbxplore.chains_from_files`. This record contains a name for
the chain, and the chain itself as a
:class:`pbxplore.structure.structure.Chain` object. Note that, even if
we want to read a single file, we need to provide it as a list to
:func:`pbxplore.chains_from_files`.

.. code:: python

    pdb_path = os.path.join(pbx.DEMO_DATA_PATH, '1BTA.pdb')
    structure_reader = pbx.chains_from_files([pdb_path])
    chain_name, chain = next(structure_reader)
    print(chain_name)
    print(chain)

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-3-8a9163a9b9bb> in <module>()
    ----> 1 pdb_path = os.path.join(pbx.DEMO_DATA_PATH, '1BTA.pdb')
          2 structure_reader = pbx.chains_from_files([pdb_path])
          3 chain_name, chain = next(structure_reader)
          4 print(chain_name)
          5 print(chain)


    NameError: name 'pbx' is not defined

Protein Blocks are assigned based on the dihedral angles of the
backbone. So we need to calculate them. The
:meth:`pbxplore.structure.structure.Chain.get_phi_psi_angles` methods
calculate these angles and return them in a form that can be directly
provided to the assignement function.

The dihedral angles are returned as a dictionnary. Each key of this
dictionary is a residue number, and each value is a dictionary with the
phi and psi angles.

.. code:: python

    dihedrals = chain.get_phi_psi_angles()
    pprint(dihedrals)

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-4-9cf0a8bc4086> in <module>()
    ----> 1 dihedrals = chain.get_phi_psi_angles()
          2 pprint(dihedrals)


    NameError: name 'chain' is not defined

The dihedral angles can be provided to the :func:`pbxplore.assign`
function that assigns a Protein Block to each residue, and that returns
the PB sequence as a string. Note that the first and last two residues
are assigned to the ``Z`` jocker block as some dihedral angles cannot be
calculated.

.. code:: python

    pb_seq = pbx.assign(dihedrals)
    print(pb_seq)

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-5-71c7132535bf> in <module>()
    ----> 1 pb_seq = pbx.assign(dihedrals)
          2 print(pb_seq)


    NameError: name 'pbx' is not defined

Assign PB for several models of a single file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A single PDB file can contain several models. Then, we do not want to
read only the first chain. Instead, we want to iterate over all the
chains.

.. code:: python

    pdb_path = os.path.join(pbx.DEMO_DATA_PATH, '2LFU.pdb')
    for chain_name, chain in pbx.chains_from_files([pdb_path]):
        dihedrals = chain.get_phi_psi_angles()
        pb_seq = pbx.assign(dihedrals)
        print('* {}'.format(chain_name))
        print('  {}'.format(pb_seq))

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-6-378e76790064> in <module>()
    ----> 1 pdb_path = os.path.join(pbx.DEMO_DATA_PATH, '2LFU.pdb')
          2 for chain_name, chain in pbx.chains_from_files([pdb_path]):
          3     dihedrals = chain.get_phi_psi_angles()
          4     pb_seq = pbx.assign(dihedrals)
          5     print('* {}'.format(chain_name))


    NameError: name 'pbx' is not defined

Assign PB for a set of structures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :func:`pbxplore.chains_from_files` function can also handle
several chains from several files.

.. code:: python

    import glob
    files = [os.path.join(pbx.DEMO_DATA_PATH, pdb_name)
             for pdb_name in ('1BTA.pdb', '2LFU.pdb', '3ICH.pdb')]
    print('The following files will be used:')
    pprint(files)
    for chain_name, chain in pbx.chains_from_files(files):
        dihedrals = chain.get_phi_psi_angles()
        pb_seq = pbx.assign(dihedrals)
        print('* {}'.format(chain_name))
        print('  {}'.format(pb_seq))

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-7-73672ce266c9> in <module>()
          1 import glob
          2 files = [os.path.join(pbx.DEMO_DATA_PATH, pdb_name)
    ----> 3          for pdb_name in ('1BTA.pdb', '2LFU.pdb', '3ICH.pdb')]
          4 print('The following files will be used:')
          5 pprint(files)


    NameError: name 'pbx' is not defined

Assign PB for frames in a trajectory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PB sequences can be assigned from a trajectory. To do so, we use the
:func:`pbxplore.chains_from_trajectory` function that takes the path
to a trajectory and the path to the corresponding topology as argument.
Any file formats readable by MDAnalysis can be used. Except for its
arguments, :func:`pbxplore.chains_from_trajectory` works the same as
:func:`pbxplore.chains_from_files`.

\*\* Note that MDAnalysis is required to use this feature. \*\*

.. code:: python

    trajectory = os.path.join(pbx.DEMO_DATA_PATH, 'barstar_md_traj.xtc')
    topology = os.path.join(pbx.DEMO_DATA_PATH, 'barstar_md_traj.gro')
    for chain_name, chain in pbx.chains_from_trajectory(trajectory, topology):
        dihedrals = chain.get_phi_psi_angles()
        pb_seq = pbx.assign(dihedrals)
        print('* {}'.format(chain_name))
        print('  {}'.format(pb_seq))

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-8-5c7dfa551061> in <module>()
    ----> 1 trajectory = os.path.join(pbx.DEMO_DATA_PATH, 'barstar_md_traj.xtc')
          2 topology = os.path.join(pbx.DEMO_DATA_PATH, 'barstar_md_traj.gro')
          3 for chain_name, chain in pbx.chains_from_trajectory(trajectory, topology):
          4     dihedrals = chain.get_phi_psi_angles()
          5     pb_seq = pbx.assign(dihedrals)


    NameError: name 'pbx' is not defined

Use a different structure parser
--------------------------------

Providing the dihedral angles can be formated as expected by
:func:`pbxplore.assign`, the source of these angles does not matter.
For instance, other PDB parser can be used with PBxplore.

BioPython
~~~~~~~~~

.. code:: python

    import Bio.PDB
    import math

    pdb_path = os.path.join(pbx.DEMO_DATA_PATH, "2LFU.pdb")
    for model in Bio.PDB.PDBParser().get_structure("2LFU", pdb_path):
        for chain in model:
            polypeptides = Bio.PDB.PPBuilder().build_peptides(chain)
            for poly_index, poly in enumerate(polypeptides):
                dihedral_list = poly.get_phi_psi_list()
                dihedrals = {}
                for resid, (phi, psi) in enumerate(dihedral_list, start=1):
                    if not phi is None:
                        phi = 180 * phi / math.pi
                    if not psi is None:
                        psi = 180 * psi / math.pi
                    dihedrals[resid] = {'phi': phi, 'psi': psi}
            print(model, chain)
            pb_seq = pbx.assign(dihedrals)
            print(pb_seq)

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-9-7d6a63049325> in <module>()
          2 import math
          3 
    ----> 4 pdb_path = os.path.join(pbx.DEMO_DATA_PATH, "2LFU.pdb")
          5 for model in Bio.PDB.PDBParser().get_structure("2LFU", pdb_path):
          6     for chain in model:


    NameError: name 'pbx' is not defined

