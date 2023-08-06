
# coding: utf-8

# # HMMER Tutorial - Exploring the Data

# The HMMER tutorial should be completed or a copy of the data downloaded ([figshare](http://files.figshare.com/2599149/tutorial_hmmer_data.zip)) and uncompressed. The followind variable can be used to change the default location.

# In[1]:

# Directory where the tutorial data is found
data_dir = 'tutorial-hmmer-data/'


# ## Imports

# In[2]:

from __future__ import print_function

#Python Standard Library
import glob
import pickle
import sys
import itertools

#External Dependencies (install via pip or anaconda)

# Check if running interactively or not
import matplotlib as mpl # http://matplotlib.org
# from:
# http://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
# and
# http://stackoverflow.com/questions/15455029/python-matplotlib-agg-vs-interactive-plotting-and-tight-layout
import __main__ as main
if hasattr(main, '__file__'):
    # Non interactive, force the use of Agg backend instead
    # of the default one
    mpl.use('Agg')

import numpy # http://www.numpy.org
import pandas # http://pandas.pydata.org
import seaborn # http://stanford.edu/~mwaskom/software/seaborn/
import scipy # http://www.scipy.org
import matplotlib.pyplot as plt 


#MGKit Import
from mgkit.io import gff, fasta
from mgkit.mappings import eggnog
import mgkit.counts, mgkit.taxon, mgkit.snps, mgkit.plots
import mgkit.snps
import mgkit.mappings.enzyme
import mgkit.net.uniprot
import mgkit.utils.dictionary
import mgkit.kegg


# In[3]:

mgkit.logger.config_log()


# In[4]:

mgkit.cite(sys.stdout)


# ## Reads Data

# In[5]:

# This file contains the SNPs information and it is the output
# of the snp_parser script
snp_data = pickle.load(open('{}snp_data.pickle'.format(data_dir), 'r'))


# In[6]:

# Taxonomy needs to be download beforehand. It is loaded into an an
# instance of mgkit.taxon.UniprotTaxonomy. It is used in filtering
# data and to map taxon IDs to different levels in the taxonomy
taxonomy = mgkit.taxon.UniprotTaxonomy('{}mg_data/taxonomy.pickle'.format(data_dir))


# In[7]:

# Loads all annotations in a dictionary, with the unique ID (uid) as key
# and the mgkit.io.gff.Annotation instance that represent the line in the
# GFF file as value
annotations = {x.uid: x for x in gff.parse_gff('{}assembly.filt.cov.gff'.format(data_dir))}


# In[8]:

# Sample names
sample_names = {
    'I': "Influent",
    'B': "Buffering",
    'SA': "Secondary aeration",
    'PA': "Primary aeration",
    'SD': "Sludge digestion",
}


# ## Explore Taxa Diversity
# 
# Diversity in metagenomic samples can be analysed using pN/pS values. The data required to do this was produced in the tutorial by the *snp_parser* script. Here are some examples of how to calculate diversity estimates from this data.
# 
# The complete toolset to map diversity estimates can be found in the **mgkit.snps** package, with the *mgkit.snps.funcs.combine_sample_snps* function building the final pandas DataFrame. As the use of the function requires the initialisation of different functions, a few easier to use ones are available in the **mgkit.snps.conv_func** module:
# 
# * get_rank_dataframe
# * get_gene_map_dataframe
# * get_full_dataframe
# * get_gene_taxon_dataframe
# 
# The first is used to get diversity estimates for taxa, the second for genes/functions. The other two provides functionality to return estimates tied to both taxon and function.

# In[9]:

# Sets the minimum coverage for an annotation to be
# included into the table (defaults to 4)
mgkit.consts.DEFAULT_SNP_FILTER['min_cov'] = 4


# In[10]:

# To get diversity estimates for taxa *mgkit.snps.conv_func.get_rank_dataframe* can be used
# It is also imported and accesible from the *mgkit.snps* package
# ATTENTION: the lowest rank that can be used is *order*, since that's the level that was
# used when the profiles were created
pnps = mgkit.snps.get_rank_dataframe(snp_data, taxonomy, min_num=3, rank='order', index_type='taxon')


# In[11]:

# Renaming the columns and rows
pnps = pnps.rename(
    columns=sample_names,
    index=lambda x: taxonomy[x].s_name.capitalize()
)


# In[12]:

# The dataframe exposes a method that print a table with some basic statistics
pnps.describe()


# In[13]:

# The complete table
pnps


# In[14]:

# sort the DataFrame to plot them by mean value
# older versions of pandas have a *sort* method instead of a *sort_values*
plot_order = pnps.mean(axis=1).sort_values(inplace=False, ascending=False).index

# A matplotlib single figure (sizes are in inches) can be created via a function in mgkit
fig, ax = mgkit.plots.get_single_figure(figsize=(10, 25))

# This function uses the boxplot function in matplotlib, adding some easier to use functionality
_ = mgkit.plots.boxplot.boxplot_dataframe(
    pnps,
    plot_order, 
    ax,
    # By default the function renders the boxplot vertical.
    box_vert=False,
    # some fonts settings, note the *rotation* key, it refers to the rotation of the 
    # labels for the taxa names. The default is vertical, as the boxplot order above
    fonts=dict(fontsize=14, rotation='horizontal'),
    # the colours are generated with hls color palette, for the number of rows in the
    # DataFrame
    data_colours={
        x: color
        for x, color in zip(plot_order, seaborn.color_palette('hls', len(pnps.index)))
    }
)

# Taxa names should be in italics
for text in ax.get_yticklabels():
    text.set_fontstyle('italic')

# It sets the axes labels
_ = ax.set_xlabel('pN/pS', fontsize=16)
_ = ax.set_ylabel('Order', fontsize=16)


# ### Phylum Level Diversity
# 
# Even if it was chosen the *Order* as rank for the profiles, a higher level represantation can be obtained.

# In[15]:

# The only difference is the *rank* chosen and the size of the plot
pnps = mgkit.snps.get_rank_dataframe(snp_data, taxonomy, min_num=3, rank='phylum', index_type='taxon')

pnps = pnps.rename(
    columns=sample_names,
    index=lambda x: taxonomy[x].s_name.capitalize()
)
#sort the DataFrame to plot them by mean value
plot_order = pnps.mean(axis=1).sort_values(inplace=False, ascending=False).index

fig, ax = mgkit.plots.get_single_figure(figsize=(10, 10))
_ = mgkit.plots.boxplot.boxplot_dataframe(
    pnps, 
    plot_order, 
    ax, 
    fonts=dict(fontsize=14, rotation='horizontal'),
    data_colours={
        x: color
        for x, color in zip(plot_order, seaborn.color_palette('hls', len(pnps.index)))
    },
    box_vert=False
)
_ = ax.set_xlabel('pN/pS', fontsize=16)
_ = ax.set_ylabel('Phylum', fontsize=16)

# Taxa names should be in italics
for text in ax.get_yticklabels():
    text.set_fontstyle('italic')


# ## Using eggNOG and Functional Categories

# ### Loading eggNOG Data

# In[16]:

# This class allow the mapping of eggNOG identifiers to Functional Categories
eg = eggnog.NOGInfo()
# Just a few to speed up the analysis, but other can be used
# Should have been downloaded by the full tutorial script
eg.load_members('{}map_data/COG.members.txt.gz'.format(data_dir))
eg.load_members('{}map_data/NOG.members.txt.gz'.format(data_dir))
eg.load_funccat('{}map_data/COG.funccat.txt.gz'.format(data_dir))
eg.load_funccat('{}map_data/NOG.funccat.txt.gz'.format(data_dir))


# ### Download KO to eggNOG Mappings

# To use functional categories a mapping from KO identifiers to eggNOG ones is needed. There's no direct path to get this, but one way is to get the mappings from KO to Uniprot identifiers and the mappings from the resulting Uniprot identifiers to eggNOG identifiers. In MGKit, the *net* package contains modules to use network resources. In particular, the *mgkit.net.uniprot* can be used to query Uniprot and also map identifiers.

# In[17]:

# All gene_id properties of the annotations are put in a *set* to remove duplicates
ko_up = mgkit.net.uniprot.get_mappings(
    {annotation.gene_id for annotation in annotations.itervalues()}, 
    db_from='KO_ID', db_to='ID'
)
# While a complex expression, the *set* generation involves the iteration of all values from
# the *ko_up* dictionary to eliminate the duplicates
up_eg = mgkit.net.uniprot.get_mappings(
    set(itertools.chain(*(values for values in ko_up.itervalues()))), 
    db_from='ID', db_to='EGGNOG_ID'
)


# After obtaining the two dictionaries in the correct order, a mapping dictionary can be produced with the *mgkit.utils.dictionary.combine_dict* function. This will produce a direct KO to eggNOG identifiers map.

# In[18]:

ko_eg_map = mgkit.utils.dictionary.combine_dict(ko_up, up_eg)


# Since we now have the KO to eggNOG mapping, we can associate to each KO identifier, the functional categories

# In[19]:

#Build mapping KO IDs -> eggNOG functional categories
fc_map = {
    # notice that we use the *ko_eg_map*
    annotation.gene_id: eg.get_nogs_funccat(ko_eg_map[annotation.gene_id])
    for annotation in annotations.itervalues()
}


# #### Saving the Mappings

# It is possible to store the mapping we saved in the GFF with the following

# In[20]:

# This will add the mappings to the annotations
for annotation in annotations.itervalues():
    annotation.set_mapping('eggnog', ko_eg_map[annotation.gene_id])


# In[21]:

# And they are now available
annotations[annotations.keys()[0]].get_mapping('eggnog')


# In[22]:

# The GFF file needs to be saved
with open('{}assembly.filt.cov.eggnog.gff'.format(data_dir), 'w') as fh:
    for annotation in annotations.itervalues():
        annotation.to_file(fh)


# In[23]:

# You can notice that the *map_EGGNOG* attribute was added to disk
print(open("{}assembly.filt.cov.eggnog.gff".format(data_dir)).readline())


# ### Create FC DataFrame

# In[24]:

# The creation of the DataFrame for a gene is straight forward, by using the KO to FC map
eg_pnps = mgkit.snps.get_gene_map_dataframe(snp_data, taxonomy, min_num=3, gene_map=fc_map, index_type='gene')


# In[25]:

# Renames rows/columns
eg_pnps = eg_pnps.rename(
    columns=sample_names,
    index=eggnog.EGGNOG_CAT
)


# In[26]:

eg_pnps.describe()


# In[27]:

eg_pnps


# #### Plot the Distributions

# In[28]:

#sort the DataFrame to plot them by mean value
plot_order = eg_pnps.mean(axis=1).sort_values(inplace=False, ascending=False).index

fig, ax = mgkit.plots.get_single_figure(figsize=(10, 10))
_ = mgkit.plots.boxplot.boxplot_dataframe(
    eg_pnps, 
    plot_order, 
    ax, 
    fonts=dict(fontsize=14, rotation='horizontal'),
    data_colours={
        x: color
        for x, color in zip(plot_order, seaborn.color_palette('hls', len(eg_pnps.index)))
    },
    box_vert=False
)
_ = ax.set_xlabel('pN/pS', fontsize=16)
_ = ax.set_ylabel('Functional Category', fontsize=16)


# #### Plot Distributions as KDE
# 
# Some better profiling can be found using the a KDE (Kernel Density Estimation). Seaborn makes it easy to plot it and it is easy to see that the Influent (first part) and Sludge digestion (last part) have a wider distribution of diversity estimates.

# In[29]:

fig, ax = mgkit.plots.get_single_figure(figsize=(20, 20))

seaborn.set(font_scale=2)

for figid, (sample, color) in enumerate(zip(eg_pnps.columns, seaborn.color_palette('Set1', len(eg_pnps.columns)))):
    seaborn.kdeplot(eg_pnps[sample].dropna(), ax=ax, color=color, shade=True)


# ## Using Enzyme Classification
# 
# The enzyme classification mappings can be retrieved directly from KO identifiers using the Kegg REST API. MGKit provides a class that makes this easy to do.

# In[30]:

# The first step is to instance the Kegg client class
kclient = mgkit.kegg.KeggClientRest()


# In[31]:

# the *link_ids* is use to link any kind of identifiers within the Kegg DB. The first argument
# of the method is the target, in our case *ec*, for the enzyme classification and the second
# argument is the list of identifiers to map. To reduce the size of the query and because it would
# be redundant anyway, we can use a set for all annotations gene_id attribute we have.
ec_map = kclient.link_ids('ec', set(annotation.gene_id for annotation in annotations.itervalues()))


# In[32]:

# You can see that for each KO identifier, a list of enzyme identifiers is returned
ec_map['K00260']


# In[33]:

ec_pnps = mgkit.snps.get_gene_map_dataframe(snp_data, taxonomy, min_num=3, gene_map=ec_map, index_type='gene')


# In[34]:

# The enzyme classification naming is verbose, so it's better not to rename the rows
ec_pnps = ec_pnps.rename(columns=sample_names)


# ### Distributions of EC

# In[35]:

fig, ax = mgkit.plots.get_single_figure(figsize=(20, 20))

seaborn.set(font_scale=2)

for figid, (sample, color) in enumerate(zip(ec_pnps.columns, seaborn.color_palette('Set1', len(ec_pnps.columns)))):
    seaborn.kdeplot(ec_pnps[sample].dropna(), ax=ax, color=color, shade=True)


# In[36]:

#sort the DataFrame to plot them by mean value
plot_order = ec_pnps.mean(axis=1).sort_values(inplace=False, ascending=False).index

fig, ax = mgkit.plots.get_single_figure(figsize=(10, 10))
_ = mgkit.plots.boxplot.boxplot_dataframe(
    ec_pnps, 
    plot_order, 
    ax, 
    fonts=dict(fontsize=14, rotation='horizontal'),
    data_colours={
        x: color
        for x, color in zip(plot_order, seaborn.color_palette('hls', len(ec_pnps.index)))
    },
    box_vert=False
)
_ = ax.set_xlabel('pN/pS', fontsize=16)
_ = ax.set_ylabel('EC', fontsize=16)


# #### Adding full names to the enzymes
# 
# A dictionary with EC names (enzclass.txt) must be collected from expasy, at the following [address](ftp://ftp.expasy.org/databases/enzyme/enzclass.txt)

# In[37]:

# The names of all EC identifiers can be obtained from expasy
ec_names = mgkit.mappings.enzyme.parse_expasy_file("{}map_data/enzclass.txt".format(data_dir))


# In[38]:

reload(mgkit.mappings.enzyme)


# In[39]:

#sort the DataFrame to plot them by mean value
plot_order = ec_pnps.mean(axis=1).sort_values(inplace=False, ascending=False).index

fig, ax = mgkit.plots.get_single_figure(figsize=(15, 25))
_ = mgkit.plots.boxplot.boxplot_dataframe(
    ec_pnps, 
    plot_order,
    ax, 
    fonts=dict(fontsize=14, rotation='horizontal'),
    data_colours={
        x: color
        for x, color in zip(plot_order, seaborn.color_palette('hls', len(ec_pnps.index)))
    },
    box_vert=False,
    
    label_map={
        ec_id: "{} - {}".format(
            ec_id,
            mgkit.mappings.enzyme.get_enzyme_full_name(ec_id, ec_names, ',\n')
        )
        for ec_id in plot_order
    }
)
_ = ax.set_xlabel('pN/pS', fontsize=16)
_ = ax.set_ylabel('EC', fontsize=16)


# ## Using a Full Gene/Taxon DataFrame
# 
# It possible to use data at the most specific level, by using the **mgkit.snps.conv_func.get_full_dataframe** function.  This can be used to have a detail view of diversity in each taxon. In this tutorial, the gene will be from **Kegg  Ortholog**, while the most specific taxonomic level is the **Order**.
# 
# In our case, the output of the function will be a DataFrame with a *Multindex* for the *index*. This allows selective sorting, as it will be showed.

# In[40]:

dataframe = mgkit.snps.conv_func.get_full_dataframe(snp_data, taxonomy)


# It's better not to rename the colummns/rows until the desired sorting is achieved
# the sorting can not be possible if any duplicated key (gene, taxon) is found

# In[41]:

# Change the sorting by taxon, gene
dataframe.reorder_levels(['taxon', 'gene']).sort_index()


# To get an idea of how many taxa the DataFrame has, we can use the following it will:
# 
# 1. get all values for the **taxon** level
# 2. user the *unique* method of the index to deduplicate the values
# 3. check the length of the index

# In[42]:

print(len(dataframe.index.get_level_values('taxon').unique()))


# ### Using EC to reduce the number of rows
# 
# One of the points here, is that we want to plot a diversity profile for each taxon that includes the boxplot for each of its genes. If we want to see all of them it will not be readable at all. Since it's too much data to visualise a good idea is taking hints of what seems to be important.
# 
# Reducing the complexity compromise the use of a mapping for both the genes *and* a different taxonomic *rank*. This allows to condense more information into a series of plots. It can be done using the **get_gene_taxon_dataframe** function and the following will make a EC/Phylum DataFrame.

# In[43]:

dataframe = mgkit.snps.conv_func.get_gene_taxon_dataframe(snp_data, taxonomy, gene_map=ec_map, rank='phylum')


# In[44]:

print(len(dataframe.index.get_level_values('gene').unique()))


# The number of plots is reduced and we can also reduce more by using a 3 level notation, instead of a 4 level one. One way to do this is using the already made *ec_map* and reducing the level of each enzyme associated with a KO identifier, using the **mgkit.mappings.enzyme.get_enzyme_level** function. This function accept a level (1 to 4), besides the EC identifier to change.
# 
# **Note:** take care to deduplicate the transformed EC identifiers, as they can change the diversity estimates.

# In[45]:

ec3_map = {
    # a set can be created using all the EC identifiers from the ec_map dictionary
    ko_id: {mgkit.mappings.enzyme.get_enzyme_level(ec_id, 3) for ec_id in ec_ids}
    for ko_id, ec_ids in ec_map.iteritems()
}


# In[46]:

# For comparison
print(ec3_map['K15864'], ec_map['K15864'])


# In[47]:

# The new DataFrame
dataframe = mgkit.snps.conv_func.get_gene_taxon_dataframe(snp_data, taxonomy, gene_map=ec3_map, rank='phylum')


# In[48]:

print(len(dataframe.index.get_level_values('gene').unique()))


# As you can see, the number of genes was almost halved. It is a very specific level of functionality that can be undestood from this. The DataFrame can be plot on a 6x4 grid, using **mgkit.plots.get_grid_figure**, which internally uses the **GridSpec** class of matplotlib.

# In[49]:

# As long as the multiplied numbers result in at least 13, the size of the plot
# can be customised
nrows = 5
ncols = 3

# the difference lies in the size of the grid we want to use and the return value
# that is a GridSpec instance
fig, gs = mgkit.plots.get_grid_figure(nrows, ncols, figsize=(5 * ncols, 5 * nrows))

for figid, ec_id in enumerate(sorted(dataframe.index.get_level_values('gene').unique())):
    # to create the axis for each it can either be used a gs[figid] to access in order the
    # block in the grid, or the notation gs[0, 1], to access the first row, second column
    # of the grid. It's easier to automate the process by using a single index notation,
    # so that's what we use in the example
    ax = fig.add_subplot(gs[figid])
    
    # we only plot one EC at a time
    ec_df = dataframe.loc[ec_id]
    
    #sort the DataFrame to plot them by mean value
    plot_order = ec_df.mean(axis=1).sort_values(inplace=False, ascending=False).index

    _ = mgkit.plots.boxplot.boxplot_dataframe(
        ec_df, 
        plot_order,
        ax, 
        fonts=dict(fontsize=14, rotation='horizontal'),
        data_colours={
            x: color
            for x, color in zip(plot_order, seaborn.color_palette('hls', len(ec_df.index)))
        },
        box_vert=False,
        label_map={x: taxonomy[x].s_name.capitalize() for x in plot_order}
    )
    _ = ax.set_title(ec_id)
fig.tight_layout()

