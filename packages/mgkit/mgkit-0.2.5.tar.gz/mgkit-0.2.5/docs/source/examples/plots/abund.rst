
Abundance Plots
===============

.. code:: python

    import numpy
    import mgkit.plots
    import mgkit.plots.abund
    import seaborn as sns
    import pandas as pd

.. code:: python

    n = 10
    p = 0.50
    size = 20

.. code:: python

    data = pd.DataFrame({
        'S1': numpy.random.negative_binomial(n, p, size), 
        'S2': numpy.random.negative_binomial(n, p + 0.1, size),
        'S3': numpy.random.negative_binomial(n, p - 0.1, size),
    })

Triangle Plot
-------------

Grid
~~~~

.. code:: python

    # First we need to draw the triangle grid
    # aspect should be equal to ensure that the triangle sides have the same length
    fig, ax = mgkit.plots.get_single_figure(figsize=(10, 10), aspect='equal')
    # the labels passed are first drawn from bottom-left, then bottom-right and finally top
    mgkit.plots.abund.draw_triangle_grid(ax, labels=data.columns)



.. image:: abund_files/abund_6_0.png


.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(10, 10), aspect='equal')
    # the style can be customised by passing the appropriate matplotlib line markers with the styles parameter
    mgkit.plots.abund.draw_triangle_grid(ax, labels=data.columns, styles=['--', '-.', '-'])



.. image:: abund_files/abund_7_0.png


.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(10, 10), aspect='equal')
    # The axis can be set to solid lines and the internals to dotted by passing None as styles value
    mgkit.plots.abund.draw_triangle_grid(ax, labels=data.columns, styles=None)



.. image:: abund_files/abund_8_0.png


Plot
~~~~

.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(10, 10), aspect='equal')
    mgkit.plots.abund.draw_triangle_grid(ax, labels=data.columns)
    # this function accept matrices with either two or three columns
    mgkit.plots.abund.draw_circles(ax, data)




.. parsed-literal::

    <matplotlib.collections.PathCollection at 0x10e369c50>




.. image:: abund_files/abund_10_1.png


.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(10, 10), aspect='equal')
    mgkit.plots.abund.draw_triangle_grid(ax, labels=data.columns)
    # col_func is any function that accept a value (an element of data.index) and returns a valid matplotlib color for it
    col_func = lambda x: sns.color_palette('hls', len(data))[x]
    mgkit.plots.abund.draw_circles(ax, data, col_func=col_func)




.. parsed-literal::

    <matplotlib.collections.PathCollection at 0x10e8a9650>




.. image:: abund_files/abund_11_1.png


.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(10, 10), aspect='equal')
    mgkit.plots.abund.draw_triangle_grid(ax, labels=data.columns)
    # csize is the base size for the circle
    mgkit.plots.abund.draw_circles(ax, data, col_func=col_func, csize=500)




.. parsed-literal::

    <matplotlib.collections.PathCollection at 0x10ed8e790>




.. image:: abund_files/abund_12_1.png


.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(10, 10), aspect='equal')
    mgkit.plots.abund.draw_triangle_grid(ax, labels=data.columns)
    # the sizescale parameter allows to specify a size factor for each row that is multiplied to the csize parameter
    sizescale = pd.Series(numpy.random.random(20) * 3)
    mgkit.plots.abund.draw_circles(
        ax, 
        data, 
        col_func=lambda x: sns.color_palette('hls', len(data))[x], 
        csize=500, 
        sizescale=sizescale
    )




.. parsed-literal::

    <matplotlib.collections.PathCollection at 0x10d400190>




.. image:: abund_files/abund_13_1.png


.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(10, 10), aspect='equal')
    mgkit.plots.abund.draw_triangle_grid(ax, labels=data.columns)
    # the order parameter can be used to only plot only a subset of the point
    mgkit.plots.abund.draw_circles(
        ax, 
        data, 
        col_func=col_func, 
        csize=500, 
        sizescale=sizescale,
        order=data.index[:10]
    )




.. parsed-literal::

    <matplotlib.collections.PathCollection at 0x10de6ac90>




.. image:: abund_files/abund_14_1.png


.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(10, 10), aspect='equal')
    mgkit.plots.abund.draw_triangle_grid(ax, labels=data.columns)
    # or also to make sure bigger circles are drawn first, below smaller ones
    mgkit.plots.abund.draw_circles(
        ax, 
        data, 
        col_func=col_func, 
        csize=500, 
        sizescale=sizescale,
        order=sizescale.sort(ascending=False, inplace=False).index
    )


.. parsed-literal::

    /Users/francesco/dev/dev-env/lib/python2.7/site-packages/ipykernel/__main__.py:10: FutureWarning: sort is deprecated, use sort_values(inplace=True) for for INPLACE sorting




.. parsed-literal::

    <matplotlib.collections.PathCollection at 0x10d873250>




.. image:: abund_files/abund_15_2.png


.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(10, 10), aspect='equal')
    mgkit.plots.abund.draw_triangle_grid(ax, labels=data.columns)
    # trasparency of circles can be adjusted with the alpha parameter (between 0 and 1)
    mgkit.plots.abund.draw_circles(
        ax, 
        data, 
        col_func=col_func, 
        csize=500, 
        sizescale=sizescale,
        order=sizescale.sort(ascending=False, inplace=False).index,
        alpha=1
    )


.. parsed-literal::

    /Users/francesco/dev/dev-env/lib/python2.7/site-packages/ipykernel/__main__.py:10: FutureWarning: sort is deprecated, use sort_values(inplace=True) for for INPLACE sorting




.. parsed-literal::

    <matplotlib.collections.PathCollection at 0x10f346750>




.. image:: abund_files/abund_16_2.png


.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(10, 10), aspect='equal')
    mgkit.plots.abund.draw_triangle_grid(ax, labels=data.columns)
    # if lines are required around the circles, linewidths and edgecolor can be used to customise them
    mgkit.plots.abund.draw_circles(
        ax, 
        data, 
        col_func=col_func, 
        csize=500, 
        sizescale=sizescale,
        order=sizescale.sort(ascending=False, inplace=False).index,
        linewidths=1,
        edgecolor='k'
    )


.. parsed-literal::

    /Users/francesco/dev/dev-env/lib/python2.7/site-packages/ipykernel/__main__.py:10: FutureWarning: sort is deprecated, use sort_values(inplace=True) for for INPLACE sorting




.. parsed-literal::

    <matplotlib.collections.PathCollection at 0x10f829c50>




.. image:: abund_files/abund_17_2.png


Abundance Plot with 2 Samples
-----------------------------

Grid
~~~~

.. code:: python

    # First we need to draw the 1D grid
    # aspect should be set to make sure the correct aspect ratio is drawn
    fig, ax = mgkit.plots.get_single_figure(figsize=(10, 3), aspect=0.1)
    # the labels passed are drawn from left to right
    mgkit.plots.abund.draw_1d_grid(ax, labels=data.columns[:2])



.. image:: abund_files/abund_20_0.png


.. code:: python

    fig, ax = mgkit.plots.get_single_figure(figsize=(10, 3), aspect=0.1)
    mgkit.plots.abund.draw_1d_grid(ax, labels=data.columns[:2])
    mgkit.plots.abund.draw_circles(
        ax, 
        data.icol([0,1]), 
        col_func=col_func, 
        csize=500, 
        sizescale=sizescale,
        order=sizescale.sort(ascending=False, inplace=False).index,
        linewidths=1,
        edgecolor='k'
    )


.. parsed-literal::

    /Users/francesco/dev/dev-env/lib/python2.7/site-packages/ipykernel/__main__.py:5: FutureWarning: icol(i) is deprecated. Please use .iloc[:,i]
    /Users/francesco/dev/dev-env/lib/python2.7/site-packages/ipykernel/__main__.py:9: FutureWarning: sort is deprecated, use sort_values(inplace=True) for for INPLACE sorting




.. parsed-literal::

    <matplotlib.collections.PathCollection at 0x1108923d0>




.. image:: abund_files/abund_21_2.png

