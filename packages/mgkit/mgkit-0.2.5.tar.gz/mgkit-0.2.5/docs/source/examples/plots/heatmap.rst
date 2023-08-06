
Heatmaps
========

.. code:: python

    import mgkit.plots
    import numpy
    import pandas
    import seaborn as sns
    import matplotlib.colors


.. parsed-literal::

    /Users/francesco/dev/dev-env/lib/python2.7/site-packages/matplotlib/__init__.py:872: UserWarning: axes.color_cycle is deprecated and replaced with axes.prop_cycle; please use the latter.
      warnings.warn(self.msg_depr % (key, alt_key))


Random matrix and color map init
--------------------------------

.. code:: python

    nrow = 50
    ncol = nrow
    
    data = pandas.DataFrame(
    {
        x: numpy.random.negative_binomial(500, 0.5, nrow)
        for x in xrange(ncol)
    }
    )

.. code:: python

    sns.palplot(sns.color_palette('Blues', 9))



.. image:: heatmap_files/heatmap_4_0.png


.. code:: python

    cmap = matplotlib.colors.ListedColormap(sns.color_palette('Blues', 9))

Basic plot
----------

.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(10,10), aspect='equal')
    mgkit.plots.heatmap.baseheatmap(data, ax, cmap=cmap)




.. parsed-literal::

    <matplotlib.collections.QuadMesh at 0x10f926390>




.. image:: heatmap_files/heatmap_7_1.png


Add numbers to the heatmap
--------------------------

Default
~~~~~~~

.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(20,20))
    mgkit.plots.heatmap.baseheatmap(data.iloc[:20, :20], ax, cmap=cmap, annot=True)




.. parsed-literal::

    <matplotlib.collections.QuadMesh at 0x113413a90>




.. image:: heatmap_files/heatmap_10_1.png


Change format of numbers
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(10,10))
    mgkit.plots.heatmap.baseheatmap(
        data.iloc[:10, :10], 
        ax, 
        cmap=cmap, 
        annot=True,
        annotopts=dict(format=lambda x: "{:.1f}".format(x))
    )




.. parsed-literal::

    <matplotlib.collections.QuadMesh at 0x11d61ba90>




.. image:: heatmap_files/heatmap_12_1.png


.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(15,15))
    mgkit.plots.heatmap.baseheatmap(
        data.iloc[:20, :20], 
        ax, 
        cmap=cmap, 
        annot=True,
        annotopts=dict(
            format=lambda x: "%.1f" % x,
            fontsize=10,
            color='r'
        )
    )




.. parsed-literal::

    <matplotlib.collections.QuadMesh at 0x11e3c0950>




.. image:: heatmap_files/heatmap_13_1.png


Using Boundaries for the colors
-------------------------------

.. code:: python

    norm = matplotlib.colors.BoundaryNorm([0, 300, 500, 700, 900, 1000], cmap.N)
    
    fig, ax = mgkit.plots.get_single_figure(figsize=(10,10), aspect='equal')
    mgkit.plots.heatmap.baseheatmap(data, ax, cmap=cmap, norm=norm)




.. parsed-literal::

    <matplotlib.collections.QuadMesh at 0x1125167d0>




.. image:: heatmap_files/heatmap_15_1.png


Normalising the colors
----------------------

.. code:: python

    norm = matplotlib.colors.Normalize(vmin=400, vmax=700, clip=True)
    
    fig, ax = mgkit.plots.get_single_figure(figsize=(10,10), aspect='equal')
    mgkit.plots.heatmap.baseheatmap(data, ax, cmap=cmap, norm=norm)




.. parsed-literal::

    <matplotlib.collections.QuadMesh at 0x1128a5590>




.. image:: heatmap_files/heatmap_17_1.png


Grouping labels
~~~~~~~~~~~~~~~

.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(10,10), aspect='equal')
    mgkit.plots.heatmap.baseheatmap(data, ax, cmap=cmap)
    mgkit.plots.grouped_spine(
        [range(10), range(10, 20), range(20, 30), range(30, 40), range(40, 50)], 
        ['first', 'second', 'third', 'fourth', 'fifth'],
        ax
    )



.. image:: heatmap_files/heatmap_19_0.png


Reversing the order of the rows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(10,10), aspect='equal')
    mgkit.plots.heatmap.baseheatmap(data.loc[data.index[::-1]], ax, cmap=cmap)
    mgkit.plots.grouped_spine(
        [range(10), range(10, 20), range(20, 30), range(30, 40), range(40, 50)][::-1], 
        ['first', 'second', 'third', 'fourth', 'fifth'][::-1],
        ax
    )



.. image:: heatmap_files/heatmap_21_0.png


A dendrogram from clustering the data
-------------------------------------

Clustering rows
~~~~~~~~~~~~~~~

.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(20, 5))
    _ = mgkit.plots.heatmap.dendrogram(data, ax)



.. image:: heatmap_files/heatmap_24_0.png


Clustering colums (You need the transposed matrix)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(20, 5))
    _ = mgkit.plots.heatmap.dendrogram(data.T, ax)



.. image:: heatmap_files/heatmap_26_0.png


A simple clustered heatmap, look at the code for customisation
--------------------------------------------------------------

.. code:: python

    mgkit.plots.heatmap.heatmap_clustered(data, figsize=(20, 15), cmap=cmap)



.. image:: heatmap_files/heatmap_28_0.png

