Visualize protein deformability
===============================

.. contents:: Table of Contents
   :local:
   :backlinks: none

.. note::

   This page is initialy a jupyter notebook. You can see a `notebook HTML
   render <Deformability_.html>`__ of it or download the `notebook
   itself <Deformability.ipynb>`__.


Protein Blocks are great tools to study protein deformability. Indeed,
if the block assigned to a residue changes between two frames of a
trajectory, it represents a local deformation of the protein rather than
the displacement of the residue.

The API allows to visualize Protein Block variability throughout a
molecular dynamics simulation trajectory.

.. code:: python

    from __future__ import print_function, division
    from pprint import pprint
    from IPython.display import Image, display
    import matplotlib.pyplot as plt
    import os

    # The following line, in a jupyter notebook, allows to display
    # the figure directly in the notebook. See <https://jupyter.org/>
    %matplotlib inline

.. code:: python

    import pbxplore as pbx

::

    ---------------------------------------------------------------------------

    ImportError                               Traceback (most recent call last)

    <ipython-input-2-853cbdb98b68> in <module>()
    ----> 1 import pbxplore as pbx


    ImportError: No module named pbxplore

Here we will look at a molecular dynamics simulation of the barstar. As
we will analyse Protein Block sequences, we first need to assign these
sequences for each frame of the trajectory.

.. code:: python

    # Assign PB sequences for all frames of a trajectory
    trajectory = os.path.join(pbx.DEMO_DATA_PATH, 'barstar_md_traj.xtc')
    topology = os.path.join(pbx.DEMO_DATA_PATH, 'barstar_md_traj.gro')
    sequences = []
    for chain_name, chain in pbx.chains_from_trajectory(trajectory, topology):
        dihedrals = chain.get_phi_psi_angles()
        pb_seq = pbx.assign(dihedrals)
        sequences.append(pb_seq)

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-3-495e579af03b> in <module>()
          1 # Assign PB sequences for all frames of a trajectory
    ----> 2 trajectory = os.path.join(pbx.DEMO_DATA_PATH, 'barstar_md_traj.xtc')
          3 topology = os.path.join(pbx.DEMO_DATA_PATH, 'barstar_md_traj.gro')
          4 sequences = []
          5 for chain_name, chain in pbx.chains_from_trajectory(trajectory, topology):


    NameError: name 'pbx' is not defined

Block occurences per position
-----------------------------

The basic information we need to analyse protein deformability is the
count of occurences of each PB for each position throughout the
trajectory. This occurence matrix can be calculated with the
:func:`pbxplore.analysis.count_matrix` function.

.. code:: python

    count_matrix = pbx.analysis.count_matrix(sequences)

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-4-25d9f2aed9b5> in <module>()
    ----> 1 count_matrix = pbx.analysis.count_matrix(sequences)


    NameError: name 'pbx' is not defined

``count_matrix`` is a numpy array with one row per PB and one column per
position. In each cell is the number of time a position was assigned to
a PB.

We can visualize ``count_matrix`` using Matplotlib as any 2D numpy
array.

.. code:: python

    im = plt.imshow(count_matrix, interpolation='none', aspect='auto')
    plt.colorbar(im)
    plt.xlabel('Position')
    plt.ylabel('Block')

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-5-2544c1e550cd> in <module>()
    ----> 1 im = plt.imshow(count_matrix, interpolation='none', aspect='auto')
          2 plt.colorbar(im)
          3 plt.xlabel('Position')
          4 plt.ylabel('Block')


    NameError: name 'count_matrix' is not defined

PBxplore provides the :func:`pbxplore.analysis.plot_map` function to
ease the visualization of the occurence matrix.

.. code:: python

    pbx.analysis.plot_map('map.png', count_matrix)
    !rm map.png

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-6-89cb23d2983b> in <module>()
    ----> 1 pbx.analysis.plot_map('map.png', count_matrix)
          2 get_ipython().system(u'rm map.png')


    NameError: name 'pbx' is not defined

The :func:`pbxplore.analysis.plot_map` helper has a ``residue_min``
and a ``residue_max`` optional arguments to display only part of the
matrix. These two arguments can be pass to all PBxplore functions that
produce a figure.

.. code:: python

    pbx.analysis.plot_map('map.png', count_matrix,
                          residue_min=60, residue_max=70)
    !rm map.png

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-7-d2cdc6435a50> in <module>()
    ----> 1 pbx.analysis.plot_map('map.png', count_matrix,
          2                       residue_min=60, residue_max=70)
          3 get_ipython().system(u'rm map.png')


    NameError: name 'pbx' is not defined

Note that matrix in the the figure produced by
:func:`pbxplore.analysis.plot_map` is normalized so as the sum of each
column is 1. The matrix can be normalized with the
:func:`pbxplore.analysis.compute_freq_matrix`.

.. code:: python

    freq_matrix = pbx.analysis.compute_freq_matrix(count_matrix)

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-8-65ead41a37b6> in <module>()
    ----> 1 freq_matrix = pbx.analysis.compute_freq_matrix(count_matrix)


    NameError: name 'pbx' is not defined

.. code:: python

    im = plt.imshow(freq_matrix, interpolation='none', aspect='auto')
    plt.colorbar(im)
    plt.xlabel('Position')
    plt.ylabel('Block')

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-9-81cb853faf4a> in <module>()
    ----> 1 im = plt.imshow(freq_matrix, interpolation='none', aspect='auto')
          2 plt.colorbar(im)
          3 plt.xlabel('Position')
          4 plt.ylabel('Block')


    NameError: name 'freq_matrix' is not defined

Protein Block entropy
---------------------

The :math:`N_{eq}` is a measure of variability based on the count matrix
calculated above. It can be computed with the
:func:`pbxplore.analysis.compute_neq` function.

.. code:: python

    neq_by_position = pbx.analysis.compute_neq(count_matrix)

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-10-7eeb19d961f7> in <module>()
    ----> 1 neq_by_position = pbx.analysis.compute_neq(count_matrix)


    NameError: name 'pbx' is not defined

``neq_by_position`` is a 1D numpy array with the :math:`N_{eq}` for each
residue.

.. code:: python

    plt.plot(neq_by_position)
    plt.xlabel('Position')
    plt.ylabel('$N_{eq}$')

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-11-b3b064739482> in <module>()
    ----> 1 plt.plot(neq_by_position)
          2 plt.xlabel('Position')
          3 plt.ylabel('$N_{eq}$')


    NameError: name 'neq_by_position' is not defined

The :func:`pbxplore.analysis.plot_neq` helper ease the plotting of the
:math:`N_{eq}`.

.. code:: python

    pbx.analysis.plot_neq('neq.png', neq_by_position)
    !rm neq.png

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-12-f4134ffa3fff> in <module>()
    ----> 1 pbx.analysis.plot_neq('neq.png', neq_by_position)
          2 get_ipython().system(u'rm neq.png')


    NameError: name 'pbx' is not defined

The ``residue_min`` and ``residue_max`` arguments are available.

.. code:: python

    pbx.analysis.plot_neq('neq.png', neq_by_position,
                          residue_min=60, residue_max=70)
    !rm neq.png

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-13-d9fd90e1d17b> in <module>()
    ----> 1 pbx.analysis.plot_neq('neq.png', neq_by_position,
          2                       residue_min=60, residue_max=70)
          3 get_ipython().system(u'rm neq.png')


    NameError: name 'pbx' is not defined

Display PB variability as a logo
--------------------------------

.. code:: python

    pbx.analysis.generate_weblogo('logo.png', count_matrix)
    display(Image('logo.png'))
    !rm logo.png

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-14-a4d44c0d9f48> in <module>()
    ----> 1 pbx.analysis.generate_weblogo('logo.png', count_matrix)
          2 display(Image('logo.png'))
          3 get_ipython().system(u'rm logo.png')


    NameError: name 'pbx' is not defined

.. code:: python

    pbx.analysis.generate_weblogo('logo.png', count_matrix,
                                  residue_min=60, residue_max=70)
    display(Image('logo.png'))
    !rm logo.png

::

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-15-ae0b8a456c34> in <module>()
    ----> 1 pbx.analysis.generate_weblogo('logo.png', count_matrix,
          2                               residue_min=60, residue_max=70)
          3 display(Image('logo.png'))
          4 get_ipython().system(u'rm logo.png')


    NameError: name 'pbx' is not defined

